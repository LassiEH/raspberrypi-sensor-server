from flask import Flask, render_template
from sense_hat import SenseHat
from io import BytesIO

import matplotlib.pyplot as plt
import datetime
import base64

sense = SenseHat()
state = False
file_path = "sensor_data_log.txt"

sense.clear((0,0,0))

app = Flask(__name__)


"""
Gets todays date
"""
def get_date():
    date = datetime.datetime.now()
    return date.strftime("%d.%m.%Y")

"""
Gets the temperature from the SenseHat sensor
"""
def get_temperature():
    return round(sense.get_temperature(),1)

"""
Gets the pressure from the SenseHat sensor
"""
def get_pressure():
    return round(sense.get_pressure(),1)

"""
Gets the humidity from the SenseHat sensor
"""
def get_humidity():
    return round(sense.get_humidity(),1)

"""
Calculates the average value for
the past 5 sensor reading values
"""
def average_value(list):
    if not list: 
        return None
    
    numeric = [float(value) for value in list]

    return sum(numeric) / len(numeric)

"""
Fetches the data stored in the txt file and
creates a graph using matplotlib
"""
def get_historical_sensor_data(type):
    temps = []
    press = []
    humis = []

    with open(file_path, 'r') as file:
        for line in file:
            attributes = line.strip().split('|')
            temps.append(attributes[0])
            press.append(attributes[1])
            humis.append(attributes[2])

    if type == 'temp':
        plt.plot(range(len(temps)),temps, marker='o', linestyle='-', color='r')
        plt.xlabel('Time')
        plt.ylabel('Temperature (Celcius)')
        plt.grid(True)

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        image_in_b64 = base64.b64encode(image_stream.read()).decode('utf-8')
        plt.close()
        avg = 0
        if len(temps) >= 5:
            avg = average_value(temps[-5:])
        return image_in_b64, avg
    
    if type == 'pres':
        plt.plot(range(len(press)), press, marker='o', linestyle='-', color='g')
        plt.xlabel('Time')
        plt.ylabel('Pressure (millibar)')
        plt.grid(True)

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        image_in_b64 = base64.b64encode(image_stream.read()).decode('utf-8')
        plt.close()
        if len(press) >= 5:
            avg = average_value(press[-5:])
        return image_in_b64, avg
    
    if type == 'humi':
        print(humis)
        plt.plot(range(len(humis)), humis, marker='o', linestyle='-', color='b')
        plt.xlabel('Time')
        plt.ylabel('Humidity (%)')
        plt.grid(True)

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        image_in_b64 = base64.b64encode(image_stream.read()).decode('utf-8')
        plt.close()
        if len(humis) >= 5:
            avg = average_value(humis[-5:])
        return image_in_b64, avg

"""
Logs sensor data into a txt file
"""
def log_sensor_data(file_pth, temp, pres, humi):
    with open(file_pth, 'a') as file:
        file.write(f"{temp}|{pres}|{humi}\n")
        

"""
Collectively fetches the data from the sensors and returns them
"""
def get_sensor_data():
    temp = get_temperature()
    pres = get_pressure()
    humi = get_humidity()
    log_sensor_data(file_path, temp, pres, humi)
    return temp, pres, humi

"""
Turns the 8x8 led on or off
"""
def toggle_led():
    global state
    if state:
        r = 255
        g = 255
        b = 255
        sense.clear((r,g,b))
    if not state:
        r = 0
        g = 0
        b = 0
        sense.clear((r,g,b))
    state = not state
        


@app.route("/")
def greeting():
    
    templateData = {
        'title' : "Temperature control station",
        'time' : get_date()
    }
    return render_template('index.html', **templateData)

@app.route("/<action>")
def action(action):
    if action == 'fetch':
        temp, pres, humi = get_sensor_data()
        templateData = {
        'temp' : temp,
        'pres' : pres,
        'humi' : humi,
        'time' : get_date()
        }
        return render_template('index.html', **templateData)
    
    if action == 'light':
        toggle_led()
        return render_template('index.html')
    
    if action == 'historicalTemp':
        img, avg = get_historical_sensor_data('temp')
        templateData = {
            'img' : img,
            'avg' : avg
        }
        return render_template('index.html', **templateData)

    if action == 'historicalPres':
        img, avg = get_historical_sensor_data('pres')
        templateData = {
            'img' : img,
            'avg' : avg
        }
        return render_template('index.html', **templateData)

    if action == 'historicalHumi':
        img, avg = get_historical_sensor_data('humi')
        templateData = {
            'img' : img,
            'avg' : avg
        }
        return render_template('index.html', **templateData)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

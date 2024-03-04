import unittest
import pyserverTemplate
from datetime import datetime


class TestPyserverTemplate(unittest.TestCase):
    """
    Test fetching a temperature value
    """
    def test_get_temperature(self):
        temp = pyserverTemplate.get_temperature()
        print(temp)
        self.assertLess(temp, 40)
        self.assertGreater(temp, 20)

    """
    Test fetching a pressure value
    """
    def test_get_pressure(self):
        pres = pyserverTemplate.get_pressure()
        print(pres)
        self.assertLess(pres, 1022,0)
        self.assertGreater(pres, 1014,0)

    """
    Test fetching a humidity value
    """
    def test_get_humidity(self):
        humi = pyserverTemplate.get_humidity()
        print(humi)
        self.assertLess(humi, 20,0)
        self.assertGreater(humi,17,0)

    """
    Test getting a timedate value.
    Tests that the values are numeric and that it
    gives the correct date
    """
    def test_get_date(self):
        time = pyserverTemplate.get_date()
        values = time.strip().split('.')
        print(values[0])
        self.assertEqual(values[0].isnumeric(), True)
        print(values[1])
        self.assertEqual(values[1].isnumeric(), True)
        print(values[2])
        self.assertEqual(values[2].isnumeric(), True)
        date_now = datetime.now()
        date_string = date_now.strftime('%d.%m.%Y')
        self.assertEquals(time, date_string)

    """
    Test logging sensor readings
    """
    def test_log_sensor_data(self):
        file_pth = "test_sensor_data_log.txt"
        pyserverTemplate.log_sensor_data(file_pth, 22, 1017, 18)

        with open(file_pth, 'r') as file:
            for line in file:
                attributes = line.strip().split('|')
            
                self.assertEqual(attributes[0], "22")
                self.assertEqual(attributes[1], "1017")
                self.assertEqual(attributes[2], "18")

    """
    Test average calculation
    """
    def test_average_value(self):
        values = ['1','2','3','4','5','6','7','8','9','10']
        floatvalues = ['1.4', '6.3', '8.9', '1.0', '50.9']
        avg_values = pyserverTemplate.average_value(values)
        avg_floatvalues = pyserverTemplate.average_value(floatvalues)
        self.assertEqual(avg_values, 5.5)
        self.assertEqual(avg_floatvalues, 13.7)


        

    

if __name__ == '__main__':
    unittest.main()
    
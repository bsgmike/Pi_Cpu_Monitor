import RPi.GPIO as GPIO
import Adafruit_DHT

dht22_sensor = Adafruit_DHT.DHT22
humidity, temperature = Adafruit_DHT.read_retry(dht22_sensor, 26)


print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))

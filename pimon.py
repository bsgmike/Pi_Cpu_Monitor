# --------------Driver Library-----------------#
import RPi.GPIO as GPIO
import examples.OLED_Driver as OLED
# --------------Image Library---------------#
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
import time
from gpiozero import CPUTemperature
import board
import adafruit_dht

from PIL import ImageColor


# -------------Test Display Functions---------------#

def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf', 24)

    draw.text((0, 12), 'WaveShare', fill="BLUE", font=font)
    draw.text((0, 36), 'Electronic', fill="BLUE", font=font)
    draw.text((20, 72), '1.5 inch', fill="CYAN", font=font)
    draw.text((10, 96), 'R', fill="RED", font=font)
    draw.text((25, 96), 'G', fill="GREEN", font=font)
    draw.text((40, 96), 'B', fill="BLUE", font=font)
    draw.text((55, 96), ' OLED', fill="CYAN", font=font)

    OLED.Display_Image(image)


def Time_test():
    fred = datetime.datetime.now()
    # fred =time.time()
    # hms = time.strftime('%H:%M:%S', fred)
    time = fred.strftime("%H:%M:%S")
    cpuData = CPUTemperature()
    print("{0:.1f}".format(cpuData.temperature))
    temperature = "{0:.1f}".format(cpuData.temperature)
    # temperature = str(cpuData.temperature)
    # print(temperature)
    room_temp = roomtemperature()
    print("Time_test received ", room_temp)

    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('cambriab.ttf',24)
    # font_12 = ImageFont.truetype('cambriab.ttf', 12)
    # font_acme = ImageFont.truetype('Baloo-Regular.ttf', 36)
    # font_jetbrains = ImageFont.truetype('JetBrainsMono-Regular.ttf', 24)
    font_saxmono = ImageFont.truetype('saxmono.ttf', 16)
    font_clock = ImageFont.truetype('saxmono.ttf', 24)
    font_temperature = ImageFont.truetype('saxmono.ttf', 24)

    draw.text((0, 12), 'Mikes Clock', fill="BLUE", font=font_saxmono)
    draw.text((0, 30), time, fill="YELLOW", font=font_clock)
    draw.text((0, 100), temperature, fill="RED", font=font_temperature)
    if room_temp is not None:
        draw.text((0, 65), room_temp, fill="ORANGE", font=font_temperature)
    print(time)
    OLED.Display_Image(image)


def roomtemperature():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )

            # draw.text((0, 60), "Hello", fill="YELLOW", font=font_clock)
        )
        degree_sign = u"\N{DEGREE SIGN}"
        temperature = "{:.1f}".format(temperature_c)
        temperature = temperature + degree_sign + "C"
        print("my room temp = ", temperature)
        return temperature

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])


# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D23)
# ----------------------MAIN-------------------------#
try:

    def main():

        # -------------OLED Init------------#
        OLED.Device_Init()

        # Test_Text()
        Time_test()

        while (True):
            Time_test()

            time.sleep(2)
            # pass


    if __name__ == '__main__':
        main()

except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()


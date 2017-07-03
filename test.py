import time
import json


class DarkSkyTest:

    def __init__(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        self.pixel = {}

    def lightningStrobe(self, red, green, blue):
        # Wipe white across display a pixel at a time very quickly
        list = [5, 20, 3, 8, 5, 10]
        for i in range(0, len(list)):
            for j in range(self.config['led']['count']):
                if i % 2 == 0:
                    self.pixel[j] = (0, 0, 0)
                else:
                    self.pixel[j] = (red, green, blue)

                print(self.pixel)
                time.sleep(i / 1000.0)

    def colorWipe(self, red, green, blue, wait_ms=80):
        # Wipe color across display a pixel at a time
        for i in range(self.config['led']['count']):
            # Set max brighness as percentage
            brightness = self.config['led']['brightness']
            self.pixel[i] = [round(red * brightness), round(green * brightness), round(blue * brightness)]
            print(self.pixel)
            time.sleep(wait_ms / 1000.0)


# Initiate instance of the class
test = DarkSkyTest()

print(test.colorWipe(255, 0, 0))

#Gets / Sets a GPIO on the RPi
try:
    import RPi.GPIO

    class GpioControl:
        def write(number, on, activeLow=False):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio, GPIO.OUT)
            high = on ^ activeLow
            if high:
                GPIO.output(gpio, GPIO.HIGH) 
            else:
                GPIO.output(gpio, GPIO.LOW) 

        def read(number, activeLow=False):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(number, GPIO.IN)

            if(GPIO.input(number) == GPIO.HIGH):
                return not activeLow
            else:
                return activeLow 
            #             | AL= False | AL= True  |
            # GPIO HIGH   | True      | False     |
            # GPIO LOW    | False     | True      |

except: 
    from flask import current_app
    class GpioControl:
        def write(number, on, activeLow=False):
            if on:
                current_app.logger.info("Write output {} ON\n".format(number))
            else: 
                current_app.logger.info("Write output {} OFF\n".format(number))

        def read(number, activeLow=False):
            print("Read input {}\n".format(number))    
            return not activeLow


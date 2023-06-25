from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import time  # Don't forget to import time
import atexit

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['LOGGER_HANDLER_POLICY'] = 'always'
app.config['LOGGER_NAME'] = 'app.logger'
Bootstrap(app)
socketio = SocketIO(app)


# Setup the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pins = {"red": 17, "green": 27, "blue": 22}
touch_sensor_pin = 23
buzzer_pin = 18  # Define your buzzer pin



GPIO.setup(list(led_pins.values()), GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)  # Setup the buzzer pin
GPIO.setup(touch_sensor_pin, GPIO.IN)

# Initialize the buzzer
buzzer = GPIO.PWM(buzzer_pin, 1)  # 1 is just an initial frequency
buzzer.start(0)  # Start with duty cycle 0%

def cleanup (): 
    buzzer.stop()
    GPIO.cleanup()

atexit.register(cleanup)

@app.route("/")
def index():
    return render_template("index.html")

# Replace these with your own functions to control the components
@socketio.on("control_led")
def control_led(color, state):
    GPIO.output(led_pins[color], state)

@socketio.on("play_buzzer")
def play_buzzer(frequency, duration):
    buzzer.ChangeFrequency(frequency)  # Change the frequency
    buzzer.ChangeDutyCycle(50)  # 50% to make it audible
    time.sleep(duration)
    buzzer.ChangeDutyCycle(0)  # Stop the buzzer

@socketio.on("read_touch_sensor")
def read_touch_sensor():
    state = GPIO.input(touch_sensor_pin)
    return {"state": state}

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


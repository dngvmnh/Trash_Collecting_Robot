import random
import serial
ser = serial.Serial('COM8', 9600)
from pynput import keyboard
def generate_random_letter():
    letters = [b'f', b'r', b'b', b'l']
    return random.choice(letters)
interrupt = False
def on_press(key):
    global interrupt
    interrupt = True
    if key == keyboard.Key.down:
        ser.write(b'2')
    elif key == keyboard.Key.left:
        ser.write(b'4')
    elif key == keyboard.Key.right:
        ser.write(b'6')
    elif key == keyboard.Key.up:
        ser.write(b'8')

def waitForExecution():
    while True:
                data = ser.readline().decode().strip()
                if (data.lower()=='done executing'):
                    break
                                                     
def on_release(key):
    ser.write(b'0')
    global interrupt
    interrupt = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        if interrupt:
            print("Interrupted. Waiting for interrupt to become False...")
            while interrupt:
                pass 
            print("Interrupt resolved. Resuming...")
        else:
            random_letter = generate_random_letter()
            ser.write(random_letter)
            print('done writing')
            waitForExecution()
            print(random_letter)

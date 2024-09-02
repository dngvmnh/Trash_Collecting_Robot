#robot going randomly
#interruption from keyboard can manually navigate robot


import random
import serial
import time
ser = serial.Serial("COM8", 9600, timeout=.1)
from pynput import keyboard
actions = [b"forward\n", b"backward\n", b"turnRight\n", b"turnLeft\n"]

interrupt = False
def on_press(key):
    global interrupt
    if key == keyboard.Key.down:
        ser.write(b"backward\n")
        interrupt = True
    elif key == keyboard.Key.left:
        ser.write(b"turnLeft\n")
        interrupt = True
    elif key == keyboard.Key.right:
        ser.write(b"turnRight\n")
        interrupt = True
    elif key == keyboard.Key.up:
        ser.write(b"forward\n")
        interrupt = True
                                      
def on_release(key):
    ser.write(b"stop\n")
    global interrupt
    interrupt = False

def goRandomly():
    nextAction = random.choice(actions)
    ser.write(nextAction)
    if actions.index(nextAction) < 2:
        for i in range(random.randint(10,20)):
            time.sleep(0.1)
            if (bottleFound()):
                break
    else:
        for i in range(random.randint(1,10)):
            time.sleep(0.1)
            if (bottleFound()):
                break
    ser.write(b"stop\n")

def bottleFound():
    data = ser.readline().decode().strip()
    if (data == "bottle found"):
        return True
    return False
def bottleCollected():
    data = ser.readline().decode().strip()
    if (data == "bottle collected"):
        return True
    return False

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            if not interrupt or bottleFound():
                goRandomly()
            if bottleFound():
                while not bottleCollected():
                    pass
main()
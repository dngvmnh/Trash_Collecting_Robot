import serial
from pynput import keyboard

ser = serial.Serial('COM13', 9600)

def on_key_press(key):
    if key == keyboard.Key.down:
        ser.write(b"backward\n")
    elif key == keyboard.Key.left:
        ser.write(b"turnLeft\n")
    elif key == keyboard.Key.right:
        ser.write(b"turnRight\n")
    elif key == keyboard.Key.up:
        ser.write(b"forward\n")

def on_key_release(key):
    if key in [keyboard.Key.down, keyboard.Key.left, keyboard.Key.right, keyboard.Key.up]:
        ser.write(b"stop\n")

listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
listener.start()
listener.join()
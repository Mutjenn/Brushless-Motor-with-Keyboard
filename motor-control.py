import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

# GPIO pin belirleme
GPIO.setmode(GPIO.BCM)
up_down_motor_channels = [12, 13]  # üst alt motorlar
forward_backward_motor_channels = [10, 11, 14, 15]  # ileri geri motorlar

# ESC kalibrasyonu
ESC_MIN = 205
ESC_MAX = 405
ESC_NEUTRAL = (ESC_MIN + ESC_MAX) // 2 #305 Orta değer

# PCA9685 kurulumu
pca = Adafruit_PCA9685.PCA9685()
pca.set_pwm_freq(50)  

# Motor kontrol fonksiyonları
def set_motor_speed(channel, speed):
    pulse = int(ESC_NEUTRAL + speed * (ESC_MAX - ESC_NEUTRAL))
    pca.set_pwm(channel, 0, pulse)

def stop_all_motors():
    for channel in up_down_motor_channels + forward_backward_motor_channels:
        set_motor_speed(channel, 0)

try:
    print("Use 'W' to move up, 'S' to move down, 'A' to go backward, 'D' to go forward, 'L' for left turn, 'R' for right turn, 'X' to stop all motors.")

    while True:
        user_input = input("Enter command: ").upper()

        if user_input == 'W':
            
            for channel in up_down_motor_channels:
                set_motor_speed(channel, 0.5) #yukarı

        elif user_input == 'S':
            
            for channel in up_down_motor_channels:
                set_motor_speed(channel, -0.5)#aşağı

        elif user_input == 'A':
            
            for channel in forward_backward_motor_channels:
                set_motor_speed(channel, -1.0)#geri

        elif user_input == 'D':
            
            for channel in forward_backward_motor_channels:
                set_motor_speed(channel, 1.0)#ileri

        elif user_input == 'L':
            
            for channel in forward_backward_motor_channels[1:4]:  # Motors 2-4
                set_motor_speed(channel, -1.0)
            for channel in forward_backward_motor_channels[2:3]:  # Motors 3-5
                set_motor_speed(channel, 1.0)#sola dön

        elif user_input == 'R':
            
            for channel in forward_backward_motor_channels[1:4]:  # Motors 2-4
                set_motor_speed(channel, 1.0)
            for channel in forward_backward_motor_channels[2:3]:  # Motors 3-5
                set_motor_speed(channel, -1.0)#sağa dön

        elif user_input == 'X':
            stop_all_motors()#motorları durdur

        else:
            print("Invalid command. Use 'W', 'S', 'A', 'D', 'L', 'R', or 'X'.")

except KeyboardInterrupt:
    stop_all_motors()
    print("\nExiting the program.")

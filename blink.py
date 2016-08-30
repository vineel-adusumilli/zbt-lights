#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

class Letter:
  def __init__(self, rpin, gpin, bpin):
    self.rpin = rpin
    self.gpin = gpin
    self.bpin = bpin
    GPIO.setup(self.rpin, GPIO.OUT)
    GPIO.setup(self.gpin, GPIO.OUT)
    GPIO.setup(self.bpin, GPIO.OUT)
    self.rpwm = GPIO.PWM(self.rpin, 50)
    self.gpwm = GPIO.PWM(self.gpin, 50)
    self.bpwm = GPIO.PWM(self.bpin, 50)
    self.rpwm.start(0)
    self.gpwm.start(0)
    self.bpwm.start(0)

  def rgb(self, r, g, b):
    self.rpwm.ChangeDutyCycle((255 - r) * 100.0 / 255)
    self.gpwm.ChangeDutyCycle((255 - g) * 100.0 / 255)
    self.bpwm.ChangeDutyCycle((255 - b) * 100.0 / 255)

GPIO.setmode(GPIO.BCM)
z = Letter(24, 25, 23)
b = Letter(20, 21, 16)
t = Letter(19, 26, 13)


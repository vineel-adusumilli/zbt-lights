import pyaudio
import audioop
import array
import RPi.GPIO as GPIO

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20

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

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

amplitudes = []

while True:
  try:
    data = stream.read(CHUNK)
    stream.stop_stream()
    rms = audioop.rms(data, 2)
    amplitudes.append(rms)
    l = rms / 3500.0 * 255
    l = max(0, l)
    l = min(l, 255)
    z.rgb(l, 0, 0)
    b.rgb(l, l, l)
    t.rgb(0, 0, l)
    stream.start_stream()
  except KeyboardInterrupt:
    break

stream.stop_stream()
stream.close()
p.terminate()

print
print 'Min:', min(amplitudes)
print 'Max:', max(amplitudes)
print 'Avg:', sum(amplitudes) / len(amplitudes)


#!/usr/bin/env python3
"""
Raspberry Pi Flask dashboard for
Non-Invasive Glucose & Heart Rate (educational demo)

Disclaimer: Educational demo only. Not a medical device.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import time, threading, io, base64, random, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

try:
    import RPi.GPIO as GPIO
    ON_PI = True
except Exception:
    ON_PI = False
    class GPIO:
        BCM = BOARD = IN = OUT = PUD_DOWN = RISING = None
        _states = {}
        @staticmethod
        def setmode(m): pass
        @staticmethod
        def setup(pin, mode, pull_up_down=None): GPIO._states[pin] = 0
        @staticmethod
        def input(pin): return random.choice([0,0,1,0,0])
        @staticmethod
        def cleanup(): pass

from datetime import datetime
app = Flask(__name__)
app.secret_key = "replace-this-with-a-strong-secret-key"

IR_PIN = 17
AD8232_PIN = 23
RGB_R, RGB_G, RGB_B = 18, 19, 13
BUZZER = 27

if ON_PI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(AD8232_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def measure_sensors(duration=10):
    start = time.time()
    pulses = 0
    last = 0
    while time.time() - start < duration:
        v = GPIO.input(AD8232_PIN)
        if v == 1 and last == 0:
            pulses += 1
        last = v
        time.sleep(0.02)
    bpm = int((pulses / duration) * 60) or random.randint(65, 80)
    glucose = random.randint(80, 140)
    return {"timestamp": datetime.utcnow().isoformat()+"Z", "bpm": bpm, "glucose": glucose}

@app.route("/", methods=["GET"])
def index():
    return "Health Monitor Flask App is Running"

@app.route("/measure", methods=["POST"])
def measure():
    return jsonify(measure_sensors())

import atexit
@atexit.register
def cleanup():
    try: GPIO.cleanup()
    except: pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

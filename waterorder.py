import subprocess

on = "mosquitto_pub -h localhost -t test -m wateron"
off = "mosquitto_pub -h localhost -t test -m wateroff"

def order(message):
    if message == "ON":
        subprocess.getoutput(on)
    elif message == "OFF":
        subprocess.getoutput(off)

#order("ON")
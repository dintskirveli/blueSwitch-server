import serial
from serial import SerialException
from flask import Flask
import time

blue = None
connecting = False
count = 0
def maybeConnect():
	global connecting
	global blue
	print "maybeConnect() "+str(connecting)
        try:
                if connecting == False :
                        connecting = True
                        print "trying to connect.."
                        del blue
                        blue = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=1)
			connecting = False
		else :
			print "already connecting"
        except SerialException:
		connecting = False
                print "Connection failed, trying again in 5 seconds..."
                time.sleep(5)
		maybeConnect()

def createApp():
        app = Flask(__name__)
        maybeConnect()
        return app

app = createApp()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/on", methods=['POST'])
def on():
        maybeWrite("1");
	stat = maybeRead();
	if stat.find("ON") != -1:
		connecting = False
        	return "ON\n"
	else :
		return "on() Error: "+stat+"\n"

@app.route("/off", methods=['POST'])
def off():
        maybeWrite("0");
	stat = maybeRead()
        if stat.find("OFF") != -1:
		connecting = False
                return "OFF\n"
        else :
                return "off() Error: "+stat+"\n"


@app.route("/toggle", methods=['POST'])
def toggle():
        maybeWrite("2")
	stat = maybeRead()
	global count
	count = count +1;
	print count
	if stat.find("OFF") != -1:
		connecting = False
		return "OFF\n"
	elif stat.find("ON") != -1:
		connecting = False
                return "ON\n"
        else :
                return "toggle() Error: "+stat+"\n"

@app.route("/status")
def status(i = 0):
        maybeWrite("3");
	stat = maybeRead()
	if stat.find("Status...ON") != -1:
		return "Status...ON\n"
	elif stat.find("Status...OFF") != -1:
		return "Status...OFF\n"
	elif i < 5:
		return status(i+1)
        return stat

def maybeWrite(x):
	try:
		blue.write(x)
	except SerialException:
		print "writing failed!"
		maybeConnect()
		return "read fail";

def maybeRead():
	try:
              	return blue.readline()
        except SerialException:
		print "reading failed!"
          	maybeConnect()
		return "read fail";
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4159, debug=True, use_reloader=False, threaded=False)


import paho.mqtt.client as mqtt
import pysdcp
import time


lastState = ""
projector = pysdcp.Projector('beamer.rzl.so')

def on_connect(client, userdata, flags, rc):
    print ("connected")
    client.subscribe("/service/beamer/command")

def on_message(client, userdata, msg):
    payload = msg.payload
    print(payload)
    global lastState
    lastState = ""
    if(payload == b'ON' or payload == b'1'):
       projector.set_power(True) 
    elif (payload == b'OFF' or payload == b'0'):
       projector.set_power(False) 
    else:
      client.publish("/service/beamer/error", payload="unknown command. please pass 0, 1, ON or OFF", qos=0)

client = mqtt.Client()
client.will_set('/service/beamer/state', 'offline', 0, True)
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("mqtt.rzl.so")
client.loop_start()

while True:
    state = 'unknown'
    try:
      state = projector.get_power_string()
    except:
      pass

    print (state)

    if(state != lastState):
      client.publish("/service/beamer/state", payload=state, qos=0, retain=True)
      lastState = state

    time.sleep(1)

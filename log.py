import time
import argparse

import psutil
import paho.mqtt.client as mqtt

#history list
history = []

def on_message(client, obj, msg):
    history.append(int(msg.payload))
    print(history)
    f = open("log.txt", 'w')
    for i in history:
        f.write( str(i) + ' ')
    f.close()

def main():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host='localhost', port=1883)
    client.subscribe('history', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    f = open("log.txt", 'w')
    f.close()
    main()

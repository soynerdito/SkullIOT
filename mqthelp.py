import paho.mqtt.client as paho

class MHelper:
    
    def __init__(self):
        self.client = 0

    def on_connect(self, client, userdata, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
    
    def on_disconnect(self, mosq, obj, rc):
        print("Disconnected successfully.")

    def on_publish(self, mosq, obj, mid):
        print("Message "+str(mid)+" published.")

    def on_messageold(self, mosq, obj, msg):
        print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)

    def on_subscribe(self, mosq, obj, mid, qos_list):
        print("Subscribe with mid "+str(mid)+" received.")

    def bind(self, client ):
        client.on_publish = self.on_publish
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe

    def config(self, ip, name ):
        self.client = paho.Client()
        #self.client = mosquitto.Mosquitto(name)
        self.bind( self.client )
        #self.client.connect(ip, 1883, 60)
        self.client.connect("iot.eclipse.org", 1883, 60)
        #self.client.connect( ip )
        return self.client


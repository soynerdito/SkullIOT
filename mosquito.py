from mqthelp import MHelper

helper = MHelper()
client = helper.config("192.168.10.106", "listener" )
client.subscribe("topic", 0)
client.loop(  )


#client = mosquitto.Mosquitto("listener")
#client.connect("192.168.10.118")
#client.loop()

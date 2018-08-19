import paho.mqtt.client as mqtt
import sys

class MqttClient:
	host = "example.org"
	port = 1883

	def __init__(self):
		pass
	
	def setRecvHandler(self, recvHandler):
		self.recvHandler = recvHandler

	def on_connect(self, client, userdata, flags, res_code):
		print " connectted!! result code :"+str(res_code)

	def on_message(self, client , userdata, msg):
		print "recv : "+str(msg.topic)+" : "+str(msg.payload)
		self.recvHandler(msg.topic, msg.payload)

	def on_log(self, client, userdata, level, buf):
		print "[log] : "+str(buf)

	def publish_to(self, topic, sendmsg):
		self.client.publish(topic, sendmsg)
		print "send message >"+ sendmsg
	
	def subscribe_to(self, read_topic):
		self.client.subscribe(read_topic)
		self.client.loop_start()

	def connect(self, logprint=False):
		self.client = mqtt.Client(protocol=mqtt.MQTTv311)
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		if logprint:
			self.client.on_log = self.on_log

		self.client.connect(MqttClient.host, port=MqttClient.port, keepalive=30)

	def disconnect(self):
		self.client.loop_stop()
		self.client.disconnect()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit(1)
	fname = sys.argv[1]
	f = open(fname)
	data = f.read()
	print (data)
	client = MqttClient()
	client.connect(logprint=True)
	client.publish_to("motiontest",data)
	print ("end")


from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
import random
from paho.mqtt import client as mqtt_client
#Set paramter of MQTT broker connection
broker = 'broker.hivemq.com'
port = 1883
topic = "iot-nhom7"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'abc'
password = 'public'
#function will be called after connecting the client
#create MQTT client at the same time and this client will connect to broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker !")
        else:
            print("Falied to connect, return code %d\n". rc)
    #Set connecting Client Id
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
#Publish messages
#send message to the topic python/mqtt every second
def publish(client, msg_count):
    # msg_count = {"username":"vietanh", "label": "in", "exit": "y"}
    # while True:
	# time.sleep(1)
	msg = f'messages: {msg_count}'
	result = client.publish(topic, msg)
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f'Failed to send message to topic {topic}')

@login_required
def register(request):
	if request.user.username!='vietanh':
		return redirect('not-authorised')
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			msg = {"username": form.data["username"], "password": form.data["password1"], "exit": "n"}
			client = connect_mqtt()
			print("FORM:", form.data["username"], form.data["password1"])
			publish(client, msg)

			# form.save() ###add user to database
			messages.success(request, f'Employee registered successfully!')
			return redirect('dashboard')
		


	else:
		form=UserCreationForm()
	return render(request,'users/register.html', {'form' : form})






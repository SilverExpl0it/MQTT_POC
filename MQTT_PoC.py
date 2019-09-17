import paho.mqtt.client as mc


class MQTT:
    def __init__(self, file_name, target):
        self.file_name = file_name
        self.target = target
        self.file_to_save = None
        self.connected = False

    def start(self):
        try:
            self.file_to_save = open(self.file_name, "w+")
        except Exception as e:
            print(e)
            print("Error found")
            return
        print("Waiting for info")
        client = mc.Client(client_id="MqttClient")
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        try:
            client.connect(self.target)
            client.loop_forever()
        except:
            if self.file_to_save:
                self.file_to_save.close()
        print("\nData in " + self.file_name)

    def __on_connect(self, client, userdata, flags, rc):
        if not self.connected:
            print("Connection succesful")
            self.connected = True
        client.subscribe("#", qos=1)
        client.subscribe("$SYS/#")

    def __on_message(self, client, userdata, msg):
        self.file_to_save.write(f"Topic >> {msg.topic} -- Message >> {msg.payload.decode('utf-8')}\n")


if __name__ == "__main__":
    mqtt = MQTT("./mqtt_info.txt", "127.0.0.1")
    mqtt.start()

import json

# specially deal with rabbit MQ
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.parms = pika.URLParameters(cloud_amqp_url)
        self.parms.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.parms)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name) # create queue if not exist

    # send a message
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print("[x] Sent message to %s:%s" % (self.queue_name, message))

    # get a message
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        # if method_frame is not None
        if method_frame:
            print("[x] Received message from %s:%s" % (self.queue_name, body))
            # tell queue you received the msg, and it can be removed from queue.
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode('utf-8'))
        else:
            print("No message returned.")
            return None

    # BlockingConnection.sleep is a safer way to sleep than time.sleep(). This
    # will still to send heartbeat to remote cloudAMQP server.
    # if only use python's sleep, heartbeat will stop to send, the connection will be removed by remote server.
    def sleep(self, seconds):
        self.connection.sleep(seconds)

from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://oibmmghn:sKrkMTtm55KnbDfURC0ouVbuF06pQigw@termite.rmq.cloudamqp.com/oibmmghn"
TEST_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    msg = {'test': 'demo'}
    client.sendMessage(msg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert msg == receivedMsg
    print 'test_basic paassed!'

if __name__ == "__main__":
    test_basic()

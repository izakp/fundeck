from kombu import Queue, Producer, Connection, Exchange
from kombu.pools import connections
from kombu.utils import uuid
from kombu.five import Empty

class PublishingException(Exception):
    pass

class BasePublisher(object):
    def __init__(self, broker_url):
        self.connection = connections[Connection(broker_url)].acquire()

    def publish_message(self, payload, queue_name, headers=None, properties={}, retry=True, declare_queue=False, connect_max_retries=3):
        with connections[self.connection].acquire() as conn:
            conn.ensure_connection(max_retries=connect_max_retries)
            if declare_queue:
                queue = Queue(queue_name, routing_key=queue_name)
                queue(conn).declare()

            producer = conn.Producer(serializer='json')
            try:
                producer.publish(payload, routing_key=queue_name, headers=headers, retry=retry, **properties)
            except Exception, e:
                logger.error(repr(e))
                raise PublishingException("Failed to publish message %s" % payload)

    def publish_message_to_exchange(self, payload, exchange_name, exchange_type="topic", routing_key="", headers=None, properties={}, retry=True, connect_max_retries=3):
        exchange = Exchange(exchange_name, type=exchange_type)
        with connections[self.connection].acquire() as conn:
            conn.ensure_connection(max_retries=connect_max_retries)
            producer = conn.Producer(exchange=exchange, serializer='json')
            try:
                producer.publish(payload, exchange=exchange, routing_key=routing_key, headers=headers, retry=retry, **properties)
            except Exception, e:
                logger.error(repr(e))
                raise PublishingException("Failed to publish message %s" % payload)

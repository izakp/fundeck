import signal
import traceback

from kombu import Queue, Connection, binding
from kombu.mixins import ConsumerMixin
from kombu.utils import uuid
from kombu.five import Empty
from kombu.pools import connections

import logging
logger = logging.getLogger(__name__)

class BaseConsumer(ConsumerMixin):
    def __init__(self, broker_url, queue_names,
                    declare_queues=False, exchange=None,
                    routing_key=None, auto_delete=False,
                    additional_bindings=[], max_requeues=3):
        self.connection = connections[Connection(broker_url)].acquire()
        self.queue_names = queue_names
        self.declare_queues = declare_queues
        self.exchange = exchange
        self.routing_key = routing_key
        self.auto_delete = auto_delete
        self.additional_bindings = additional_bindings
        self.max_requeues = max_requeues

    def get_consumers(self, Consumer, channel):
        queues = []
        for queue_name in self.queue_names:
            if self.exchange is not None:
                bindings = [binding(self.exchange, routing_key=self.routing_key)]
                for additional_binding in self.additional_bindings:
                    bindings.append(binding(self.exchange, routing_key=additional_binding))
                queue = Queue(queue_name, bindings, auto_delete=self.auto_delete)
            else:
                queue = Queue(name=queue_name, routing_key=queue_name)

            queues.append(queue)

        return [Consumer(queues=queues,
                        auto_declare=self.declare_queues,
                        callbacks=[self.handle_delivery])]

    def on_consume_end(self, connection, channel):
        logger.info("Cancelling connections...")
        connection.release()
        logger.info("Done.")

    def shutdown(self, *args):
        logger.info("Shutting down...")
        self.should_stop = True

    def handle_delivery(self, body, message):
        self.process_message(message)
        message.ack()

    def process_message(self, message):
        raise NotImplementedError

    def start(self):
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
            signal.signal(sig, self.shutdown)

        try:
            logger.info("Starting consumer on %s" % self.connection.host)
            logger.info("Listening on queues %s" % self.queue_names)
            logger.info("Consumer ready.")
            self.run()

        except Exception, exc:
            logger.fatal("%s \n %s" % (exc, traceback.format_exc()))
            self.shutdown()

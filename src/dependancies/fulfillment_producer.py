from src.clients.kafka.fulfillment_producer import FulfillmentProducer
from src.interfaces.fulfillment_producer_interface import FulfillmentProducerInterface


def get_fulfillment_producer() -> FulfillmentProducerInterface:
    return FulfillmentProducer()

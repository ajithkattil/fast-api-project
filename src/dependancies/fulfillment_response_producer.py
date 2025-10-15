from src.clients.kafka.fulfillment_response_producer import FulfillmentResponseProducer
from src.interfaces.fulfillment_response_producer_interface import FulfillmentResponseProducerInterface


def get_fulfillment_response_producer() -> FulfillmentResponseProducerInterface:
    return FulfillmentResponseProducer()

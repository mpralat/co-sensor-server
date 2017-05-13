from channels import include, route_class
from channels.generic.websockets import WebsocketDemultiplexer
from . import consumers


class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        'sensor': consumers.SensorConsumer,
    }


channel_routing = [
    route_class(Demultiplexer, path=r'^/room/[0-9A-F]{16}'),
]

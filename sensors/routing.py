from channels import route_class
from . import consumers


channel_routing = [
    route_class(consumers.SensorConsumer, path=r'^/room/[0-9A-F]{16}/sensor'),
    route_class(consumers.ClientConsumer, path=r'^/room/[0-9A-F]{16}/client'),
    route_class(consumers.ClientConsumer, path=r'^/room/[0-9A-F]{16}/stats'),
    route_class(consumers.ClientConsumer, path=r'^/room/[0-9A-F]{16}/map'),
]

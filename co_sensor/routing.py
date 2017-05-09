from channels import include
from sensors.routing import channel_routing as sensors_routing


channel_routing = [
    include(sensors_routing, path=r'^/sensors'),
]

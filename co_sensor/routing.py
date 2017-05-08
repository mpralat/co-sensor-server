from channels import include


channel_routing = [
    include("sensors.routing.websocket_routing", path=r'^sensors/room'),
]

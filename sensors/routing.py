from channels import include
from . import consumers


room_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}

channel_routing = [
    include(room_routing, path=r'^/room'),
]

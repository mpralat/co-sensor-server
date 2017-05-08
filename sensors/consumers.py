from channels import Group
from channels.sessions import channel_session
from .models import Room
import json


@channel_session
def ws_connect(message):
    print("Connected!")
    label = message['path'].strip('/').split('/')[-1]
    print(label)
    room = Room.objects.get(label=label)
    Group('room-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label
    message.reply_channel.send({
        'accept': True,
    })


@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(handle=data['handle'], message=data['message'])
    Group('room-'+label).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('room-'+label).discard(message.reply_channel)

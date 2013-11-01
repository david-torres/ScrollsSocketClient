import os
import sys
# add the parent dir to the path for this example
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from ScrollsSocketClient import ScrollsSocketClient

email = 'user@example.com'
password = 'password'
room = 'chatlog'


def connect(message):
    """ This function is executed upon receiving the 'FirstConnect' event """

    scrolls.send({'msg': 'JoinLobby'})

    # subscribe to the RoomEnter event with function room_enter()
    scrolls.subscribe('RoomEnter', room_enter)

    # subscribe to the RoomInfo event with function room_info()
    scrolls.subscribe('RoomInfo', room_info)

    # subscribe to the RoomChatMessage event with function room_chat()
    scrolls.subscribe('RoomChatMessage', room_chat)

    # enter the room
    scrolls.send({'msg': 'RoomEnter', 'roomName': room})

    # try entering a busy room for lots of updates
    # scrolls.send({'msg': 'RoomEnterFree', 'roomName': 'Trading'})


def room_info(message):
    """ This function is executed upon receiving the 'RoomInfo' event """
    print 'Currently in room: ' + ', '.join([profile['name'] for profile in message['profiles']])


def room_chat(message):
    """ This function is executed upon receiving the 'RoomChatMessage' event """
    print message['from'] + ': ' + message['text']


def room_enter(message):
    """ This function is executed upon receiving the 'RoomEnter' event """
    print 'Entered ' + message['roomName']


# give the client our username/password
scrolls = ScrollsSocketClient(email, password)

# subscribe to the FirstConnect event with function connect()
scrolls.subscribe('FirstConnect', connect)

# login to the server
scrolls.login()

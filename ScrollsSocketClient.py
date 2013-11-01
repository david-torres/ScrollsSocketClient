from threading import Thread
from Queue import Queue
import requests
import socket
import json
import time


class PingThread(Thread):
    def __init__(self, scrolls_client):
        self.scrolls_client = scrolls_client
        self.stopped = False
        Thread.__init__(self)

    def run(self):
        while not self.stopped:
            self.scrolls_client.send({'msg': 'Ping'})
            time.sleep(10)


class MessageThread(Thread):
    def __init__(self, scrolls_client):
        self.scrolls_client = scrolls_client
        self.stopped = False
        Thread.__init__(self)

    def run(self):
        while not self.stopped:
            # grab a message from queue
            message = self.scrolls_client.queue.get()

            # make a copy of the current subscribers to keep this thread-safe
            current_subscribers = dict(self.scrolls_client.subscribers)

            # send message to subscribers
            for subscriber_key, subscriber_callback in current_subscribers.iteritems():
                # msg or op should match what we asked for
                if 'msg' in message and message['msg'] == subscriber_key:
                    subscriber_callback(message)
                elif 'op' in message and message['op'] == subscriber_key:
                    subscriber_callback(message)

            # signals to queue job is done
            self.scrolls_client.queue.task_done()


class ReceiveThread(Thread):
    def __init__(self, scrolls_client):
        self.scrolls_client = scrolls_client
        self.stopped = False
        Thread.__init__(self)

    def run(self):
        while not self.stopped:
            self.scrolls_client.receive()


class ScrollsSocketClient(object):
    '''
    A Python client for the Scrolls socket server.

    Usage:
    YOUR_SCROLLS_EMAIL = 'user@example.com'
    YOUR_SCROLLS_PASSWORD = 'password'

    scrolls = ScrollsSocketClient(YOUR_SCROLLS_EMAIL, YOUR_SCROLLS_PASSWORD)

    '''

    # queue vars
    queue = Queue()
    subscribers = {}

    # auth vars
    auth_url = 'https://authserver.mojang.com/authenticate'
    json_header = {'content-type':'application/json'}
    username = None
    password = None

    # socket vars
    _socket_recv = 8192
    _scrolls_host = '54.208.22.193'
    _scrolls_port = 8081
    _reconnect_sleep = 10

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        self.ping_thread = PingThread(self)
        self.message_thread = MessageThread(self)
        self.receive_thread = ReceiveThread(self)

        self.receive_thread.start()
        self.message_thread.start()

    def login(self):
        params = json.dumps({
            'username': self.username,
            'password': self.password,
            'requestUser': True,
            'agent': {
                'name': 'Scrolls',
                'version': 1
            },
        })

        r = requests.post(self.auth_url, data=params, headers=self.json_header)
        login_message = {
            'accessToken': r.json(),
            'msg': 'FirstConnect'
        }

        self.send(login_message)
        self.ping_thread.start()

    def subscribe(self, event, callback):
        # add subscribers
        self.subscribers[event] = callback

    def unsubscribe(self, event):
        # rm subscribers
        self.subscribers.pop(event)

    def send(self, params):
        # send message
        self.socket.send(json.dumps(params))

    def receive(self):
        stream_data = ''
        data_json = None

        while (1):
            try:
                # read data from the buffer
                data = self.socket.recv(self._socket_recv)
            except socket.error:
                # socket error, disconnected
                stream_data = ''
                time.sleep(self._reconnect_sleep)
                self.connect()
                continue

            if not data:
                # no more data being transmitted, i.e disconnected
                stream_data = ''
                time.sleep(self._reconnect_sleep)
                self.connect()
                continue

            else:
                # append data to the response
                stream_data += data

                try:
                    # line breaks means we are handling multiple responses
                    if stream_data.find('\n\n'):
                        # split and parse each response
                        for stream_data_line in stream_data.split('\n\n'):
                            # try to load as JSON
                            data_json = json.loads(stream_data_line)

                            # we have a response, add it to the queue
                            self.queue.put(data_json)

                            # remove the line from stream data
                            stream_data = stream_data.replace(stream_data_line + '\n\n', '')

                    # we've processed the available message, reset stream_data
                    stream_data = ''
                except:
                    # invalid json, incomplete data
                    pass

    def connect(self):
        self.socket.connect((self._scrolls_host, self._scrolls_port))

    def quit(self):
        # stop all threads and close the socket
        self.receive_thread.stopped = True
        self.receive_thread._Thread__stop()

        self.message_thread.stopped = True
        self.message_thread._Thread__stop()

        self.ping_thread.stopped = True
        self.ping_thread._Thread__stop()

        self.socket.close()

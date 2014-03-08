#!/usr/bin/env python

#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


### Simple twisted Client to Controll my Local Tinkerforge
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data)
        #self.transport.write('fuckoff')

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


###############     BEGIN UI    ######################
############### Powered by KIVY ######################

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.textbox)
        self.layout.add_widget(self.label)
        return self.layout

    def connect_to_server(self):
        reactor.connectTCP('192.168.0.111', 8000, EchoFactory(self))

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection
        print self.connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += msg + "\n"


if __name__ == '__main__':
    TwistedClientApp().run()
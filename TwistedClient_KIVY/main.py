__version__ = '1.1a'

import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
#from kivy.uix.boxlayout import BoxLayout

#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

### Simple twisted Client to Controll my Local Tinkerforge
from twisted.internet import reactor, protocol

#sm = ScreenManager()
sm = ScreenManager(transition=SlideTransition())
#currentResponse = None

######################################################################

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        print 'receivedData!'
        self.factory.app.response.text = data
        #print data

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")

#####################################################################

class Menu(Screen):
    pass

class Setup(Screen):

    def callAction(self, sserver, pport):
        global server
        global port

        server = sserver
        port = pport 

        print 'would connect to: '+server+' on port: '+port
        # need onConnection function... but how reach 
        #print self.parent
        #print connection
        
        sm.current = 'controll' #change site!

    def send_message(self):
        print 'wrong send_message'

class Controll(Screen):
    connected = False    
    connectio = None    

    command = ObjectProperty(None) # fetch textInput element
    response = ObjectProperty(None) # fetch textInput element
    
    #print 'like init function...but silly!'
    def on_pre_enter(self):
        '''
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)'''
        self.response.text = 'connecting...'
        #print 'preparing connection'
        reactor.connectTCP(str(server), int(port), EchoFactory(self))

    def send_message(self, text):
        print 'send_message'
        if self.connected:
            print self.connected
            msg = text
            print text
            print self.connectio
            if msg and self.connectio:
                self.connectio.write(str(msg))
                print 'send: ' + msg
        else: 
            print 'not Connected'
            self.text = text

    def on_connection(self, connection):
        #print 'connected succesfully!'
        #self.print_message("connected succesfully!")
        #self.response.text = "Connected succesfully!"
        self.connected = True
        self.response.text = '[color=CCFF33]Connected succesfully![/color]'
        self.connectio = connection
        #self.print_message(str(self.text))
    
    def print_message(self, *args):
        msg = str(self.text)
        print self.text
        self.response.text = '<-? Command: ' + msg
        currentResponse = self.response

    def on_message(self):
        print 'run'

    '''
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            print 'pressed enter'
        print keycode[1]
        print modifiers
        #elif keycode[1] == 's':
        #    print 'pressed s'
        #elif keycode[1] == 'up':
        #    print 'pressed up'
        #elif keycode[1] == 'down':
        #    print 'pressed down'
        return True '''

class TinkerclientApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::

         app = App.get_running_app()
         print (app.title)

       in kv language::

         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name of this cass::

         MainApp = main.kv
         MainClass = mainclass.kv

       The App part is auto removed and the whole name is lowercased.
    '''
    def build(self):
        sm.add_widget(Menu(    name='menu'))
        sm.add_widget(Setup(   name='setup'))
        sm.add_widget(Controll(name='controll'))
        return sm


if __name__ == '__main__':
    tinker = TinkerclientApp()
    tinker.run()
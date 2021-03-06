#!/usr/bin/env python

import sys
import dbus
from PyQt4.QtGui import QApplication
from dbus.mainloop.qt import DBusQtMainLoop

bus_loop = DBusQtMainLoop(set_as_default=True)
answer = ""

def connect_dbus(text = "", flag = "message"):
    global answer
    answer = text
    if flag == "message":
        bus = dbus.SessionBus()
        bus.add_signal_receiver(pidgin_control_func,
                                dbus_interface="im.pidgin.purple.PurpleInterface",
                                signal_name="ReceivedImMsg")

def pidgin_control_func(account, sender, message, conversation, flags):
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
        # This condition is here to check if I want to chat by myself, make class do
        # not answer me, and this will be helpful to avoid that endless loop of answer.
        # that bad bug I mean :D

    if purple.PurpleAccountGetUsername(account) != sender:
        purple.PurpleConvImSend(purple.PurpleConvIm(conversation), answer)

    
def main(message):
    # This signal function call and the line after that is here
    # to help me Quit after pressing 'Ctrl+C'
    import signal
    # After reciving signal.SIGINT or 'Ctrl+C' it has rights to kill main program.
    # I mean signal.SiG_DFL can be any function else that can call QApplication(quit);-)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication([])
    connect_dbus(message)
    app.exec_()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
        main(message)
    else:
        print "Usage: command YOUR_MESSAGE"

    
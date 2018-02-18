#!/usr/bin/python

# https://wiki.archlinux.org/index.php/Desktop_notifications
# Dependencies: libnotify, python-gobject (or python2-gobject for Python 2)

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

def show_message(subject, body):
    Notify.init(subject)
    Notify.Notification.new(subject, body, "dialog-information").show()

if __name__ == "__main__":
    show_message("subject", "body")

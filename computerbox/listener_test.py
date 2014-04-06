#!/usr/bin/python

# Say "THREE END" to switch to the news commands, and say "STOP READING
# HEADLINES" to switch back to the test commands.

import gobject
import pygst
pygst.require("0.10")
gobject.threads_init()
import gst

import signal
import time

import configuration
import listener

# I know---you want to import speaker and have TTS stuff here as well. Don't.
# GST does something thread-y that doesn't work well with pyttsx. Instead, use
# a producer/consumer pattern to have them do things in separate threads, as in
# the other files in this directory.

class TestListener(listener.CommandListener):
  def _EnqueueCommand(self, asr, text, uttid):
    print "Got command: %s" % text
    if text == self.trigger:
      self.Pause()
      self.other.Listen()

  def ConfigureSwitch(self, trigger, other):
    self.trigger = trigger
    self.other = other


def Initialize():
  test = TestListener("test")
  news = TestListener("news")
  test.ConfigureSwitch("THREE END", news)
  news.ConfigureSwitch("STOP READING HEADLINES", test)
  test.Listen()

Initialize()
print "Ready to go!"
signal.pause()  # Don't do anything unless prompted by the ASR.

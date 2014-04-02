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

# I know---you want to import speaker and have TTS stuff here as well. Don't.
# GST does something thread-y that doesn't work well with pyttsx. Instead, use
# a producer/consumer pattern to have them do things in separate threads, as in
# the other files in this directory.

pipeline = gst.parse_launch(
  #"gconfaudiosrc ! " +
  ("pulsesrc device=%s ! " % configuration.PULSESRC_NAME) +
  "audioconvert ! audioresample ! " +
  "vader name=vad auto-threshold=true ! pocketsphinx name=asr ! " +
  "fakesink")

def SwitchTo(name):
  print "Switching FSG and dictionary to %s..." % name
  filename = "%s/%s" % (configuration.DATA_DIR, name)
  asr = pipeline.get_by_name("asr")
  pipeline.set_state(gst.STATE_PAUSED)
  asr.set_property("configured", False)
  asr.set_property("fsg", "%s.fsg" % filename)
  asr.set_property("dict", "%s.dic" % filename)
  asr.set_property("configured", True)
  pipeline.set_state(gst.STATE_PLAYING)
  print "done switching!"

def AsrResult(asr, text, uttid):
  print "\nGot result: %s\n" % text
  #time.sleep(1)
  print "resuming..."
  if text == "STOP READING HEADLINES":
    SwitchTo("test")
  if text == "THREE END":
    SwitchTo("news")

def AsrPartialResult(asr, text, uttid):
  print "\nGot partial result: %s\n" % text

def Initialize():
  """Initialize the speech components"""
  filename = "%s/test" % configuration.DATA_DIR

  asr = pipeline.get_by_name("asr")
  asr.set_property("fsg", "%s.fsg" % filename)
  asr.set_property("dict", "%s.dic" % filename)
  asr.connect("result", AsrResult)
  #asr.connect("partial_result", AsrPartialResult)
  asr.set_property("configured", True)
  pipeline.set_state(gst.STATE_PLAYING)

Initialize()
signal.pause()  # Don't do anything unless prompted by the ASR.

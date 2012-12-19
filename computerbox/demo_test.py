#!/usr/bin/python

"""
If you run this with no arguments from the command line, it can recognize the
grammar
  (ONE|TWO|THREE) (STOP|END)
When you are done playing around with it, use control-C to quit.

If you run this with an argument, it will use the dictionary and FSG named by
that argument in the data directory. For example, running 
  demo_test.py test
is equivalent to running this with no arguments.
"""

import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

import signal
import sys

import configuration

# I know---you want to import speaker and have TTS stuff here as well. Don't.
# GST does something thread-y that doesn't work well with pyttsx. Instead, use
# a producer/consumer pattern to have them do things in separate threads, as in
# the other files in this directory.

pipeline = gst.parse_launch(
  "gconfaudiosrc ! audioconvert ! audioresample ! " +
  "vader name=vad auto-threshold=true ! pocketsphinx name=asr ! " +
  "fakesink")

def AsrResult(asr, text, uttid):
  """Forward result signals on the bus to the main thread."""
  print "\nGot result: %s\n" % text

def AsrPartialResult(asr, text, uttid):
  """Forward result signals on the bus to the main thread."""
  print "\nGot partial result: %s\n" % text

def Initialize():
  """Initialize the speech components"""
  if len(sys.argv) > 1:
    file = sys.argv[1]
  else:
    file = "test"
  filename = "%s/%s" % (configuration.DATA_DIR, file)

  asr = pipeline.get_by_name('asr')
  asr.set_property('fsg', "%s.fsg" % filename)
  asr.set_property('dict', "%s.dic" % filename)
  # Use a line like the following to test out an adapted model.
  # FMI on adapting PocketSphinx to your particular environment/voice, see
  # http://cmusphinx.sourceforge.net/wiki/tutorialadapt
  #asr.set_property(
  #    'hmm', "/home/alan/sphinx/sphinx_training/hub4wsj_sc_8kadapt")
  asr.connect('result', AsrResult)
  #asr.connect('partial_result', AsrPartialResult)
  asr.set_property('configured', True)

  pipeline.set_state(gst.STATE_PLAYING)

Initialize()
signal.pause()  # Don't do anything unless prompted by the ASR.

#!/usr/bin/python

"""
This defines the CommandListener class, which sets up a gstreamer pipeline and
PocketSphinx engine to recognize spoken phrases. Each CommandListener object
retains a queue of commands it has recognized the user spoke.

Member functions in this class to be used elsewhere:
- The constructor takes the name of a pair of .fsg and .dic files in the data
  directory, for PocketSphinx to recognize. The CommandListener will start
  paused (i.e., not listening).
- Listen() will start it listening
- Pause() will stop it listening
- AddCommand(phrase, value) will associate the text of the phrase with the given
  value, so that this value is returned later when the text is spoken. The
  intention here is that you can have easy-to-use values returned instead of
  having stringly typed variables running all over the place, but this is
  completely optional.
- HasCommand() indicates whether there is a command that has been recognized and
  is ready to be dequeued.
- GetCommand() and BlockingGetCommand() return the next command (one is
  nonblocking, the other is blocking). These commands are either values set with
  AddCommand(), or the raw text the person spoke. If there are no commands
  enqueued when GetCommand() is called, it returns None.
- ClearCommands() will remove any recognized commands that have been queued up
  waiting for a call to GetCommand().

We store received commands in a threadsafe queue because gstreamer does some
kind of crazy thread stuff that doesn't play well with pyttsx, and this way we
can asynchronously add and remove stuff from the command queue and pyttsx won't
throw a fit.
"""

import gobject
import pygst
pygst.require("0.10")
gobject.threads_init()
import gst

import Queue

import configuration
import time

VERBOSE = True

_in_use = False
_pipeline = gst.parse_launch(
    ("pulsesrc device=%s ! " % configuration.PULSESRC_NAME) +
    #"gconfaudiosrc ! " +
    "audioconvert ! audioresample ! " +
    "vader name=vad auto-threshold=true ! " +
    "pocketsphinx name=asr ! " +
    "fakesink")
_pipeline.set_state(gst.STATE_PAUSED)

class CommandListener(object):
  def __init__(self, name):
    self.command_queue = Queue.Queue()  # Must be threadsafe
    self.command_registry = {}  # Mapping from spoken phrases to return values
    # We need to store a member pointer to the global pipeline. Something about
    # the threadiness of gstreamer doesn't play well with global variables,
    # maybe?
    # TODO: try removing this when things are working more solidly.
    self.pipeline = _pipeline
    self.whole_filename = "%s/%s" % (configuration.DATA_DIR, name)

  def AddCommand(self, phrase, value):
    self.command_registry[phrase] = value

  def ClearCommands(self):
    # Making a new one is easier than clearing the old one.
    self.command_queue = Queue.Queue()

  def Listen(self):
    # TODO: replace this next line with a check to make sure the pipeline isn't
    # currently being used by another listener.
    self.pipeline.set_state(gst.STATE_PAUSED)
    asr = self.pipeline.get_by_name("asr")
    asr.set_property("configured", False)
    asr.set_property("fsg", "%s.fsg" % self.whole_filename)
    asr.set_property("dict", "%s.dic" % self.whole_filename)
    asr.connect("result", self._EnqueueCommand)
    asr.connect("partial_result", self._HandlePartialResult)
    asr.set_property("configured", True)
    time.sleep(1)
    self.pipeline.set_state(gst.STATE_PLAYING)
    if VERBOSE:
      print "Switched to new listener. Valid commands are:"
      for command in self.command_registry:
        print command

  def Pause(self):
    if VERBOSE:
      print "Turning listener off..."
    self.pipeline.set_state(gst.STATE_PAUSED)

  def HasCommand(self):
    return not self.command_queue.empty()

  def GetCommand(self):
    # If we try to dequeue something from an empty queue, the Empty exception is
    # raised. Consider using this in the future, but for now just return None
    # instead.
    if self.HasCommand():
      return self.command_queue.get()
    return None

  def BlockingGetCommand(self):
    return self.command_queue.get(True)  # True = block until ready

  def _HandlePartialResult(self, asr, text, uttid):
    if VERBOSE:
      print "Got partial result from pocketsphinx: %s" % text

  def _EnqueueCommand(self, asr, text, uttid):
    """
    This should only be called by the gstreamer pipeline when it recognizes
    spoken text.
    """
    if VERBOSE:
      print "Got command from pocketsphinx: %s" % text
    if text in self.command_registry:
      self.command_queue.put(self.command_registry[text])
    else:
      if len(self.command_registry) > 0:
        print ("WARNING: non-empty command registry does not contain current " +
            "command (%s)" % text)
      self.command_queue.put(text)

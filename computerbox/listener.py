#!/usr/bin/python

"""
This defines the CommandListener class, which sets up a gstreamer pipeline and
PocketSphinx engine to recognize spoken phrases. 

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
- GetCommand() and BlockingGetCommand() return the next command (one is
  nonblocking, the other is blocking). These commands are either values set with
  AddCommand(), or the raw text the person spoke. If there are no commands
  enqueued when GetCommand() is called, it returns None.

We store received commands in a threadsafe queue because gstreamer does some
kind of crazy thread stuff, and this way we can asynchronously add and remove
stuff from the command queue.
"""

import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

import Queue

import configuration

# TODO: remove this when I'm confident everything is working again
#file_base = "/Users/alandavidson/svn1/voice/pocketsphinx/data"

class CommandListener(object):
  def __init__(self, name):
    self.command_queue = Queue.Queue()  # Must be threadsafe
    self.command_registry = {}  # Mapping from spoken phrases to return values

    # TODO: change this so that most of this pipeline is shared among all
    # listeners. We don't need multiple audioresample steps, for instance.
    self.pipeline = gst.parse_launch(
        "gconfaudiosrc ! audioconvert ! audioresample ! " +
        "vader name=vad auto-threshold=true ! " +
        ("pocketsphinx name=%s ! " % name) +
        "fakesink")

    #whole_filename = "%s/%s" % (file_base, name)
    whole_filename = "%s/%s" % (configuration.DATA_DIR, name)
    asr = self.pipeline.get_by_name(name)
    asr.set_property('fsg', "%s.fsg" % whole_filename)
    asr.set_property('dict', "%s.dic" % whole_filename)
    asr.connect('result', self._EnqueueCommand)
    asr.set_property('configured', True)
    self.pipeline.set_state(gst.STATE_PAUSED)

  def AddCommand(self, phrase, value):
    self.command_registry[phrase] = value

  def ClearCommands(self):
    # Making a new one is easier than clearing the old one.
    self.command_queue = Queue.Queue()

  def Listen(self):
    self.pipeline.set_state(gst.STATE_PLAYING)

  def Pause(self):
    self.pipeline.set_state(gst.STATE_PAUSED)

  def HasCommand(self):
    return not self.command_queue.empty()

  def GetCommand(self):
    if self.HasCommand():
      return self.command_queue.get()
    return None

  def BlockingGetCommand(self):
    return self.command_queue.get(True)  # True = block until ready

  def _EnqueueCommand(self, asr, text, uttid):
    """
    This should only be called by the gstreamer pipeline when it recognizes
    spoken text.
    """
    if text in self.command_registry:
      self.command_queue.put(self.command_registry[text])
    else:
      if len(self.command_registry) > 0:
        print ("WARNING: non-empty command registry does not contain current " +
            "command (%s)" % text)
      self.command_queue.put(text)

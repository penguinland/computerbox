#!/usr/bin/python

"""
This file is the library for the text-to-speech capabilities. It requires pyttsx
to be installed. It also uses PRONUNCIATION_CORRECTIONS in configuration.py; and
if any words are mispronounced, add them there.

The functions from here to use elsewhere are:
 -  Acknowledge() is a way for the computer to indicate that it has done
    something. There are Mac- and nonMac-specific versions of this; look near
    the bottom to see where they're defined and change from using one to the
    other.
 - Speak(text) or Say(text) uses pyttsx to speak the text.
"""

import os
import pyttsx
import re
import subprocess
import time

import configuration

_engine = pyttsx.init()

def _CorrectPronunciation(word):
  """
  Given a word, returns either that same word or a phonetic version if the TTS
  engine is going to mispronounce it.
  """
  return configuration.PRONUNCIATION_CORRECTIONS.get(word.lower(), word)

def _HandleStartedUtterance(name):
  """Used only for debugging"""
  print "starting utterance: ->%s<-" % name

def _HandleStartedWord(name, loc, len):
  """Used only for debugging"""
  print ("starting word: ->%s<-\nlocation: %d, length: %d" %
         (name, loc, len))

def _HandleFinishedUtterance(name, len):
  """Used only for debugging"""
  print "finished utterance: ->%s<-\nlength: %d" % (name, len)

def _HandleError(name, exc):
  """Used only for debugging"""
  print "error in speech engine! name is ->%s<-" % name
  print "exception is %s" % exc
  raise exc

# The next four lines are useful for debugging problems.
"""
_engine.connect("started-utterance", _HandleStartedUtterance)
_engine.connect("started-word", _HandleStartedWord)
_engine.connect("finished-utterance", _HandleFinishedUtterance)
_engine.connect("error", _HandleError)
"""

def _PyttsSpeak(text):
  if re.search("[^a-zA-Z0-9#$%&()'\"/.,!?;:\t\n -]", text):
    print "erroneous text for speech engine:\n->%s<-" % text
    _engine.say(
        "Error: unpronounceable text passed to speech engine will cause it " +
        "to hang. The text has been printed to the screen for debugging " +
        "purposes.")
  else:
    _engine.say(text)
  _engine.runAndWait()

def _PicoSpeak(text):
  temp_file = "%s/tmp.wav" % configuration.NEWS_DIR
  p = subprocess.Popen('pico2wave -w %s "%s" && play %s && rm %s' %
                       (temp_file, text, temp_file, temp_file),
                       shell=True)
  # Wait until reading the text is finished before returning
  os.waitpid(p.pid, 0)

def Speak(text):
  # First, respell mispronounced words to be phonetic. Remove punctuation
  # before checking for corrected spelling. The regex is adapted from
  # http://stackoverflow.com/questions/367155
  pieces = re.findall(r"[\w']+|[^\w']+", text)
  corrected_words = [_CorrectPronunciation(word) for word in pieces]
  corrected_text = "".join(corrected_words)
  print corrected_text
  _PyttsSpeak(corrected_text)
  #_PicoSpeak(corrected_text)

Say = Speak  # Alternative name

def _TtsAcknowledge():
  Speak("acknowledged.")

def _MacAcknowledge():
  p = subprocess.Popen("afplay /System/Library/Sounds/Purr.aiff", shell=True)
  # The sound is half a second long, followed by half a second of silence.
  # Return during that silence, rather than waiting for the whole thing.
  time.sleep(0.5)

# For non-Mac users, change which of these is commented out.
Acknowledge = _MacAcknowledge
#Acknowledge = _TtsAcknowledge

if __name__ == "__main__":
  # Example tests
  Speak("hello world")
  Speak("This is working")
  Acknowledge()
  #Speak("@")  # Should return errors without hanging.
  #Speak("right \"...MPH!\"")  # says "right "...miles per hour!"

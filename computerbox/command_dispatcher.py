#!/usr/bin/python

import os
import sys
import time

import configuration
import listener
import read_news
import speaker
import speak_time
# TODO: add this back in when it's working again.
#import start_listening

def Unimplemented():
  speaker.Speak("This command is not yet implemented in the git "
                "hub version of this project. Ignoring command.")
  speaker.Acknowledge()

def WeatherForecast():
  f = open("%s/weather.txt" % configuration.NEWS_DIR)
  forecast = f.read()
  f.close()
  speaker.Speak(forecast)

def Sleep():
  """
  We cannot actually sleep while gst is running, so exit with a nonstandard
  return code, and our calling program will know to go to sleep.
  """
  speaker.Acknowledge()
  sys.exit(3)

def ExecuteCommand():
  print "getting command to execute..."
  speaker.Acknowledge()
  print "acknowledged"
  cl.ClearCommands()
  print "cleared commands"
  cl.Listen()
  print "listening..."
  cmd = cl.BlockingGetCommand()
  print "got command: %s" % cmd
  cl.Pause()
  time.sleep(0.25)  # Don't cut the human off; it's rude.
  cmd()

def WakeUp():
  """
  This is a perpetual loop that waits for the phrase "oh computerbox" and then
  calls ExecuteCommand().
  """
  waker.Listen()
  while True:
    print "back in main while loop..."
    cmd = waker.BlockingGetCommand()
    if cmd == LISTEN:
      print "listening for command!"
      waker.Pause()
      ExecuteCommand()
      time.sleep(1)  # Avoid a race condition in gst?
      waker.Listen()
    elif cmd == UNKNOWN:
      print "ingoring noise."
      pass  # Ignore it.
    else:
      speaker.Speak("Unexpected command! " +
                    "Something is very wrong in the main loop.")

UNKNOWN = 10
LISTEN = 11

# The waker is the thing that listens for the phrase "oh computerbox" and gets
# the system ready to receive a command, while ignoring all other noise.
waker = listener.CommandListener("ohcomputer")
waker.AddCommand("UNK", UNKNOWN)
waker.AddCommand("OH COMPUTER BOX", LISTEN)

# This is the thing that deals with all the different commands you might give
# after saying "oh computerbox." It maps phrases we might hear to nullary
# functions to execute.
cl = listener.CommandListener("command")
cl.AddCommand("READ ME SCIENCE HEADLINES", read_news.ReadScienceNews)
cl.AddCommand("READ ME YOU ESS HEADLINES", read_news.ReadUSNews)
cl.AddCommand("READ ME WORLD HEADLINES", read_news.ReadWorldNews)
cl.AddCommand("READ ME ALL HEADLINES", read_news.ReadAllNews)
cl.AddCommand("READ ME SCIENCE NEWS", read_news.ReadScienceNews)
cl.AddCommand("READ ME YOU ESS NEWS", read_news.ReadUSNews)
cl.AddCommand("READ ME WORLD NEWS", read_news.ReadWorldNews)
cl.AddCommand("READ ME ALL NEWS", read_news.ReadAllNews)
cl.AddCommand("WEATHER REPORT", WeatherForecast)
cl.AddCommand("WEATHER FORECAST", WeatherForecast)
cl.AddCommand("NEVER MIND", speaker.Acknowledge)
cl.AddCommand("GO TO SLEEP", Unimplemented)  # Sleep)
cl.AddCommand("STOP LISTENING", Unimplemented)  # start_listening.DontListen)
cl.AddCommand("WHAT TIME IS IT", speak_time.SpeakTime)

if __name__ == "__main__":
  WakeUp()

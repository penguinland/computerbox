#!/usr/bin/python

import configuration
import listener
import speaker
import time

READ = 1
PREV = 2
STOP = 3

cl = listener.CommandListener("news")
cl.AddCommand("READ ME THAT ONE", READ)
cl.AddCommand("READ ME PREVIOUS ONE", PREV)
cl.AddCommand("READ ME THE PREVIOUS ONE", PREV)
cl.AddCommand("STOP READING HEADLINES", STOP)
cl.AddCommand("STOP READING NEWS", STOP)

def _ReadNews(stories):
  speaker.Acknowledge()
  # We need a for loop over all the stories, except sometimes we want to go
  # backwards one. So, make it a while loop.
  i = 0
  while i < len(stories):
    story = stories[i]
    print "headline: %s" % story.headline
    speaker.Speak(story.headline)
    cl.ClearCommands()
    cl.Listen()
    time.sleep(3)
    cl.Pause()
    if cl.HasCommand():
      cmd = cl.GetCommand()
      print "Got command: %s" % cmd
      if cmd == STOP:
        print "stopping..."
        speaker.Acknowledge()
        return
      elif cmd == READ:
        print "reading story..."
        speaker.Acknowledge()
        _ReadArticle(story)
      elif cmd == PREV:
        print "reading previous story..."
        if i > 0:
          speaker.Acknowledge()
          _ReadArticle(stories[i-1])
          i -= 1  # Maybe read the current one as well as the previous one...
        else:
          speaker.Speak("Warning. No previous article to read. Skipping.")
      else:
        print "unrecognized command: %s" % cmd
        speaker.Speak("Warning: unrecognized command (%s). Ignoring." % cmd)
    i += 1
  speaker.Speak("No more headlines.")

def _ReadArticle(story):
  print story.location
  f = open(story.location)
  contents = f.read()
  f.close()
  if len(contents) == 0:
    speaker.Speak("Article has no contents.")
  else:
    print "Speaking contents:"
    #print contents
    speaker.Speak(contents)
  time.sleep(1)  # Pause at the end of the article
  speaker.Speak("Resuming Headlines.")
  time.sleep(0.5)

class _Story(object):
  def __init__(self, headline, location):
    self.headline = headline
    self.location = location

def _GetHeadlinesFromFile(filename):
  try:
    f = open("%s/%s.txt" % (configuration.NEWS_DIR, filename))
  except IOError:
    speaker.Speak("Error. Cannot find headline list.")
    return []
  story_descriptions = [line for line in f]
  f.close()
  stories = []
  for descr in story_descriptions:
    location = "%s/%s.txt" % (configuration.NEWS_DIR, descr.split()[-1])
    headline = " ".join(descr.split()[:-1])
    stories.append(_Story(headline, location))
  return stories

def _ReadNewsFromFile(filename):
  _ReadNews(_GetHeadlinesFromFile(filename))

def ReadScienceNews():
  _ReadNewsFromFile("sci")

def ReadUSNews():
  _ReadNewsFromFile("us")

def ReadWorldNews():
  _ReadNewsFromFile("world")

def ReadAllNews():
  _ReadNewsFromFile("all")

if __name__ == "__main__":
  ReadAllNews()

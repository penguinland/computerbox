#!/usr/bin/python

"""
SpeakTime() does what it says: it speaks the current time, rounded to the
nearest 5 minutes and made more human-friendly a la the fuzzy clock in KDE.
"""

import random
import time

import speaker

def _RoundToFive(m):
  """Rounds m to the nearest multiple of 5"""
  d = m / 5
  r = m % 5
  if r >= 3:
    d += 1
  return d * 5

def _GetNumericalTime():
  t = time.localtime()
  h = t.tm_hour
  m = t.tm_min
  m = _RoundToFive(m)
  if m == 60:
    h += 1
    m = 0
  if h == 24:
    h = 0
  return (h, m)

def _FormatMinute(h, m):
  # We don't use the h argument; it's included for consistency with _FormatHour
  options = ["%s o'clock",
             "five past %s",
             "ten past %s",
             "a quarter past %s",
             "twenty past %s",
             "twenty five past %s",
             "half past %s",
             "twenty five to %s",
             "twenty to %s",
             "a quarter to %s",
             "ten to %s",
             "five to %s"]
  return options[m / 5]

def _FormatHour(h, m):
  """Returns the nearest hour"""
  if m <= 30:
    if h == 0:
      return "midnight"
    if h == 12:
      return "noon"
    return h
  # If we get this far, we're closer to the next hour than the previous one.
  if h == 23:
    return "midnight"
  if h == 11:
    return "noon"
  return h + 1

def SpeakTime():
  # Easter eggs!
  choice = random.random()
  if choice < 0.02:
    speaker.Speak("adventure time!")
  #elif choice < 0.04:
  #  speaker.Speak("shirtless o'clock!")
  else:
    # Actually give the time
    (h, m) = _GetNumericalTime()  # 24 hour time, rounded to the nearest 5 min.
    minute_text = _FormatMinute(h, m)
    hour_text = _FormatHour(h, m)
    text = minute_text % hour_text

    # Special cases:
    if h == 12 and m == 0:
      text = "noon"
    if h == 0 and m == 0:
      text = "midnight"

    speaker.Speak(text)

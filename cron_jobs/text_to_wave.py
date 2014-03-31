#!/usr/bin/python

import os
import subprocess
import sys

def Convert(filename, text):
  wav_file = "%s.wav" % filename[:-4]
  p = subprocess.Popen('pico2wave -w %s "%s"' % (wav_file, text), shell=True)
  os.waitpid(p.pid, 0)  # Don't return until the file is written.

if __name__ == "__main__":
  filename = sys.argv[-1]
  f = open(filename)
  text = f.read()
  f.close()
  Convert(filename, text)
  command = "play %s.wav" % filename[:-4]
  print command
  subprocess.Popen(command, shell=True)

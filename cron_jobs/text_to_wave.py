#!/usr/bin/python

import subprocess

def Convert(filename, text):
  wav_file = "%s.wav" % filename[:-4]
  subprocess.Popen('pico2wave -w %s "%s"' % (wav_file, text), shell=True)

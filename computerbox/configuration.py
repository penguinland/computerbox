"""
This file is for constants that get used in other places. This way, there's only
one file you need to modify.
"""

# The path to the directory containing the .fsg files for speech recognition.
# This is probably the data directory in the same location as this file. Due to
# a quirk in PocketSphinx that I haven't worked out yet, it appears that this
# needs to be fully specified; you can't use a tilde for your home directory.
DATA_DIR = "/Users/alandavidson/computerbox/computerbox/data"

# A mapping from mispronounced lowercased words to phonetic versions. Comments
# are phonetic versions of the default pronunciation, to explain why the word
# was added here.
PRONUNCIATION_CORRECTIONS = {
  "edt" : "eastern time",  # ee dee tee
  "fla" : "Florida",  # flah
  "gif" : "giff",  # Gee Ai Eff
  "gui" : "gooey",  # Gee You Ai
  "qty" : "quantity",  # tai
  "mpg" : "miles per gallon",  # em pee gee
  "mph" : "miles per hour",  # em pee aitch
  "mr" : "mister",  # em arr
  "ms" : "miss",  # em ess
  "mrs" : "misses",  # em arr es
  "jr" : "junior",  # jay arr
  "sr" : "senior",  # ess arr
  "sen" : "senator",  # sen
  "syria" : "seerya", # surria
  "sc" : "south carolina",  # ess see
  }


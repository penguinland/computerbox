"""
This file is for constants that get used in other places. This way, there's only
one file you need to modify.
"""

LINUX = 11
MAC_OSX = 12

# Change the following line to your operating system.
CURRENT_OS = LINUX

# The path to the root directory of the git repository. Probably the parent of
# the directory that this file is in. Due to a quirk in PocketSphinx that I
# haven't figured out yet, it appears that this needs to be fully specified; you
# can't use a tilde for your home directory.
ROOT_DIR = "/home/alan/computerbox"

# The directory where .fsg and .dic files are stored
DATA_DIR = "%s/computerbox/data" % ROOT_DIR
# The directory where news articles are written by the cron jobs.
NEWS_DIR = "%s/cron_jobs/news_articles" % ROOT_DIR

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


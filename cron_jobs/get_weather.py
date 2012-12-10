#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import urllib

import configuration

directory = "/Users/alandavidson/computerbox/cron_jobs/news_articles"

def _SoupToText(soup):
  period = soup("div", "titleSubtle")[0].get_text()  # ex: Tonight, Tomorrow
  temperature = soup("div", "foreSummary")[0].get_text()
  # This next line uses contents()[0] instead of get_text() to get rid of the
  # part about 20% chance of rain or whatever.
  conditions = soup("div", "foreCondition")[0].contents[0]
  extremum = "high"
  if "ight" in period:  # Tonight, tomorrow night, etc.
    extremum = "low"
  text = ("%s will be %s with a %s of %s" %
          (period, conditions, extremum, temperature))
  text = re.sub(unichr(0xb0) + "F", "degrees.", text)
  return re.sub(r"\s+", " ", text)

def GetWeather():
  f = urllib.urlopen(configuration.WEATHER_URL)
  xml = f.read()
  f.close()

  soup = BeautifulSoup(xml)
  forecast = soup.find_all("div", "foreGlance")

  f = open("%s/%s" % (configuration.CACHE_DIR, "weather.txt"), "w")
  f.write(_SoupToText(forecast[0]))
  f.write(_SoupToText(forecast[1]))
  f.close()

if __name__ == "__main__":
  GetWeather()

#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import urllib

import configuration

def _SoupToText(soup):
  period = soup("div", "titleSubtle")[0].get_text()  # ex: Tonight, Tomorrow
  temperature = soup("div", "foreSummary")[0].get_text()
  # This next line uses contents()[0] instead of get_text() to get rid of the
  # part about 20% chance of rain or whatever.
  conditions = soup("div", "foreCondition")[0].contents[0]
  conditions = conditions.replace("T-storms", "thunderstorms")
  extremum = "high"
  if "ight" in period:  # Tonight, tomorrow night, etc.
    extremum = "low"
  text = ("%s will be %s with a %s of %s. " %
          (period, conditions, extremum, temperature))
  text = re.sub(unichr(0xb0) + r"F\s*", "degrees", text)
  return re.sub(r"\s+", " ", text)

def GetWeather():
  f = urllib.urlopen(configuration.WEATHER_URL)
  xml = f.read()
  f.close()

  soup = BeautifulSoup(xml)
  forecast = soup.find_all("div", "foreGlance")
  forecast_text = "%s %s" % (_SoupToText(forecast[0]),
                             _SoupToText(forecast[1]))

  filename = "%s/weather.txt" % configuration.NEWS_DIR
  f = open(filename, "w")
  f.write(forecast_text)
  f.write("")  # End with a newline to make debugging easier
  f.close()

if __name__ == "__main__":
  GetWeather()

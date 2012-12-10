#!/usr/bin/python

CACHE_DIR = "/Users/alandavidson/computerbox/cron_jobs/news_articles"

# Your ZIP code for weather forecasts
ZIP_CODE = 27705
# I'm aware that the Weather Underground has RSS feeds such as
#   http://rss.wunderground.com/auto/rss_full/NC/Durham.xml?units=english
# However, they're (surprisingly) not nearly as parseable as their main website
# is. For ease of coding here, I'm going for the main site.
WEATHER_URL = ("http://www.wunderground.com/cgi-bin/findweather/hdfForecast?"
               "query=%s" % ZIP_CODE)

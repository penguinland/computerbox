#!/usr/bin/python

"""
This file should be run as a cron job. It gets news articles from the Google
News RSS feeds and uses article_to_text.py to extract the text, then saves that
text and some "table of contents" text files into the news_articles directories.
"""

# To get rid of old files, try this;
# find /path/to/files* -mtime +7 -exec rm {} \;
# The 7 takes out anything over a week old. Note the spaces after rm and {}

import hashlib
import re
import socket
import urllib
import article_to_text

scitech = "http://news.google.com/news?ned=us&topic=t&output=rss"
us = "http://news.google.com/news?ned=us&topic=n&output=rss"
world = "http://news.google.com/news?ned=us&topic=w&output=rss"
# Add more RSS feeds if desired

# TODO: set this to some global path when this is installed on the computer it
# should be run on.
directory = "/Users/alandavidson/computerbox/cron_jobs/news_articles"

# TODO: We get an IOError when the socket times out; handle that correctly.
socket.setdefaulttimeout(10)  # timeout in seconds

def ParseArticleRSS(xml):
  """
  Takes an XML entry from an RSS feed; returns a (headline, URL) pair
  """
  xml = xml.replace("&apos;", "'")
  xml = xml.replace("&quot;", " quote ")
  #print xml
  article_match = re.search("<title>(.*) - (.*)</title>", xml)
  title = article_match.group(1)
  paper = article_match.group(2).replace(".", " dot ")
  full_title = "%s, by %s" % (title, paper)
  url = re.search("<link>.*&amp;url=(.*)</link>", xml).group(1)
  return (full_title, url)

def GetArticles(rss):
  """
  Takes a URL of an RSS feed; returns a list of (headline, newspaper name, URL)
  tuples.
  """
  f = urllib.urlopen(rss)
  xml = f.read()
  f.close()
  xml = xml.replace("\n", " ")
  article_matches = re.finditer("<item>(.*?)</item>", xml)
  return [ParseArticleRSS(piece.group(1)) for piece in article_matches]

def GetArticleText(url, filename):
  """
  Takes a URL of a news article; stores the text of that article in the filename
  in the news_articles directory.
  """
  # TODO: don't bother overwriting if the file already exists.
  text = article_to_text.FormatArticle(url)
  # TODO: if the article is empty or is 1 line long with the phrase "access
  # denied" in it, don't bother adding it to the index directory.
  # TODO: figure out why I sometimes get empty articles or "access denied"
  # errors. These sites work perfectly fine in Firefox when I disable cookies,
  # javascript, and flash; what is different between that and my downloader?
  article_file = open("%s/%s.txt" % (directory, filename), "w")
  # TODO: if the last line of the article is less than 80 characters long and
  # contains an @ symbol, don't write it out, because it's just the contact
  # info of the editors or whatever.
  article_file.write(text)
  article_file.close()

def StoreArticle(article_tuple, file):
  """
  Takes a (headline, URL) pair and a file opened for writing.
  This hashes the headline and newspaper name to a variable called file_hash,
  and then:
   - puts the text of the article in directory/file_hash.txt
   - writes this record to the file.
  """
  title = article_tuple[0]
  url = article_tuple[1]

  file_hash = hashlib.sha224(title).hexdigest()

  GetArticleText(url, file_hash)
  file.write("%s\t%s\n" % (title, file_hash))

def StoreArticles(article_list, filename):
  """
  Takes a list of article tuples and a filename; downloads the spoken headlines
  and text of the articles, saves them, and puts an index file in filename.
  """
  file = open("%s/%s.txt" % (directory, filename), "w")
  for article in article_list:
    StoreArticle(article, file)
  file.close()

if __name__ == "__main__":
  print "getting science articles..."
  sci_results = GetArticles(scitech)
  StoreArticles(sci_results, "sci")
  print "getting us articles..."
  us_results = GetArticles(us)
  StoreArticles(us_results, "us")
  print "getting world articles..."
  world_results = GetArticles(world)
  StoreArticles(world_results, "world")
  print "getting all articles..."
  results = []
  results.extend(sci_results)
  results.extend(us_results)
  results.extend(world_results)
  StoreArticles(results, "all")
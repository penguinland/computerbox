#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import readability
import urllib

def _StripTag(html, tag):
  """
  Returns the html but with all instances of <tag> or </tag> removed (text in
  between tags remains).
  """
  return re.sub("</?%s[^>]*>" % tag, "", html)

def ExtractText(html):
  """
  Takes HTML of an article; returns the text of the article.
  """
  # TODO: readability is mangling some HTML-encoded unicode, such as &#151;.
  # Figure out why and how to fix it.
  doc = readability.Document(html)
  better_html = doc.summary(False)  # False means don't wrap it in HTML

  # Remove all tables, including nested tables.
  soup = BeautifulSoup(better_html)
  tags_to_remove = ["table", "tr", "td", "th", "figure", "noscript", "cite",
                    "link", "br", "img"]
  for tag in tags_to_remove:
    for subtree in soup.findAll(tag):
      subtree.extract()
  # Also remove paragraphs that are nothing but a single giant link, since they
  # tend to be "related" headlines that aren't part of the actual article.
  for subtree in soup.findAll("p"):
    if len(subtree.contents) == 1:
      p_contents = subtree.contents[0]
      try:
        if p_contents.name == "a":
          subtree.extract()
      except AttributeError:
        # p_contents was text, rather than more HTML.
        pass
  better_html = soup.prettify()  # cast it back to a string

  better_html = better_html.replace("\n", " ")
  better_html = better_html.replace("\t", " ")

  # Remove headers
  for i in range(1, 8):
    better_html = _StripTag(better_html, "h%d" % i)
  # Remove other text modification tags
  tags_to_strip = ["a", "b", "i", "strong", "span", "em", "ul", "ol", "li",
                   "font", "html", "body"]
  for tag in tags_to_strip:
    better_html = _StripTag(better_html, tag)

  better_html = re.sub("<!--((?!-->)(\\n|.))*-->", "", better_html)

  better_html = better_html.replace("&#91;", "[")
  better_html = better_html.replace("&#93;", "]")

  dashes = ["&ndash;", "&#151;", "&#x2014;", "&#8212;", "&mdash;"]
  for dash in dashes:
    better_html = better_html.replace(dash, " --- ")

  quotes = ["&quot;", "&raquot;", "\"", "&rdquot;", "&#8221;", "&#8220;",
            "&ldquot;", "&ldquo;", "&rdquo;", 
            unichr(0x201c).encode("UTF-8"), unichr(0x201d).encode("UTF-8")]
  for quote in quotes:
    # Put the quote on the other side of a period/comma if it's at the end of a
    # sentence, so that the pause is in the right place.
    better_html = re.sub(r"([,.!]?)%s" % quote, r" quote\1 ", better_html)

  # Currency conversion
  money_suffixes = ["hundred", "thousand", "million", "billion", "trillion"]
  suffix_re = "".join(["( %ss?)*" % suffix for suffix in money_suffixes])
  better_html = re.sub(r"\$([0-9,.]*[0-9]%s)" % suffix_re, r"\1 dollars",
      better_html)
  better_html = re.sub(r"\&pound;([0-9,.]*[0-9]%s)" % suffix_re,
      r"\1 pounds sterling", better_html)

  # Don't pronounce US as "us"
  better_html = better_html.replace(" US ", " you ess ")

  better_html = better_html.replace("&#8230;", "... ")  # ellipsis
  better_html = better_html.replace("&#039;", "'")  # apostrophe
  better_html = better_html.replace("&#39;", "'")  # apostrophe
  better_html = better_html.replace("&#8217;", "'")  # apostrophe
  better_html = better_html.replace("&rsquo;", "'")
  better_html = better_html.replace("&amp;", "&")
  better_html = better_html.replace("&copy;", " copyright ")
  better_html = better_html.replace("&nbsp;", " ")
  better_html = better_html.replace("&#160;", " ")  # ?
  better_html = better_html.replace("&#13;", "")  # noncoding ASCII character?

  # These lines are straight non-regex replacement, but string.replace doesn't
  # play well with unicode.
  better_html = re.sub(unichr(0x2026).encode("UTF-8"), "... ", better_html)
  better_html = re.sub(unichr(0x2013).encode("UTF-8"), " - ", better_html)
  better_html = re.sub(unichr(0x2014).encode("UTF-8"), " - ", better_html)
  better_html = re.sub(unichr(0x151).encode("UTF-8"), " - ", better_html)
  better_html = re.sub("\xc3\x82\xc2\x97", " - ", better_html)

  # TODO: remove unknown &#...;'s when I'm confident I have all the important
  # ones.

  # Strip out empty and useless HTML tags. Note that this repeats to
  # convergence, so that we can get rid of things like <a><b></b></a>
  next_html = re.sub(r"<(\w*)( [^>]*)?> *</\1>", "", better_html)
  next_html = re.sub(r"<(\w*)( [^>]*)?/>", "", next_html)
  next_html = re.sub("\s+", " ", next_html)
  while next_html != better_html:  # more empty tags to strip out
    better_html = next_html
    next_html = re.sub(r"<(\w*)( [^>]*)?>\s*</\1>", "", better_html)
    next_html = re.sub(r"<(\w*)( [^>]*)?/>", "", next_html)
    next_html = re.sub("\s+", " ", next_html)

  # <div> tags are tricky: sometimes they contain junk to remove, and sometimes
  # they contain article text that we want to keep. The class name for the ones
  # that contain article text is often human-readable, but not standardized and
  # varies widely from website to website. Instead of figuring that out, I'm
  # just going to remove any <div> tags whose body is too small. Again, I will
  # repeat until convergence, so that we can get rid of stuff like
  # <div><div>April 3, New York</div></div>
  min_div_size = 100  # Characters required for a <div> to be worth keeping

  soup = BeautifulSoup(better_html)
  iterate_again = True
  while iterate_again:
    iterate_again = False
    for subtree in soup.findAll("div"):
      if len(subtree.text) < min_div_size:
        subtree.extract()
        iterate_again = True
  #better_html = "%s" % soup  # cast it back to a string
  better_html = soup.prettify()  # cast it back to a string

  # Get rid of the <html> and <body> tags that BeautifulSoup adds in again, and
  # strip out any remaining <div>'s (which presumably encapsulate the article
  # itself).
  tags_to_strip = ["div", "html", "body"]
  for tag in tags_to_strip:
    better_html = _StripTag(better_html, tag)

  better_html = better_html.replace("[", "")
  better_html = better_html.replace("]", "")

  # Finally, turn <p> tags into actual paragraphs. This part should go last,
  # because other replacement stuff can't deal with newlines correctly.
  better_html = better_html.replace("</p>", "")
  text = re.sub("(<p( [^>]*)?>)+", "\n\n", better_html)
  # Get rid of extra whitespace, for ease of debugging output
  text = re.sub("\s*\n\s*\n\s*", "\n\n", text)
  text = re.sub(" +", " ", text)

  # NOTE: if you want to improve this function, comment out the next two lines
  # to make debugging easier.

  # If there are any crazy Unicode characters left, try to convert them to ASCII
  # equivalents.
  #text = text.encode("ASCII", "replace")
  # As a last resort, remove any remaining non-speakable characters.
  text = re.sub("[^a-zA-Z0-9#$%&()'/.,!?;:\t\n -]", "", text)

  # Make sure to end with a newline, to format things better.
  if len(text) > 0 and text[-1] != "\n":
    text = "%s\n" % text
  return text

def FormatArticle(url):
  """
  Takes a URL; returns the text of the article.
  """
  # TODO: find a way to detect articles that span multiple pages, and aggregate
  # all pages together. It might help to take the HTML of the first page, look
  # for a "print this page" link, and grab the HTML from _that_ page for
  # processing.

  # TODO: put this in a try block and return early if it throws an IOError
  # because the socket timed out.
  html = urllib.urlopen(url).read()
  return ExtractText(html)

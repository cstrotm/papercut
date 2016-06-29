# Copyright (c) 2002 Joao Prado Maia. See the LICENSE file for more information.
import time
import re

singleline_regexp = re.compile("^\.", re.M)

def wrap(text, width=78):
    """Wraps text at a specified width.
        
    This is used on the PhorumMail feature, as to emulate completely the
    current Phorum behavior when it sends out copies of the posted
    articles.
    """
    i = 0
    while i < len(text):
        if i + width + 1 > len(text):
            i = len(text)
        else:
            findnl = text.find('\n', i)
            findspc = text.rfind(' ', i, i+width+1)
            if findspc != -1:
                if findnl != -1 and findnl < findspc:
                    i = findnl + 1
                else:
                    text = text[:findspc] + '\n' + text[findspc+1:]
                    i = findspc + 1
            else:
                findspc = text.find(' ', i)
                if findspc != -1:
                    text = text[:findspc] + '\n' + text[findspc+1:]
                    i = findspc + 1
    return text

def get_formatted_time(time_tuple):
    """Formats the time tuple in a NNTP friendly way.
    
    Some newsreaders didn't like the date format being sent using leading
    zeros on the days, so we needed to hack our own little format.
    """
    # days without leading zeros, please
    day = int(time.strftime('%d', time_tuple))
    tmp1 = time.strftime('%a,', time_tuple)
    tmp2 = time.strftime('%b %Y %H:%M:%S %Z', time_tuple)
    return "%s %s %s" % (tmp1, day, tmp2)

def format_body(text):
    """Formats the body of message being sent to the client.
    
    Since the NNTP protocol uses a single dot on a line to denote the end
    of the response, we need to substitute all leading dots on the body of
    the message with two dots.
    """
    return singleline_regexp.sub("..", text)

def format_wildcards(pattern):
    return pattern.replace('*', '.*').replace('?', '.*')

def format_wildcards_sql(pattern):
    return pattern.replace('*', '%').replace('?', '%')

def filterchars(text, characters):
    '''Reduces string text to the characters found in string characters'''
    res = ''
    for char in text:
        if char in characters:
            res += char

    return res


class ReadlineWrapper:
  '''
  Provides a readline() method for a string (This allows rfc822.Message to
  be used on plain strings)
  '''

  def __init__(self, text):
    if isinstance(text, list):
      self.lines = text
    elif isinstance(text, str):
      self.lines = text.split("\n")
    else:
      raise TypeError('text must be string or a list of lines')
    self.i = 0

  def readline(self, size=-1):
    if ( self.i < len(self.lines) ):
      if ( size > 0 ):
        ret = self.lines[self.i]
      else:
        ret = self.lines[self.i][:size-1]
    else:
      ret = ''
    self.i += 1
    return ret

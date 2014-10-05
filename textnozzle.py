#!/usr/bin/env python

import re, string

chunk_size = 1024
class TextNozzle:
  def __init__(self, source):
    self.source = source
    self.char_queue = []
    self.pattern = re.compile('[\W_]+')
    self.open_file()

  def open_file(self):
    self.fh = open(self.source, 'r')

  def read_from_queue(self):
    self.check_queue()
    return self.char_queue.pop(0)

  def get_char(self, v):
    if v == 0:
      return " "
    self.check_queue()
    char = self.read_from_queue()
    while not char.isalpha():
      char = self.read_from_queue()
    return char
  
  def check_queue(self):
    if len(self.char_queue) == 0:
      self.recharge_queue()
    
  def recharge_queue(self):
    data = self.fh.read(chunk_size)
    if data == "":
      self.open_file()
      data = self.fh.read(chunk_size)
    self.char_queue = list(data)

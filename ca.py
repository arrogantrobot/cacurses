#!/usr/bin/env python

class ca:
  def __init__(self, width):
    self.width = width
    self.reset()
    self.rule = 129
    self.mask = [1, 2, 4, 8, 16, 32, 64, 128]

  def reset(self):
    self.cells = [0 for n in range(self.width)]
    self.cells[int(self.width/2)] = 1
  
  def get_next(self):
    self.iterate()
    return self.cells

  def set_rule(self, rule):
    self.rule = rule

  def get_rule(self):
    return self.rule
  
  def increment_rule(self):
    self.rule = (self.rule + 1) % 255

  def decrement_rule(self):
    self.rule = (self.rule - 1) % 255

  def iterate(self):
    nxt = []
    for n in range(len(self.cells)):
      nxt.append(self.get_cell(n))
    s = sum(nxt)
    if s == 0 or s == len(nxt):
      self.reset
    else:
      self.cells = nxt

  def get_cell(self, n):
    index = 0
    if n == 0:
      if self.cells[self.width - 1] == 1:
        index += 1
    else:
      if self.cells[n - 1] == 1:
        index += 1
    if self.cells[n] == 1:
      index += 2
    if n == self.width - 1:
      if self.cells[0] == 1:
        index += 4
    else:
      if self.cells[n + 1] == 1:
        index += 4
    val = 0
    if (self.rule & self.mask[index]) > 0:
      val = 1
    return val

#!/usr/bin/env python
# encoding: utf-8

import os
import sys


def searchFlacs(top):
  for root, dirs, files in os.walk(top):
    #check if there are flacs in this folder
    flacs = False
    for name in files:
      if name.endswith((".flac")):
        flacs = True
        break
    if flacs:
      print root + " ::"
    for name in files:
      if name.endswith((".flac")):
        print "  - " +name


if __name__ == '__main__':
  assert len(sys.argv) >= 2, 'Please specify an input folder!'

  root_dir = sys.argv[1]

  searchFlacs(root_dir)



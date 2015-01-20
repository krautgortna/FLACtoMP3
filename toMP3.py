#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import subprocess
import time
from multiprocessing import Pool
from multiprocessing import Process

global root_dir

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def searchFlacs(top):
  flacs = []
  print "Found:"
  for root, dirs, files in os.walk(top):
    #check if there are flacs in this folder
    flacsfound = False
    for name in files:
      if name.endswith((".flac")):
        flacsfound = True
        break
    if flacsfound:
      print root + " ::"
    for name in files:
      if name.endswith((".flac")):
        print "  - " + name
        flacs.append((root, name))
  return flacs
        
def convert(files):
  FNULL = open('log.txt', 'w')
  for dir, file in files:
      oldfile = os.path.join(dir, file)
      newfile = oldfile.replace(".flac", ".mp3")  
      #print "Processing: " + oldfile.replace(root_dir, '')
      try:
        '''
        output = subprocess.Popen(["ffmpeg", "-n", "-i", oldfile, "-qscale:a", "0", newfile], stdout=subprocess.PIPE).communicate()[0]
        #output = subprocess.Popen(["ffmpeg", "-n", "-i", oldfile, "-qscale:a", "0", newfile], stdout=None).communicate()[0]        
        with open('log.txt', 'w') as logfile:
          logfile.write(output)
        '''
        start = time.time()
        retcode = subprocess.call(["ffmpeg", "-n", "-i", oldfile, "-qscale:a", "0", newfile], stdout=FNULL, stderr=subprocess.STDOUT)
        elapsed = time.time() - start
        if os.path.isfile(newfile):
            print "Processed: " + oldfile.replace(root_dir, ''),
            print bcolors.OKBLUE + "   ... in %s s" % (round(elapsed, 3)) + bcolors.ENDC
        else:
            print "Processed: " + oldfile.replace(root_dir, ''),
            print bcolors.FAIL + "\n   ...ERROR occured! Check log.txt for details!" + bcolors.ENDC

      except OSError:
        print "Error starting ffmpeg. Did you install ffmpeg and add it to your PATH?"
        print ""
        raise

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


if __name__ == '__main__':
  assert len(sys.argv) >= 2, 'Please specify an input folder!'

  root_dir = sys.argv[1]
  
  start_overall = time.time()

  files = searchFlacs(root_dir)
  #convert(files, root_dir)
  files_chunks = list(chunks(files, len(files)/5))

  jobs = []
  for chunk in files_chunks:
    p = Process(target=convert, args=(chunk,))
    jobs.append(p)
    p.start()

  elapsed_overall = time.time() - start_overall
  
  print bcolors.BOLD + "Processed all files in %s s" % (round(elapsed_overall, 3)) + bcolors.ENDC



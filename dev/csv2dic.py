#!/usr/bin/env python

# Used for parsing jh_dict_unicode.csv

import argparse
import codecs
import csv
import os

def main():
  # Argument parsing
  parser = argparse.ArgumentParser(prog='csv2dic', description='Converts csv file to corpus dic format.')
  parser.add_argument('path')
  args = parser.parse_args()

  if not os.path.exists(args.path):
    print "Error: path '" + args.path + "' does not exist"
    os._exit(1)
    
  if (os.path.isfile(args.path)):
    processCsv(args.path)
  else:
    print "Error: path '" + args.path + "' is not a file"
    os._exit(1)

def processCsv(path):
  if not os.path.exists(path):
    print "Error: path '" + path + "' does not exist"
    os._exit(1)

  print os.path.splitext(os.path.abspath(path))[0]
  wyliefile = open(os.path.splitext(os.path.abspath(path))[0] + ".wylie", "w")
  bodfile = open(os.path.splitext(os.path.abspath(path))[0] + ".bod", "w")    
  enfile = open(os.path.splitext(os.path.abspath(path))[0] + ".en", "w")
  
  with open(path) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
      wylie = row["definiendum"]
      bod = row[""]
      if "ERROR" in bod:
        continue
      english = row["english1"].split(";")
      for en in english:
        if wylie and bod and en:
          en = en.replace('\n', ' ')
          if "\n" in en:
            print en + "Uh oh"
            os._exit(1)
          wyliefile.write(wylie.strip() + "\n")
          bodfile.write(bod.strip() + "\n")
          enfile.write(en.strip() + "\n")

main()
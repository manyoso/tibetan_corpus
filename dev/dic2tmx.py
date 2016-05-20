#!/usr/bin/env python

import argparse
import glob
import os
import codecs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import chardet

tmx = Element("tmx")
tmx.attrib["version"] = "1.4"
header = SubElement(tmx, "header")
header.attrib["creationtool"] = "dic2tmx"
header.attrib["creationtoolversion"] = "0.1"
header.attrib["datatype"] = "PlainText"
header.attrib["segtype"] = "sentence"
header.attrib["adminlang"] = "en-us"
header.attrib["srclang"] = "EN"
header.attrib["o-tmf"] = "dic"
body = SubElement(tmx, "body")

def main():
  # Argument parsing
  parser = argparse.ArgumentParser(prog='dic2tmx', description='Converts corpus dictionary files to tmx format.')
  parser.add_argument('path')
  args = parser.parse_args()

  if not os.path.exists(args.path):
    print "Error: path '" + args.path + "' does not exist"
    os._exit(1)
    
  if (os.path.isdir(args.path)):
    processDir(args.path)
  else:
    processFile(args.path)
  print prettify(tmx).encode("utf-8")

def processDir(path):
  index = path + os.sep + "index.txt"
  if not os.path.exists(index):
    print "Error: path '" + index + "' does not exist"
    os._exit(1)

  lines = [line.rstrip('\n') for line in open(index)]
  for line in lines:
    processFile(path + os.sep + line)

def processFile(path):
  wylie = os.path.abspath(path + ".wylie")
  bod = os.path.abspath(path + ".bod")
  en = os.path.abspath(path + ".en")

  wylielines = bodlines = enlines = None
  
  if os.path.exists(wylie):
    wylielines = [line.rstrip('\n') for line in codecs.open(wylie, "r", encoding="utf-8")]
  if os.path.exists(bod):
    bodlines = [line.rstrip('\n') for line in codecs.open(bod, "r", encoding="utf-8")]
  if os.path.exists(en):
    enlines = [line.rstrip('\n') for line in codecs.open(en, "r", encoding="utf-8")]
    
  assert len(wylielines) == len(bodlines) == len(enlines)
  zipped = zip(wylielines, bodlines, enlines)
  
  tu = SubElement(body, "tu")
  tu.attrib["tuid"] = os.path.basename(path)
  for row in zipped:
    tuvW = SubElement(tu, "tuv")
    tuvW.attrib["xml:lang"] = "wylie"
    segW = SubElement(tuvW, "seg")
    segW.text = row[0]
    
    tuvB = SubElement(tu, "tuv")
    tuvB.attrib["xml:lang"] = "bod"
    segB = SubElement(tuvB, "seg")
    segB.text = row[1]
    
    tuvE = SubElement(tu, "tuv")
    tuvE.attrib["xml:lang"] = "en"
    segE = SubElement(tuvE, "seg")
    segE.text = row[2]
  
def prettify(elem):
  rough_string = tostring(elem, encoding="utf-8")
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ")
  
main()
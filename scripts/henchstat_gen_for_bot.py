import argparse
import libhenches
import libspellbook
import tables
import sys
import random

random.seed()

classes = libhenches.parseClasses("pcclasses")
spells = libspellbook.parseSpells("pcspells")
names = libhenches.parseNames("germans")
tables.loadtables("treasuretables")
profs = libhenches.parseProfs("genprofs")

def genHenches(level:int):
  ol = libhenches.genHenches(1, int(level), classes, 10, True, spells, names, profs, True)
  return ''.join(ol)

def genParty(numHenches:int, minLevel:int, maxLevel:int):
  outstring = ""
  for hench in range(numHenches):
    ol = libhenches.genHenches(1, random.randint(minLevel, maxLevel), classes, 10, True, spells, names, profs, True)
    temp = '\n'.join(ol)
    outstring += temp + '\n'
  return outstring

def genHenchesByMarket(market:int, months:int):
  for month in range(0, months):
    print ("Month " + str(month) + ":")
    for level in range(0,5):
      numHenches = libhenches.rollMarket(libhenches.marketClasses[market-1][level])
      print ("L" + str(level) + "s: " + str(numHenches))
      ol = libhenches.genHenches(numHenches, level, classes, market, True, spells, names, profs, True)
      outstring = '\n'.join(ol)
      print (outstring)


import random
# blah dice dependency
import dice
import argparse
import tables

random.seed()

# TODO move me to a data file
# the problem here is that the multitable function always joins with ', '
# if that were configurable, could join with '\n'
# and then have a table like CityStock: [CityEnc*2d4]
# but we don't, so we're doing it this way for now
lairdice = { "City": (1,4), "Inhabited":(1,4), "Clear":(1,4), "Grass":(1,4), "Scrub":(1,4),\
"Hill":(2,4,1), "Woods":(2,4,1), "Desert":(2,4,1), "Jungle":(2,6,1),\
"Mountain":(2,6,1), "Swamp":(2,6,1)}

# load the monster file
tables.loadtables("./monstertables")
# load the terrain description
tables.loadtables("./enctables")
# load the treasure files
tables.loadtables("./treasuretables")

def generate(rows, cols, terrain, encounter, full):
    encTypeSuffix = "Enc" if encounter else "Lair"
    # and now we generate the lairs in the hexes
    outputStr = ""
    for r in range(0,rows):
        for c in range(0,cols):
            if not encounter: 
                outputStr += ("Hex (" + str(r) + ", " + str(c) + "):\n")
            numlairs = 1 if encounter else dice.roll(lairdice[terrain])
            for i in range(0, numlairs):
                monster = tables.evaltable(terrain + "Enc") + '\n'
                outputStr += monster
                monstertable = ''.join(monster.rstrip().lstrip().split(" ")) + encTypeSuffix
                if full and monstertable in tables.tabledice.keys():
                    lairout = tables.evaltable(monstertable)
                    outputStr += lairout+"\n\n"
            outputStr += '\n'
    return outputStr.strip()

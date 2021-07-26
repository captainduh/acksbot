
import random
import sys

# the function of this script is to take a number of mercenaries or thieves
# who have suffered a calamity or leadership change, and determine how many 
# desert, betray, or so forth

possibleoutcomes = [
  ('Attack',2),
  ('Betray',5),
  ('Hesitate',8),
  ('Continue',11),
  ('Continue with elan',10000)]

def calculateDeserters(numguys:int, mlmod:int):
    results = {}
    deserterOutput = ""
    for o in possibleoutcomes:
      results[o[0]] = 0

    for i in range(0,numguys):
      ml = random.randint(1,6)+random.randint(1,6)+mlmod
      for (s,m) in possibleoutcomes:
        if ml <= m:
          results[s] += 1
          break

    for (k,_) in possibleoutcomes:
      deserterOutput += "%s: %d\n"%(k,results[k])

    return deserterOutput

# Dylan Stitt
# Unit 2 Unit Project
# Bear Fish River

from ecosystem import *
import time, os, random

DAYS_SIMULATED = 30
RIVER_SIZE = 10
START_BEARS = 10
START_FISH = 10

def main():
    river = River(RIVER_SIZE, START_BEARS, START_FISH)
    #river.initialPopulation(5)
    #print(river)
    for i in range(10):
        fish = Fish(random.randint(0, river.size - 1), random.randint(0, river.size - 1))
        river.addBaby(fish)

    river.placeBaby()
    #print(river)
    for fish in river.animals:
        fish.move(river)
    #print(river)


if __name__ == '__main__':
    for i in range(1000000):
        main()


# BACKUP
'''
from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 15
START_BEARS = 10
START_FISH = 10

def BearFishRiver():

  r = River(RIVER_SIZE, START_BEARS, START_FISH)
  day = 0
  done = False
  for day in range(DAYS_SIMULATED):
    print(f"\n\nDay: {day+1}")
    print(r)
    print(f"\nStarting Poplation: {r.population} animals")
    done = r.new_day()
    print(f"Ending Poplation: {r.population} animals")
    print(r)
    day += 1
    sleep(5)

if __name__ == "__main__":
  BearFishRiver()
'''
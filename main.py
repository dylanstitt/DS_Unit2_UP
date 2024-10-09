# Dylan Stitt
# Unit 2 Unit Project
# Bear Fish River

from ecosystem import *
import time, os

def main():
    river = River(25, 2, 2)
    print(river[(0, 0)])

if __name__ == '__main__':
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
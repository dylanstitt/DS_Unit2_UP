# Dylan Stitt
# Unit 2 Unit Project
# Bear Fish River

from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 10
START_BEARS = 5
START_FISH = 5

def main():

    r = River(RIVER_SIZE, START_BEARS, START_FISH)
    day = 0
    done = False
    for day in range(DAYS_SIMULATED):
        print(f"\n\nDay: {day+1}")
        print(r)
        print(f"\nStarting Population: {r.population} animals")
        done = r.newDay()
        print(f"Ending Population: {r.population} animals")
        print(r)
        day += 1
        #sleep()

if __name__ == "__main__":
    #for i in range(10000): main()
    main()
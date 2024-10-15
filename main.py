# Dylan Stitt
# Unit 2 Unit Project
# Bear Fish River

#TODO - Finish the newDay function for the simulation running and fix the collision logic
#TODO - debug

from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 10
START_BEARS = 10
START_FISH = 10

def main():

    r = River(RIVER_SIZE, START_BEARS, START_FISH)
    day = 0
    done = False
    for day in range(DAYS_SIMULATED):
        #print(f"\n\nDay: {day+1}")
        #print(r)
        #print(f"\nStarting Population: {r.population} animals")
        done = r.newDay()
        #print(f"Ending Population: {r.population} animals")
        #print(r)
        day += 1
        #sleep()

        if day == 5:
            break

if __name__ == "__main__":
    #for i in range(10000): main()
    main()
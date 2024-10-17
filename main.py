# Dylan Stitt
# Unit 2 Unit Project
# Bear Fish River

from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 15
START_BEARS = 10
START_FISH = 20

def main():

    r = River(RIVER_SIZE, START_BEARS, START_FISH)
    for day in range(DAYS_SIMULATED):
        print(f"\n\nDay: {day+1}")
        print(r)
        print(f"\nStarting Population: {r.population} animals")
        r.newDay()
        print(f"Ending Population: {r.population} animals")
        print(r)
        day += 1
        sleep(5)

if __name__ == "__main__":
    main()

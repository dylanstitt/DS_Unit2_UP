from random import randint, choice

class River:

    def __init__(self, size, numBears, numFish):
        """River Constructor"""
        self.river = [['🟦' for i in range(size)] for i in range(size)]
        self.size = size
        self.numBears = numBears
        self.numFish = numFish

        self.animals = []
        self.population = 0

        self.__pendingBabies = []
        self.__initialPopulation()

    def __str__(self):
        """Print the river"""
        for i in self.river:
            for j in i:
                print(j, end='')
            print()
        return ''

    def __getitem__(self, x):
        """Indexing the river"""
        return self.river[x]

    #TODO MAKE PRIVATE AND RUN IN NEW DAY
    def __initialPopulation(self):
        """Place the initial population of bears and fish randomly in the river"""
        used = []
        for i in range(self.numBears):
            x, y = randint(0, self.size-1), randint(0, self.size-1)
            while (x, y) in used:
                x, y = randint(0, self.size-1), randint(0, self.size-1)

            used.append((x, y))
            bear = Bear(x, y, 5)
            self.river[y][x] = bear
            self.animals.append(bear)

        for i in range(self.numFish):
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
            while (x, y) in used:
                x, y = randint(0, self.size - 1), randint(0, self.size - 1)

            used.append((x, y))
            fish = Fish(x, y)
            self.river[y][x] = fish
            self.animals.append(fish)

        self.population = len(self.animals)

    def addBaby(self, baby):
        self.__pendingBabies.append(baby)

    def placeBaby(self):
        """Loop through __pendingBabies and place the all on the river"""
        for baby in self.__pendingBabies:
            self.animals.append(baby)
            self.river[baby.y][baby.x] = baby

        self.population = len(self.animals)

    def animalDeath(self, animal):
        """Kills and removes and animals from the river"""
        self.animals.remove(animal)
        self.population = len(self.animals)

        self.river[animal.y][animal.x] = '🟦'

    def redraw(self, animal, currentX, currentY, newCoords):
        """Redraws the river to the correct display"""

        self.river[newCoords[1]][newCoords[0]] = animal
        self.river[currentY][currentX] = '🟦'

        self.animals.remove(animal)
        self.animals.append(animal)

    def newDay(self):
        """Main simulation functionality"""
        for animal in self.animals:
            animal.move(self)
        self.placeBaby()

###################################################

class Animal:

    def __init__(self, x, y):
        """Animal Parent Constructor"""
        self.x = x
        self.y = y
        self.bredToday = False
        self.icon = ''

    def death(self, river):
        """Calls the river animalDeath function and passes in the current object"""
        river.animalDeath(self)

    def __availableCoords(self, river):
        orignial = [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1), (self.x - 1, self.y - 1), (self.x + 1, self.y + 1), (self.x - 1, self.y + 1), (self.x + 1, self.y - 1)]
        available = []
        for coords in orignial:
            try:
                if coords[0] < 0 or coords[0] > river.size - 1:
                    continue
                elif coords[1] < 0 or coords[1] > river.size - 1:
                    continue

                available.append(coords)

            except IndexError:
                continue
        
        return available
    
    def move(self, river):
        """Move the current animal to a new position"""
        x, y = choice(self.__availableCoords(river))

        if river[y][x] == '🟦':
            river.redraw(self, self.x, self.y, (x, y))

        elif river[y][x].icon == self.icon and river[self.y][self.x] is self:
            self.collision(river, (x, y), self.icon)

        elif river[y][x].icon == self.icon and river[self.y][self.x] is not self:
            self.collision(river, (x, y), '🐻🐟')

    #TODO FINISH BEAR AND FISH INTERACTION
    def collision(self, river, otherCoords, mode):
        """Detect collision between Bears and Fish and same animals"""
        if mode == '🐻':
            bearObjs = []
            for pair in [(self.y, self.x), (otherCoords[1], otherCoords[0])]:
                bearObj = [i for i in river.animals if i is river[pair[0]][pair[1]]][-1]
                bearObjs.append(bearObj)

            babyCoords1 = self.__availableCoords(river)
            babyCoords1.extend(bearObjs[1].__availableCoords(river))
            babyCoords = choice(list(set(babyCoords1)))

            river.addBaby(Bear(babyCoords[0], babyCoords[1], bearObjs[0].maxLives))

        elif mode == '🐟':
            fishObjs = []
            for pair in [(self.y, self.x), (otherCoords[1], otherCoords[0])]:
                fishObj = [i for i in river.animals if i is river[pair[0]][pair[1]]][-1]
                fishObjs.append(fishObj)

            babyCoords1 = self.__availableCoords(river)
            babyCoords1.extend(fishObjs[1].__availableCoords(river))
            babyCoords = choice(list(set(babyCoords1)))

            river.addBaby(Fish(babyCoords[0], babyCoords[1]))

        else:
            ...


###################################################

class Bear(Animal):

    def __init__(self, x, y, maxLives):
        """Bear Constructor"""
        super().__init__(x, y)

        self.icon = '🐻'
        self.eatenToday = False
        self.maxLives = maxLives
        self.lives = self.maxLives

    def __str__(self):
        """Print the bear icon"""
        return self.icon

    def starve(self, river):
        """Checks if the Bear has eaten today, and if not then decrement lives by 1 and then check for death"""
        if not self.eatenToday:
            self.lives -= 1

            if self.lives == 0:
                self.death(river)

    def consume(self, fish, river):
        """Bear eating a fish and removing the fish from the river"""
        self.lives = self.maxLives
        self.eatenToday = True
        fish.death(river)

###################################################

class Fish(Animal):

    def __init__(self, x, y):
        """Fish Constructor"""
        super().__init__(x, y)
        self.icon = '🐟'

    def __str__(self):
        """Print the fish icon"""
        return self.icon

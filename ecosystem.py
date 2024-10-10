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

    ############################################# MAKE PRIVATE AND RUN IN NEW DAY
    def initialPopulation(self, bearLives):
        """Place the initial population of bears and fish randomly in the river"""
        used = []
        for i in range(self.numBears):
            x, y = randint(0, self.size-1), randint(0, self.size-1)
            while (x, y) in used:
                x, y = randint(0, self.size-1), randint(0, self.size-1)

            used.append((x, y))
            bear = Bear(x, y, bearLives)
            self.river[y][x] = bear.icon
            self.animals.append(bear)

        for i in range(self.numFish):
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
            while (x, y) in used:
                x, y = randint(0, self.size - 1), randint(0, self.size - 1)

            used.append((x, y))
            fish = Fish(x, y)
            self.river[y][x] = fish.icon
            self.animals.append(fish)

        self.population = len(self.animals)


    def addBaby(self, baby):
        self.__pendingBabies.append(baby)

    def placeBaby(self):
        """Loop through __pendingBabies and place the all on the river"""
        for baby in self.__pendingBabies:
            self.animals.append(baby)
            self.river[baby.y][baby.x] = baby.icon

        self.population = len(self.animals)

    def animalDeath(self):
        """Kills and removes and animals from the river"""
        ...

    def redraw(self):
        """Redraws the river to the correct display"""
        ...

    def newDay(self):
        """Main simulation functionality"""
        ...
        # Call place baby in here

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

    def move(self, river):
        """Move the current animal to a new position"""
        orignial = [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1), (self.x - 1, self.y - 1), (self.x + 1, self.y + 1), (self.x - 1, self.y + 1), (self.x + 1, self.y - 1)]
        available = []
        for coords in orignial:
            try:
                if coords[0] < 0 or coords[0] > river.size-1:
                    continue
                elif coords[1] < 0 or coords[1] > river.size-1:
                    continue

                if river[coords[1]][coords[0]] != '🟦':
                    continue
                available.append(coords)

            except IndexError:
                continue

        if len(available) != 0:
            currentCoords = (self.x, self.y)
            newCoords = choice(available)

            river[newCoords[1]][newCoords[0]] = self.icon
            river[currentCoords[1]][currentCoords[0]] = '🟦'

    def collision(self, river, other):
        """Detect collision between Bears and Fish and same sex animals"""
        if self.icon == other.icon:
            available = [(self.x-1, self.y), (self.x+1, self.y), (self.x, self.y-1), (self.x, self.y+1), (self.x-1, self.y-1), (self.x+1, self.y+1), (self.x-1, self.y+1), (self.x+1, self.y-1)]
            for coords in available:
                try:
                    if river[coords[1]][coords[0]] != '🟦':
                        available.remove(coords)

                except IndexError:
                    continue
            print(available) #####################################################
            if self.icon == '🐻':
                coords = choice(available)
                river.addBaby(Bear(coords[0], coords[1], other.maxLives))
            else:
                coords = choice(available)
                river.addBaby(Fish(coords[0], coords[1]))

        else:
            Bear.consume(self, other, river)

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

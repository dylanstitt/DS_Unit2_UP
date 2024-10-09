from random import randint

class River:

    def __init__(self, size, numBears, numFish):
        self.river = [['🟦' for i in range(size)] for i in range(size)]
        self.size = size
        self.numBears = numBears
        self.numFish = numFish

        self.animals = []
        self.population = 0

    def __str__(self):
        for i in self.river:
            for j in i:
                print(j, end='')
            print()

    def __getitem__(self, coords):
        return self.river[coords[1]][coords[0]]


    def __initalPopulation(self):
        ...

    def placeBaby(self):
        ...

    def animalDeath(self):
        ...

    def redraw(self):
        ...

    def newDay(self):
        ...

###################################################

class Animal:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bredToday = False

    def death(self):
        ...

    def move(self):
        ...

    def collision(self):
        ...

###################################################

class Bear(Animal):

    def __init__(self, x, y, maxLives):
        super().__init__(x, y)

        self.icon = '🐻'
        self.eatenToday = False
        self.maxLives = maxLives
        self.lives = self.maxLives

    def __str__(self):
        return self.icon

    def starve(self):
        ...

    def consume(self):
        ...

###################################################

class Fish(Animal):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.icon = '🐟'

    def __str__(self):
        return self.icon

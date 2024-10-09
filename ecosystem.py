from random import randint

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

    def __getitem__(self, coords):
        """Indexing the river"""
        return self.river[coords[1]][coords[0]]


    def __initialPopulation(self):
        """Place the initial population of bears and fish randomly in the river"""
        ...

    def placeBaby(self):
        """Loop through __pendingBabies and place the all on the river"""
        ...

    def animalDeath(self):
        """Kills and removes and animals from the river"""
        ...

    def redraw(self):
        """Redraws the river to the correct display"""
        ...

    def newDay(self):
        """Main simulation functionality"""
        ...

###################################################

class Animal:

    def __init__(self, x, y):
        """Animal Parent Constructor"""
        self.x = x
        self.y = y
        self.bredToday = False

    def death(self, river):
        """Calls the river animalDeath function and passes in the current object"""
        river.animalDeath(self)

    def move(self):
        """Move the current animal to a new position"""
        ...

    def collision(self, other):
        """Detect collision between Bears and Fish and same sex animals"""
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

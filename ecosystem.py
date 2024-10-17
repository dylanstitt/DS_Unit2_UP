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

    def __initialPopulation(self):
        """Place the initial population of bears and fish randomly in the river"""
        used = []
        for i in range(self.numBears):
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
            while (x, y) in used:
                x, y = randint(0, self.size - 1), randint(0, self.size - 1)

            used.append((x, y))
            bear = Bear(x, y, 3)
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
        if self.population >= self.size ** 2:
            print("RIVER FULL")
            exit()

        self.__pendingBabies.append(baby)

    def placeBabies(self):
        """Loop through __pendingBabies and place the all on the river"""
        for baby in self.__pendingBabies:
            self.animals.append(baby)
            self.river[baby.y][baby.x] = baby
        self.__pendingBabies = []

    def animalDeath(self, animal):
        """Kills and removes and animals from the river"""
        if animal in self.animals:
            self.animals.remove(animal)
            self.redraw(animal, (animal.x, animal.y))
            #print(f"☠️ ☠️ ☠️  A {str(animal)}  has died")

    def redraw(self, animal, new):
        """Redraws the river to the correct display"""
        self.river[new[1]][new[0]] = animal
        self.river[animal.y][animal.x] = '🟦'

    def newDay(self):
        """Main simulation functionality"""
        animals = self.animals[:]
        for animal in animals:
            animal.move(self)

            if type(animal) == Bear:
                animal.eatenToday = False

            animal.timesBred += 1
            if animal.timesBred == 5 and type(animal) == Fish:
                self.animalDeath(animal)
            if animal.timesBred == 2 and type(animal) == Bear:
                self.animalDeath(animal)

        self.placeBabies()
        self.animals = [self.river[i][j] for i in range(self.size) for j in range(self.size) if self.river[i][j] in self.animals]
        self.population = len(self.animals)

        for i in range(len(self.river)):
            for j in range(len(self.river[i])):
                if self.river[i][j] not in self.animals:
                    self.river[i][j] = '🟦'


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
        dx, dy = randint(-1, 1), randint(-1, 1)
        while (dx+self.x < 0 or dx+self.x >= river.size) or (dy+self.y < 0 or dy+self.y >= river.size):
            dx, dy = randint(-1, 1), randint(-1, 1)

        if river[dy+self.y][dx+self.x] == '🟦':
            river.redraw(self, (dx+self.x, dy+self.y))

        elif type(river[dy+self.y][dx+self.x]) == type(self):
            #print(f"⚠️ ⚠️ ⚠️  Collision {river[dy+self.y][dx+self.x].icon}  {self.icon}")
            self.collision(river, river[dy+self.y][dx+self.x], self.icon)

        elif type(river[dy+self.y][dx+self.x]) != type(self):
            #print(f"⚠️ ⚠️ ⚠️  Collision {river[dy+self.y][dx+self.x].icon}  {self.icon}")
            self.collision(river, river[dy+self.y][dx+self.x], '🐻🐟')

    def collision(self, river, other, mode):
        """Detect collision between Bears and Fish and same animals"""
        global x, y

        if self.icon != '🐻':
            bear, fish = other, self
        else:
            bear, fish = self, other

        if len(mode) == 1:
            x, y = randint(0, river.size-1), randint(0, river.size-1)
            while river[y][x] != '🟦':
                x, y = randint(0, river.size - 1), randint(0, river.size - 1)

        if mode == '🐻':
            river.addBaby(Bear(x, y, bear.maxLives))
            bear.starve(river)
            #print("New baby bear! 🐻")
        elif mode == '🐟':
            river.addBaby(Fish(x, y))
            #print("New baby fish! 🐟")
        else:
            bear.consume(fish, river)
            river.redraw(bear, (fish.x, fish.y))


###################################################

class Bear(Animal):

    def __init__(self, x, y, maxLives):
        """Bear Constructor"""
        super().__init__(x, y)

        self.icon = '🐻'
        self.eatenToday = False
        self.maxLives = maxLives
        self.lives = self.maxLives
        self.timesBred = 0

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
        self.timesBred = 0

    def __str__(self):
        """Print the fish icon"""
        return self.icon

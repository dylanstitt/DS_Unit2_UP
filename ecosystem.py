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

    ############################################# MAKE PRIVATE AND RUN IN NEW DAY
    def __initialPopulation(self):
        """Place the initial population of bears and fish randomly in the river"""
        used = []
        for i in range(self.numBears):
            x, y = randint(0, self.size-1), randint(0, self.size-1)
            while (x, y) in used:
                x, y = randint(0, self.size-1), randint(0, self.size-1)

            used.append((x, y))
            bear = Bear(x, y, 5)
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

    def animalDeath(self, animal):
        """Kills and removes and animals from the river"""
        self.animals.remove(animal)
        self.population = len(self.animals)

        self.river[animal.y][animal.x] = '🟦'

    def redraw(self, animal, currentX, currentY, newCoords):
        """Redraws the river to the correct display"""

        self.river[newCoords[1]][newCoords[0]] = animal.icon
        self.river[currentY][currentX] = '🟦'

    def newDay(self):
        """Main simulation functionality"""
        for animal in self.animals:
            animal.move(self)

###################################################

class Animal:

    def __init__(self, x, y):
        """Animal Parent Constructor"""
        self.x = x
        self.y = y
        self.bredToday = False
        self.icon = ''
        self.maxLives = 0

    def death(self, river):
        """Calls the river animalDeath function and passes in the current object"""
        river.animalDeath(self)

    def move(self, river):
        print(river)
        """Move the current animal to a new position"""
        orignial = [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1), (self.x - 1, self.y - 1), (self.x + 1, self.y + 1), (self.x - 1, self.y + 1), (self.x + 1, self.y - 1)]
        available = []
        for coords in orignial:
            try:
                if coords[0] < 0 or coords[0] > river.size-1:
                    continue
                elif coords[1] < 0 or coords[1] > river.size-1:
                    continue

                available.append(coords)

            except IndexError:
                continue

        ####################### FIX THE COLLISION OF ANIMALS WHEN THEY WANT TO MOVE SOMEWHERE
        ####################### PUT ALL COLLISION LOGIC IN THE COLLISION FUNCTION
        '''for coords in available:
            if river[coords[1]][coords[0]] == '🐟':
                fishObj = []
                fish = 0
                for i in range(coords[1]):
                    for j in range(coords[0]):
                        if river[i][j] == '🐟':
                            fish += 1

                for a in river.animals:
                    if a.icon == '🐟':
                        fish -= 1
                        fishObj.append(a)

                        if fish == 0:
                            break

                self.collision(river, other=fishObj[-1])

            else:
                self.collision(river, otherIcon='🐻')

            river.redraw(self, self.x, self.y, coords)'''


    def collision(self, river, other=None, otherIcon=''):
        """Detect collision between Bears and Fish and same sex animals"""
        if self.icon == otherIcon:
            orignial = [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1), (self.x - 1, self.y - 1), (self.x + 1, self.y + 1), (self.x - 1, self.y + 1), (self.x + 1, self.y - 1)]
            available = []
            for coords in orignial:
                try:
                    if coords[0] < 0 or coords[0] > river.size - 1:
                        continue
                    elif coords[1] < 0 or coords[1] > river.size - 1:
                        continue

                    if river[coords[1]][coords[0]] != '🟦':
                        continue
                    available.append(coords)

                except IndexError:
                    continue

            if len(available) != 0:
                if self.icon == '🐻':
                    coords = choice(available)
                    river.addBaby(Bear(coords[0], coords[1], self.maxLives))
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

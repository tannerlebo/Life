from world import World
from cell import Cell
from world_torus import World_Torus
from rules import Rules
import toolbox
from time import sleep
import os

class Life(object):

    def __init__(self):
        self.__worldType = World
        self.__world = self.__worldType(13, 51)
        self.__percentage = 50
        self.__world.randomize()
        self.__delay = 0.5
        self.__generation = 1
        self.__menu = 'main'

    def main(self):
        """Main event loop for world."""
        command = 'help'
        while command != 'quit':
            if command == 'help':
                self.help('lifehelp.txt')
                print(f'\n{self.__world}')
                self.show_status()
            elif command == 'new-world':
                self.add_new_world()
            elif command == 'next-generation':
                self.next_generation(parameter)
            elif command == 'fillrate':
                self.fillrate(parameter)
            elif command == 'change-size':
                self.change_size(parameter)
            elif command == 'run-simulation':
                self.run_simulation(parameter)
            elif command == 'jump-generations':
                self.jump_generations(parameter)
            elif command == 'delay':
                print(self.__world.get_grid())
                print(self.__world.get_rows())
                self.get_speed(parameter)
            elif command == 'change-display':
                self.change_graphics(parameter)
            elif command == 'save':
                self.save(parameter, './worlds/')
            elif command == 'load':
                self.load(parameter, './worlds/')
            elif command == 'more':
                self.__menu = 'more'
            elif command == 'back':
                self.__menu = 'main'
            elif command == 'world-type':
                self.get_geometry()
            elif command == 'change-rules':
                self.change_rules(parameter)
            self.get_menu()
            self.__menu = 'main'
            command, parameter = self.get_command()

    def get_menu(self):
        """
        Displays the menu.
        :return:
        """
        if self.__menu == 'main':
            print("N[E]w  [N]ext  [R]un  [F]illrate  [J]ump  [S]ize  [J]ump  Sa[V]e  L[O]ad  [M]ore  [H]elp  [Q]uit")
        if self.__menu == 'more':
            print("[D]elay  [G]raphics  R[U]les  Sa[V]e  L[O]ad  [W]orldType  [B]ack  [H]elp  [Q]uit")

    def get_command(self):
        """
        Get a valid command from the user.
        :return:
        """

        commands = {'e': 'new-world',
                    'n': 'next-generation',
                    'f': 'fillrate',
                    's': 'change-size',
                    'r': 'run-simulation',
                    'j': 'jump-generations',
                    'd': 'delay',
                    'v': 'save',
                    'o': 'load',
                    'h': 'help',
                    '?': 'help',
                    'g': 'change-display',
                    'u': 'change-rules',
                    'm': 'more',
                    'b': 'back',
                    'w': 'world-type',
                    'q': 'quit'}

        validCommands = commands.keys()

        letter = '&&&&&&'
        while letter not in validCommands:
            userInput = input('Command: ')
            if userInput != '':
                letter = userInput[0].lower()
                parameter = userInput[1:].strip()
                if parameter == '':
                    parameter = None
            else:
                letter = 'n'
                parameter = None

        return commands[letter], parameter

    def help(self, filename, prompt = None):
        """
        Displays instructions.
        :param filename: name of file that contains instructions
        :param prompt: question to ask after to continue program
        :return:
        """
        with open(filename, 'r') as file:
            help = file.read()
        print(help, end='')
        if prompt:
            input('\n'+prompt)
        hi = input("\n\npress <return> to continue")



    def add_new_world(self):
        """
        Adds new world and re-randomized with same fillrate.
        :return:
        """
        self.__world.randomize(self.__percentage)
        print("\n...Creating New World...")
        sleep(2)
        print(self.__world)
        self.show_status()

    def get_rows(self):
        """
        Gets amount of rows in new world from user.
        :return: rows
        """
        rows = toolbox.get_integer("How many rows do you want in your world? ")
        return rows

    def get_columns(self):
        """
        gets amount of columns in new world from user
        :return: columns
        """
        columns = toolbox.get_integer("How many columns do you want in your world? ")
        return columns

    def next_generation(self, parameter):
        """
        "advances to the next generation.
        :param parameter: amount of generations if user specifies
        :return:
        """
        if parameter:
            for generation in range(1, (int(parameter) + 1)):
                if self.__world.stop_simulation():
                    print()
                    print("Simulation is stable.")
                    print()
                    break
                else:
                    self.__world.next_generation()
                    self.__generation += 1
            print(self.__world)
            self.show_status()
        else:
            if self.__world.stop_simulation():
                print()
                print('World is stable.')
                print()
            else:
                self.__world.next_generation()
                self.__generation += 1
            print(self.__world)
            self.show_status()

    def fillrate(self, parameter):
        """
        Takes percentage from user on how much of the cells in the world are alive
        :param parameter: percent of cells alive to advance if user specifies in menu
        :return:
        """
        if parameter:
            self.__world.randomize(int(parameter))
        else:
            self.__world.randomize(self.get_percentage())
        sleep(2)
        print(f"\nFillrate changed to {self.__percentage}%")
        print(self.__world)
        self.show_status()

    def change_size(self, parameter):
        """
        Asks user what to change the size of the world to and sets it.
        :param parameter: dimensions if user specifies in menu
        :return:
        """
        if parameter and ('x' in parameter):
            rows, columns = parameter.split('x', 2)
            w1 = self.__worldType(int(rows), int(columns))
        else:
            rows = self.get_rows()
            columns = self.get_columns()
            w1 = self.__worldType(rows, columns)
        w1.create_grid()
        w1.create_neighbors()
        self.__world = w1
        self.__world.randomize(self.__percentage)
        sleep(0.5)
        print(f"\n...Changing size to {rows}x{columns}...")
        sleep(2)
        print(self.__world)
        self.show_status()

    def run_simulation(self, parameter):
        """
        Runs the simulation for a certain amount of generations inputted by the user.
        :param parameter: number of generations to advance if user specifies in menu before
        :return:
        """
        if parameter:
            for generation in range(1, int(parameter)+1):
                #stop = self.stop_simulation()
                if self.__world.stop_simulation():
                    print()
                    print("Simulation is stable.")
                    print()
                    break
                else:
                    self.__world.next_generation()
                    self.__generation += 1
                    sleep(self.__delay)
                    print(self.__world)
                    self.show_status()
            print(f"Advanced {generation} generations.\n")
        else:
            for generation in range(1, ((self.get_generations())+1)):
                #stop = self.stop_simulation()
                if self.__world.stop_simulation():
                    print()
                    print("Simulation is stable.")
                    print()
                    break
                else:
                    self.__world.next_generation()
                    sleep(self.__delay)
                    self.__generation += 1
                    print(self.__world)
                    self.show_status()
            print(f"Simulation over. Advanced {generation} generations.\n")

    def jump_generations(self, parameter):
        """
        Skips ahead a number of generations the user can input
        :param parameter: number of generations to skip if user specifies in menu before
        :return:
        """

        if parameter:
            for generation in range(1, (int(parameter) + 1)):
                stop = self.stop_simulation()
                if stop:
                    print()
                    print("Simulation is stable.")
                    print()
                    break
                else:
                    self.__2ndlastworld = self.__lastworld
                    self.__lastworld = self.__world
                    self.__world.next_generation()
            self.__generation += parameter
        else:
            for generation in range(1, ((self.get_generations())+1)):
                stop = self.stop_simulation()
                if stop:
                    print()
                    print("Simulation is stable.")
                    print()
                    break
                else:
                    self.__2ndlastworld = self.__lastworld
                    self.__lastworld = self.__world
                    self.__world.next_generation()
                    self.__generation += 1
        sleep(1)
        print("\nSkipping generations...")
        sleep(2)
        print(self.__world)
        self.show_status()

    def get_generations(self):
        """
        gets a number of generations from the user
        :return: number of generations
        """
        generations = toolbox.get_integer("How many generations do you want to advance? ")
        return int(generations)

    def get_percentage(self):
        """
        gets a number as a percent from the user
        :return: the percentage inputted
        """
        self.__percentage = toolbox.get_integer_between(1, 100, "What percent of cells do you want alive? (just enter integer) ")
        return self.__percentage

    def show_status(self):
        """
        diplays the size of the world, the percent alive, the speed, and the generation
        :return: string
        """
        string = f'Size: {self.__world.get_rows()}x{self.__world.get_columns()}  Alive: {self.calculate_percentage()}%'
        if self.__worldType == World:
            world = 'Normal'
        else:
            world  = "Disk"
        string += f'  Delay: {self.__delay} sec.  Generation: {self.__generation}  World Type: {world}'
        stayAlive = str(Rules.stayAlive)
        #stayAlive = Rules.ruleSets[set]['stayAlive']
        stayAlive1 = stayAlive[0]
        stayAlive2 = stayAlive[1]
        becomeAlive = str(Rules.becomeAlive)
        #becomeAlive = Rules.ruleSets[set]['becomeAlive']
        string +=  f'  Rules: {stayAlive1} or {stayAlive2} neighbors to stay alive, {becomeAlive} neighbors to become alive\n'
        print(string)

    def get_alive(self):
        """
        calculates the number of cells alive in the current world
        :return: returns the number of alive cells
        """
        alive = 0
        for row in self.__world.get_grid():
            for cell in row:
                if cell.get_living():
                    alive += 1
        return alive

    def get_total(self):
        """
        calculates the total number of cells in the world
        :return: the total number of cells in the world
        """
        return (self.__world.get_rows())*(self.__world.get_columns())

    def calculate_percentage(self):
        """
        takes number of cells alive and calculates it using the total cells
        :return: percent of cells alive
        """
        return round((self.get_alive()/self.get_total())*(100))

    def get_speed(self, parameter):
        """
        gets speed at which the generations advance from user
        :param parameter: number of seconds before it advances if user specifies in menu
        :return:
        """
        if parameter:
            self.__delay = parameter
        else:
            self.__delay = toolbox.get_positive_number("How many seconds do you want between each generation? ")
        print(f"Delay is now {self.__delay} second(s).\n")

    def change_graphics(self, whichCharacters):
        """Change the live and dead characters for the cells."""
        if toolbox.is_integer(whichCharacters) and \
                1 <= int(whichCharacters) <= len(Cell.displaySets.keys()):
            whichCharacters = int(whichCharacters)
        else:
            print('**************************************')
            for number, set in enumerate(Cell.displaySets):
                liveChar = Cell.displaySets[set]['liveChar']
                deadChar = Cell.displaySets[set]['deadChar']
                print(f'{number + 1}: living cells: {liveChar} dead cells: {deadChar}')
            print(f'{number + 2}: pick your own characters')
            print('**************************************')
            prompt = 'What character set would you like to use?'
            whichCharacters = toolbox.get_integer_between(1, number + 2, prompt)
            if whichCharacters == number + 2:
                alive = toolbox.get_string('Which character should represent alive cells?')
                dead = toolbox.get_string('Which character should represent dead cells?')
                Cell.set_display_user_values(alive, dead)
        setString = list(Cell.displaySets.keys())[whichCharacters - 1]
        Cell.set_display(setString)
        self.display()

    def display(self):
        """
        Prints the world, status bar and menu
        :return: None
        """
        print()
        print('****************************************************************')
        print()
        print(self.__world)
        print(self.show_status())

    def get_alive_graphic(self):
        """
        asks user what character they want for alive cells
        :return:
        """
        alive = input("What would you like to display for alive cells?")
        if len(alive) > 1:
            alive = input("Input must be one character: ")

    def get_dead_graphic(self):
        """
        asks user what character they want for dead cells
        :return:
        """
        dead = input("What would you like to display for dead cells?")
        if len(dead) > 1:
            dead = input("Input must be one character: ")

    def save(self, filename, myPath='./'):
        """
        saves the file to a name and location which user chooses
        :param filename: name the user wants the world to be called
        :param myPath: location of file it will save to
        :return: string telling user it was saved
        """
        allFiles = os.listdir(myPath)
        if filename == None:
            filename = toolbox.get_string("What would you like to call the file? ")
        if filename[-5:] != '.life':
            filename += '.life'
        if not os.path.isdir(myPath):
            os.mkdir(myPath)
        if filename[0:len(myPath)] != myPath:
            filename = myPath + filename
        if filename in allFiles:
            answer = toolbox.yes_or_no("Are you sure you want to save?")
            if answer:
                self.__world.save(filename)
                print(f'Saved {filename}')
            else:
                print(f"{filename} not saved")
        else:
            self.__world.save(filename)
            print(f'Saved {filename}')

    def load(self, filename, myPath='./'):
        """
        loads a file that user already haves and makes it the current world
        :param filename: name the user calls the world
        :param myPath: location of file it comes from
        :return:
        """
        allFiles = os.listdir(myPath)
        if filename == None:
            print("Here are your options to load:\n")
            for file in allFiles:
                print(file)
                print()
            filename = toolbox.get_string("Which file do you want to load? ")
        if filename[-5:] != '.life':
            filename += '.life'
        if filename not in allFiles:
            print('404: File not found...')
        else:
            if filename[0:len(myPath)] != myPath:
                filename = myPath + filename
            sleep(1)
            print(f"...loading {filename}...")
            sleep(2)
            self.__world = self.__worldType.from_file(filename, self.__worldType)
        print(self.__world)

    def get_geometry(self):
        print("""
        1) Normal World
        2) Torus World (no corners, world wraps around)
        """)
        geometry = toolbox.get_integer("What type of world would you like to have?")
        if geometry == 1:
            self.__worldType = World
        else:
            self.__worldType = World_Torus
        sleep(1)
        print("...creating new world...")
        sleep(2)
        print(self.__world)
        self.show_status()

    def change_rules(self, whichNumbers):
        """

        :param whichNumbers:
        :return:
        """
        if whichNumbers:
            if toolbox.is_integer(whichNumbers) and \
                    1 <= int(whichNumbers) <= len(Rules.ruleSets.keys()):
                whichNumbers = int(whichNumbers)
        else:
            print('**************************************')
            for number, set in enumerate(Rules.ruleSets):
                stayAlive = Rules.ruleSets[set]['stayAlive']
                stayAlive1 = stayAlive[0]
                stayAlive2 = stayAlive[1]
                becomeAlive = Rules.ruleSets[set]['becomeAlive']
                string = f'{number + 1}: Neighbors needed for cell to stay alive: {stayAlive1}, {stayAlive2}     '
                string += f'Neighbors needed for cell to become alive: {becomeAlive}'
                print(string)
            print(f'{number + 2}: pick your own characters')
            print('**************************************')
            prompt = 'What character set would you like to use?'
            whichNumbers = toolbox.get_integer_between(1, number + 2, prompt)
            if whichNumbers == number + 2:
                print()
                string = 'You can pick 2 number amounts of neighbors so that an  alive cell stays alive. '
                string += '\nFor example, typing "23" makes it so if a cell has 2 or 3 neighbors, it stays alive. '
                string += '\nHow many neighbors do you want? Please type a 2 digit number: '
                stay = toolbox.get_string(string)
                become = toolbox.get_string('Which number of neighbors would you like to change a cell from dead to alive? (One digit number)  ')
                Rules.set_rules_user_values(stay, become)
        setString = list(Rules.ruleSets.keys())[whichNumbers - 1]
        Rules.set_rules(setString)
        self.display()

if __name__ =='__main__':
    simulation = Life()
    simulation.main()











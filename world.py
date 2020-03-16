from cell import Cell
from rules import Rules
import random
class World(object):

    @classmethod
    def from_file(cls, filename, world):
        """
        Takes world from file and converts it to graphics the user wants.
        :param filename:
        :return: the new world they loaded
        """
        with open(filename, 'r') as myFile:
            text = myFile.readlines()

        rows = len(text)
        columns = len(text[0])
        newWorld = world(rows, columns)
        for rowNumber, row in enumerate(text):
            for columnNumber, cellText in enumerate(row):
                if cellText == Cell.displaySets['basic']['liveChar']:
                    newWorld.set_cell(rowNumber, columnNumber, True)
        return newWorld




    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._grid = self.create_grid()
        self.create_neighbors()
        self._timeline = []


    def __str__(self):
        """Return a string that represents the current generation. For example,
        a completely dead world (4x5) would look like this, assuming that
        Cell.deadChar is a period:
        .....
        .....
        .....
        .....
        A world (4x5) with one living cell would look like this, assuming
        that Cell.liveChar is an 'X' at position self.__grid[1][3]:
        .....
        ...X.
        .....
        .....
        Of course, you would not check on Cell.deadChar or Cell.liveChar. You
        would rely on the cell to know how it should be printed.
        """
        string = ''
        for row in self._grid:
            for cell in row:
                string += cell.__str__()
            string += '\n'
        return string

    def create_grid(self):
        """
        Return the grid as a list of lists. There should be one list
        to contain the entire grid and in that list there should be one
        list to contain each row in the generation. Each of the "row lists"
        should contain one object of class Cell for each column in the world.
        :return: a list of the grid
        """

        grid = []
        for rowNumber in range(self._rows):
            row = []
            for columnNumber in range(self._columns):
                row.append(Cell(rowNumber, columnNumber))
            grid.append(row)
        return grid

    def create_neighbors(self):
        """
        Loop through the grid and assign the neighbors to each cell.
        :return:
        """
        for row in self._grid:
            for cell in row:
                #
                # There are some nine situations that we have to account for:
                #
                # 1. upper left corner (3 neighbors)
                # 2. rest of the top row (5 neighbors)
                # 3. upper right corner (3 neighbors)
                # 4. far left side (5 neighbors)
                # 5. normal cells (8 neighbors)
                # 6. far right side (5 neighbors)
                # 7. lower left corner (3 neighbors)
                # 8. rest of bottom row (5 neighbors)
                # 9. lower right corner (3 neighbors)
                #
                row = cell.get_row()
                column = cell.get_column()
                #print(f'({row},{column})')
                # top row
                if row == 0:
                    if column == 0:
                        #print('upper left')
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    elif column < (self._columns - 1):
                        #print('upper')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                    else:
                        #print('upper right')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                # middle area
                elif row < (self._rows - 1):
                    if column == 0:
                        #print('far left side')
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                    elif column < (self._columns - 1):
                        #print('normal')
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column + 1])
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                    else:
                        #print('far right side')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row + 1][column])
                        cell.add_neighbor(self._grid[row + 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                # bottom row
                else:
                    if column == 0:
                        #print('lower left')
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                    elif column < (self._columns - 1):
                        #print('lower')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row][column + 1])
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])
                        cell.add_neighbor(self._grid[row - 1][column + 1])
                    else:
                        #print('lower right')
                        cell.add_neighbor(self._grid[row][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column - 1])
                        cell.add_neighbor(self._grid[row - 1][column])

    def set_cell(self, row, column, living):
        """
        Change the state of the cell at self.__grid[row][column] to the
         value of living.
        :param row: the row the cell is in
        :param column: the column the cell is it
        :param living: whether the cells is live or dead
        :return:
        """
        self._grid[row][column].set_living(living)

    def next_generation(self):
        """
        Changes the grid to the next generation after following the
        propagation rules.
        :return:
        """
        newGrid = self.create_grid()
        for row in self._grid:
            for cell in row:
                if cell.get_living() == True:
                    """stayAlive = Rules.ruleSets[Rules.ruleSet]['stayAlive']
                    neighbor1 = stayAlive[0]
                    neighbor2 = stayAlive[1]"""
                    if str(cell.living_neighbors()) in str(Rules.stayAlive):
                        newGrid[cell.get_row()][cell.get_column()].set_living(True)
                else:
                    #becomeAlive = Rules.ruleSets[Rules.ruleSet]['becomeAlive']
                    if str(cell.living_neighbors()) == str(Rules.becomeAlive):
                        newGrid[cell.get_row()][cell.get_column()].set_living(True)
        self._grid = newGrid
        self.create_neighbors()
        self._timeline.append(self.__str__())

    def randomize(self, percentage=50):
        """
        Takes a cell and randomizes whether it is dead or alive.
        :param percentage: percent change a cell is alive
        :return:
        """
        newGrid = self.create_grid()
        for row in self._grid:
            for cell in row:
                number = random.randint(1,100)
                if number <= percentage:
                    newGrid[cell.get_row()][cell.get_column()].set_living(True)
                else:
                    newGrid[cell.get_row()][cell.get_column()].set_living(False)
        self._grid = newGrid
        self.create_neighbors()

    def get_rows(self):
        return self._rows

    def get_columns(self):
        return self._columns

    def get_grid(self):
        return self._grid

    def save(self, filename):
        """
        opens the file as the basic display set and saves it as such
        :param filename: name they want to call the file
        :return:
        """
        currentDisplaySet = Cell.currentDisplaySet
        Cell.set_display('basic')
        text = self.__str__()
        Cell.set_display(currentDisplaySet)
        with open(filename, 'w') as myFile:
            myFile.write(text)

    def stop_simulation(self):
        stop = False
        currentGen = self.__str__()
        for pastGeneration in self._timeline[-3:-1]:
            if currentGen == pastGeneration:
                stop = True
        return stop


        

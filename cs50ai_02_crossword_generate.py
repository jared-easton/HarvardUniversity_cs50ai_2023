import sys
import copy
import itertools

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError
        for var in self.domains:
            removeWrds = set()
            for wrd in self.domains[var]:
                if len(wrd) != var.length:
                    removeWrds.add(wrd)
            for wrd in removeWrds:
                self.domains[var].remove(wrd) 


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        corrected = False
        lapOver = self.crossword.overlaps[x, y]
        if lapOver is not None:
            removeWrds = set()
            for x_wrd in self.domains[x]:
                charLapOver = x_wrd[lapOver[0]]
                ycharsCorresponding = {w[lapOver[1]] for w in self.domains[y]}
                if charLapOver not in ycharsCorresponding:
                    removeWrds.add(x_wrd)
                    corrected = True
            for wrd in removeWrds:
                self.domains[x].remove(wrd)

        return corrected

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError
        if arcs is None:
            next = list(itertools.product(self.crossword.variables, self.crossword.variables))
            next = [arc for arc in next if arc[0] != arc[1] and self.crossword.overlaps[arc[0], arc[1]] is not None]
        else:
            next = arcs
        while next:
            arc = next.pop(0)
            x, y = arc[0], arc[1]
            if self.revise(x, y):
                if not self.domains[x]:
                    print("ending ac3")
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    next.append((z, x))
        return True           

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #raise NotImplementedError
        if set(assignment.keys()) == self.crossword.variables and all(assignment.values()):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError
        if len(set(assignment.values())) != len(set(assignment.keys())):
            return False
        if any(var.length != len(wrd) for var, wrd in assignment.items()):
            return False
        for var, wrd in assignment.items():
            for neighbor in self.crossword.neighbors(var).intersection(assignment.keys()):
                lapOver = self.crossword.overlaps[var, neighbor]
                if wrd[lapOver[0]] != assignment[neighbor][lapOver[1]]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError
        choicesEliminated = {wrd: 0 for wrd in self.domains[var]}
        neighbors = self.crossword.neighbors(var)
        for varWrd in self.domains[var]:
            for neighbor in (neighbors - assignment.keys()):
                lapOver = self.crossword.overlaps[var, neighbor]
                for wrdN in self.domains[neighbor]:
                    if varWrd[lapOver[0]] != wrdN[lapOver[1]]:
                        choicesEliminated[varWrd] += 1
        listSorted = sorted(choicesEliminated.items(), key=lambda x:x[1])
        return  [x[0] for x in listSorted]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        varUnassigned = self.crossword.variables - assignment.keys()
        valRemaining = {var: len(self.domains[var]) for var in varUnassigned}
        valRemainingSorted = sorted(valRemaining.items(), key=lambda x: x[1])
        if len(valRemainingSorted) == 1 or valRemainingSorted[0][1] != valRemainingSorted[1][1]:
            return valRemainingSorted[0][0]
        else:
            degNum = {var: len(self.crossword.neighbors(var)) for var in varUnassigned}
            degNumSorted = sorted(degNum.items(), key=lambda x: x[1], reverse=True)
            return degNumSorted[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignTest = copy.deepcopy(assignment)
            assignTest[var] = val
            if self.consistent(assignTest):
                assignment[var] = val
                final = self.backtrack(assignment)
                if final is not None:
                    return final
            assignment.pop(var, None)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

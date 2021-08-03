import sys

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for variable in self.domains.keys():
          cur_domain = self.domains[variable].copy()
          for word in cur_domain:
            if variable.length != len(word):
              self.domains[variable].remove(word)   
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        change_occured = False
        new_domain = set()
        for x_word in self.domains[x]:
          for y_word in self.domains[y]:
            overlap = self.crossword.overlaps[x, y]
            if x_word[overlap[0]] == y_word[overlap[1]]:
              new_domain.add(x_word) 
              change_occured = True
        self.domains[x] = new_domain     


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize arcs
        if arcs == None:
          arcs = list()
          for variable in self.domains.keys():
            neighbors_set = self.crossword.neighbors(variable)
            for neighbor in neighbors_set:
              arcs.append((variable, neighbor))

        # 
        while arcs:
          (x_variable, y_variable) = arcs.pop(0)     
          if self.revise(x_variable, y_variable):
            if len(self.domains[x_variable]) == 0:
              return False
            for neighbor in self.crossword.neighbors(x_variable) - y_variable:
              arcs.append(neighbor, x_variable) 
        print("ac3")      
        for variable in self.domains.keys():
          print("domain:", variable, " ", self.domains[variable])        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment.keys()) == len(self.crossword.variables)


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        match_exists = False
        variables = assignment.keys()
        word_unique = len(assignment.values()) == len(variables)
        for variable in variables:
          if len(assignment[variable]) != variable.length:
            return False
          if variable.direction == variable.ACROSS:
            neighbors_set = self.crossword.neighbors(variable)
            for neighbor in neighbors_set:
              (i, j) = self.crossword.overlaps[variable, neighbor] 
              match_exists = False
              for word in self.domains[neighbor]:
                if assignment[variable][i] == word[j]:
                  match_exists = True
        return True and match_exists       
           

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        dict_rule_out = dict()
        # for word in self.domains[var]:
        #   neighbors_set = self.crossword.neighbors(var) - assignment.keys()  
        #   n = 0
        #   for neighbor in neighbors_set:
        #     if word in self.domains[neighbor]:
        #       n += 1
        #   if dict_rule_out.get(n, None):
        #      dict_rule_out[n] = [word]
        #   else:
        #     dict_rule_out[n].append(word)
        # values_list = list()    
        # for key in sorted(dict_rule_out.iterkeys()):
        #   values_list += dict_rule_out[key]       
        # return values_list
        return self.domains[var][0]
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        print(list(self.crossword.variables - assignment.keys()))
        return list(self.crossword.variables - assignment.keys())[0]

    def backtrack(self, assignment):
        
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.consistent(assignment) and len(assignment.keys()) == len(self.crossword.variables):
          return assignment
        variable = self.select_unassigned_variable(assignment)  
        print(variable)
        for word in self.domains[variable]:
          print(assignment)
          assignment[variable] = word
          if self.consistent(assignment):
            result = self.backtrack(assignment)
            if result != None:
              return result
            assignment.pop(variable)    
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

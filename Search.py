# -*- coding: cp1252 -*-

from utils import *
import math, random, sys, time, bisect, string
limit = 5000
size = 9

#______________________________________________________________________________
#Squelette donné par le livre, mais nous avons implanté les fonctions

class Problem(object):
    """The abstract class for a formal problem.  You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial

    #return a list of (i,j,k) where (i,j) are the coordinates of a 0 and
    #                               k is the new number we put in (i,j)
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        theActions = []
        for i in range(size):
            for j in range(size):
                if(state[i][j] == 0):
                    for k in range(1,10):
                        theActions.append((i,j,k))
        
        return theActions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        (i,j,k) = action
        res = [[0 for a in range(size)] for b in range(size)]
        for a in range(size):
            for b in range(size):
                res[a][b] = state[a][b]
        res[i][j] = k
        #ppSudokuMat(state)
        return res

    def goal_test(self, state):
        """Return True if the state is a goal."""
        allNumbers = [1,2,3,4,5,6,7,8,9]
        
        #check if each number is in each column
        for i in range(size):
            allNumb = allNumbers
            for j in range(size):
                #print self.actions(state)
                x = state[i][j]
                if(x in allNumb):
                    allNumb.remove(x)
            if(allNumb != []):
                return False
            
        #check if each number is in each line
        for i in range(size):
            allNumb = allNumbers
            for j in range(size):
                x = state[j][i]
                if(x in allNumb):
                    allNumb.remove(x)
            if(allNumb != []):
                return False
            
        #check if each number is in each box
        for a in range(0,9,3):
            for b in range (0,9,3):
                allNumb = allNumbers
                hBox = a - a % 3
                vBox = b - b % 3
                for i in range(3):
                    for j in range(3):
                        x = state[i+vBox][j+hBox]
                        if(x in allNumb):
                            allNumb.remove(x)
                if(allNumb != []):
                    return False
                
        #if we're here, all the conditions are met
        return True

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        #for the sudoku problem, the value to minimize is the number of conflicts 
        #when randomly filling the grid
        value = 0
        return value
#______________________________________________________________________________
#Vient du livre à 100%

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        update(self, state=state, parent=parent, action=action,
               path_cost=path_cost, depth=0)
        
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def expand(self, problem):
        "List the nodes reachable in one step from this node."
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        "Fig. 3.10"
        next = problem.result(self.state, action)
        return Node(next, self, action,
                    problem.path_cost(self.path_cost, self.state, action, next))

    def solution(self):
        "Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def state_hashcode(self):
        s = ""
        for i in range(size):
            for j in range(size):
                s+=str(self.state[i][j])
        return s
    
    def __hash__(self):
        return hash(self.state_hashcode())
#______________________________________________________________________________
#Uninformed Search algorithms
#Vient encore du livre, mais quelques changements à breadth_first_search(problem)

def tree_search(problem, frontier):
    """Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Don't worry about repeated paths to a state. [Fig. 3.7]"""
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def breadth_first_search(problem):
    "[Fig. 3.11]"
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = FIFOQueue()
    frontier.append(node)
    explored = set()
    compteur = 0
    stop = False
    returnVal = None
    while (frontier and not stop):
        node = frontier.pop()
        explored.add(node.state_hashcode)
        for child in node.expand(problem):
            if str(child.state_hashcode()) not in explored and child not in frontier and not stop:
                compteur = compteur+1
                if problem.goal_test(child.state):
                    ppSudokuMat(child.state)
                    return (True, compteur)
                frontier.append(child)
                if(compteur >= limit):
                    stop = True
                    returnVal = (False, compteur)
            
    return returnVal

#______________________________________________________________________________
#Other search algorithms
#Vient du livre à 100%

def recursive_best_first_search(problem, h=None):
    "[Fig. 3.26]"
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0   # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            successors.sort(lambda x,y: cmp(x.f, y.f)) # Order by lowest f value
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    return result

def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Fig. 4.2]"""
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        #min instead of max
        neighbor = argmin_random_tie(neighbors,
                                     lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor
    return current.state

#_______________________________________________________________________________
#Vient de nous à 100%


def isLegalInRow(config,line,col,num):
    for i in range(size):
        if(config[line][i] == num):
            return False
    return True

def isLegalInCol(config,line,col,num):
    for i in range(size):
        if(config[i][col]  == num):
            return False
    return True
    
def isLegalInBox(config,line,col,num):
    hBox = col - col % 3
    vBox = line - line % 3
    for i in range(3):
        for j in range(3):
            if(config[i+vBox][j+hBox] == num):
                return False
    return True
    
def isLegal(config,line,col,num):
    return (isLegalInRow(config,line,col,num) and 
            isLegalInCol(config,line,col,num) and 
            isLegalInBox(config,line,col,num))
    
def getPossibleNumbers(config,line,col):
    possibleNumbers = [1,2,3,4,5,6,7,8,9]
    
    for i in range(size):
        x = config[line][i]
        if(x in possibleNumbers):
            possibleNumbers.remove(x)
            
    for i in range(size):
        x = config[i][col]
        if(x in possibleNumbers):
            possibleNumbers.remove(x)
    
    hBox = col - col % 3
    vBox = line - line % 3
    
    for i in range(3):
        for j in range(3):
            x = config[i+vBox][j+hBox]
            if(x in possibleNumbers):
                possibleNumbers.remove(x)
                
    return possibleNumbers

#params: nom du fichier
#return: allConfigs, un tableau de configs. C'est-à-dire un tableau de tableau 9x9
#return: allProblems, un tableau de problemes
def readConfigs(filename):
    allLines =  [line.rstrip('\n') for line in open(filename)]
    allConfigs = []
    allProblems = []
    
    for line in allLines:
        i = j = 0
        aConfig = [[0 for a in range(size)] for b in range(size)]
        for x in line:
            aConfig[i][j] = int(x) #fill the matrix column by column
            j += 1
            if(j % size == 0):
                i += 1
                j = 0
        allConfigs.append(aConfig)
        aProblem = Problem(aConfig)
        allProblems.append(aProblem)
        
    return allProblems         

def ppSudokuMat(config):
    for i in range(size):
        if(i % 3 == 0):
            print "|-----------------------|"
        for j in range(size):
            if(j % 3 == 0):
                print "|",
            print config[i][j],
        print "|\n",
    print "-------------------------"

if __name__ == '__main__':
    import time
    initProblem = readConfigs('100sudoku.txt')
    dfProblems = list(initProblem) #clone the configurations to avoid altering them
#   ppSudokuMat(dfConfigs[0])
    start = time.time()
    complete = 0
    compteur = 0
    for prob in dfProblems[:10]:#mettre le nombre de config qu'on veut résoudre
        compteur += 1
        print compteur
        #ppSudokuMat(prob.initial)
        res = hill_climbing(prob)
        print res
        #result = depthFirst(conf) #work on the copy
        #if(not timeout):
        #    complete += 1
        #    ppSudokuMat(conf)
    print time.time()-start
    

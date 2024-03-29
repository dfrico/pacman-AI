# pacmanMdp.py
# IA UC3M 2016
# -----------------------
##
from game import GameStateData
from game import Game
from game import Actions
from util import nearestPoint
import util, layout
import sys, types, time, random, os

import mdp
from featureExtractors import *

class PacmanMdp(mdp.MarkovDecisionProcess):
    """
      pacman MDP
    """
    def __init__(self, extractor='StateExtractor'):
        # Feature extractor
        self.featExtractor = util.lookup(extractor, globals())()

        # Transition function (data structure required for the transition function)
        #*** YOUR CODE STARTS HERE ***"
        # Code to remove ---------- from here
        self.frequencies = util.Counter()
        # Code to remove ---------- to here
        #"*** YOUR CODE FINISHES HERE ***"


        # Dictionary with examples of a Low state for each High state: it serves to get possible actions
        # and to check terminal states (though it is not required if the high level representation
        # capture them)
        self.states = util.Counter()

        # Reward for each state at the high level representation
        self.reward = util.Counter()

    def stateToHigh(self, stateL):
        """
          Returns the high level representation of an state

        """
        return tuple(self.featExtractor.getFeatures(stateL).values())

    def addStateLow(self, stateH, stateL):
        """
          Adds a new pair stateH stateL to the dictionary of states

        """
        # print "Added", stateH
        if not stateH in self.states.keys():
            self.states[stateH] = stateL
            self.reward[stateH] = [1, [stateL.getScore()]]
        else:
            self.reward[stateH][0] += 1
            self.reward[stateH][1].append(stateL.getScore())


    def updateTransitionFunction(self, stateL, action, nextStateL):
        """
          Updates the transition function with a new case stateL, action, nextStateL

          The states received as parameters have a low level representation. The transition function
          should be stored over the high level (simplified) representation

        """
        # Change the representation to the simplified one
        state = self.stateToHigh(stateL)
        nextState= self.stateToHigh(nextStateL)

        # Set the start state in the first call
        if len(self.states.keys())== 0:
            self.setStartState(state)

        # Add the received states to self.states
        self.addStateLow(state, stateL)
        self.addStateLow(nextState, nextStateL)

        # util.raiseNotDefined()
        #"*** YOUR CODE STARTS HERE ***"
        # state, action as tuple as KEY of 1st dict
        if self.frequencies.has_key(state):
            if self.frequencies[state].has_key(action):
                if self.frequencies[state][action].has_key(nextState):
                    self.frequencies[state][action][nextState] += 1
                else:
                    self.frequencies[state][action][nextState] = 1
            else:
                self.frequencies[state][action] = util.Counter()
                self.frequencies[state][action][nextState] = 1
        else:
            self.frequencies[state] = util.Counter()
            self.frequencies[state][action] = util.Counter()
            self.frequencies[state][action][nextState] = 1


        #"*** YOUR CODE FINISHES HERE ***"

    def getPossibleActions(self, state):
        """
        Returns list of valid actions for 'state'.

        Note that you can request moves into walls and
        that "exit" states transition to the terminal
        state under the special action "done".
        """
        if not state in self.states.keys():
            return []
        return (self.states[state]).getLegalActions(0)

    def getStates(self):
        """
        Return list of all states.
        """
        return self.states.keys()

    def isKnownState(self, state):
        """
        True if the state is in the dict of states.
        """
        return state in self.states.keys()

    def getAverageReward(self, state):
        """
        Return average rewards of the known low level states represented by a high level state
        """
        return sum(i for i in  self.reward[state][1])/self.reward[state][0]

    def getReward(self, state, action, nextState):
        """
        Get reward for state, action, nextState transition.

        """
        return self.getAverageReward(nextState) - self.getAverageReward(state)

    def setStartState(self, state):
        """
        set for start state
        """
        self.startState = state

    def getStartState(self):
        """
        get for start state
        """
        return self.startState

    def isTerminal(self, state):
        """
        Pacman terminal states
        """
        if not state in self.states.keys():
            return self.featExtractor.isTerminalFeatures(state)
        else:
            return self.states[state].isLose() or self.states[state].isWin()

    def printMdp( self ):
        """
        Shows the transition function of the MDP
        """
        for state in self.states.keys():
            for action in self.getPossibleActions(state):
                print state, action, self.getTransitionStatesAndProbabilities(state, action)

    def getTransitionStatesAndProbabilities(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        if action not in self.getPossibleActions(state):
            raise "Illegal action!"

        if self.isTerminal(state):
            return []

        successors = []

        # util.raiseNotDefined()
        #"*** YOUR CODE STARTS HERE ***"
        total = 0

        if self.frequencies.has_key(state) and self.frequencies[state].has_key(action):
            # ss = simplified state, aka number of times pacman did an action from a state.
            for sstate in self.frequencies[state][action]:
                total += self.frequencies[state][action][sstate]
            for sstate in self.frequencies[state][action]:
                successors.append((sstate, (self.frequencies[state][action][sstate])/total))

        #"*** YOUR CODE FINISHES HERE ***"

        return successors

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 19:39:27 2018

@author: Aidin
"""


from __future__ import print_function, division
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future


import numpy as np
import matplotlib.pyplot as plt

LEN = 3

    

class Environment:
    def __init__(self):
        self.board = np.zeros((LEN,LEN))
        self.x = -1
        self.o = 1
        self.ended = False
        self.winner = None
        self.totalStates = 3**(LEN*LEN)
        
    def isEmpty(self,i , j):
        return self.board[i,j] == 0 
    
    def reward(self, symbol):
        if not self.gameOver():
            return 0
        return 1 if self.winner == symbol else 0
    
    def getState(self):
        pos = 0
        num = 0
        for i in range(LEN):
            for j in range(LEN):
                if self.board[i,j] == 0:
                    val = 0
                elif self.board[i,j] == self.x:
                    val = 1
                elif self.board[i,j] == self.o:
                    val = 2
                num += (3**pos)*val
                pos += 1
        return num
        
    def gameOver(self, forceRecalculate = False):
        if not forceRecalculate  and self.ended:
            return self.ended
        
        for i in range(LEN):
            for player in (self.x,self.o):
                if self.board[i].sum() ==player*LEN:
                    self.winner = player
                    self.ended = True
                    return True
        for j in range(LEN):
            for player in (self.x,self.o):
                if self.board[:j].sum() ==player*LEN:
                    self.winner = player
                    self.ended = True
                    return True
        for player in (self.x, self.o):
            if self.board.trace() == player*LEN:
                self.winner = player
                self.ended = True
                return True
            if np.fliplr(self.board).trace() == player*LEN:
                self.winner = player
                self.ended = True
                return True
        if np.all((self.board == 0) == False):
            self.winner = None
            self.ended = True
            return True
        self.winner = None
        return False


    def drawGame(self):
        for i in range(LEN):
            print ("-------------")
            for j in range(LEN):
                print("  ", end="")
                if self.board[i,j] == self.x:
                    print ("x", end="")
                elif self.board[i,j] == self.o:
                    print ("o", end="")
                else:
                    print (" ", end="")
            print ("")
        print ("-------------")
    

class Agent:
    def __init__(self,eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.stateHistory = []
    
    def setValue(self,V):
        self.V = V
    
    def setSymbol(self,symbol):
        self.symbol = symbol
    
    def setVerbose(self,Verbose):
        self.Verbose = Verbose
        
    def resetHistory(self):
        self.stateHistory = []
    
    def takeAction(self,environment):
        
        random = np.random.rand()
        maxState = None
        if random < self.eps:
            if self.verbose:
                print ("Taking a random action")
                
            possibleMoves = []
            for i in range(LEN):
                for j in range(LEN):
                    if environment.isEmpty(i,j):
                        possibleMoves.append((i,j))
            index = np.random.choice((len(possibleMoves)))
            nextMove = possibleMoves[index]
        else:
            pos2value = {}
            nextMove = None
            maxValue = -1
            for i in range(LEN):
                for j in range(LEN):
                    if environment.isEmpty(i,j):
                        environment.board[i,j] = self.symbol
                        state = environment.getState()
                        environment.board[i,j] = 0
                        pos2value[(i,j)] = self.V[state]
                        if self.V[state]>maxValue:
                            maxValue = self.V[state]
                            maxState = state
                            nextMove = (i,j)
                            
            if self.verbose:
                print ("Taking a greedy action")
                for i in range(LEN):
                    print ("-----------------------")
                    for j in range(LEN):
                        if environment.isEmpty(i,j):
                            print ("%.2f|" % pos2value[(i,j)])
                        else:
                            print (" ")
                            if environment.board[i,j] == environment.x:                              
                                print ("x |")
                            elif environment.board[i,j] == environment.o:  
                                print ("o |")
                            else:
                                print (" |")
                    print ("")
                print ("-----------------------")
            environment.board[nextMove[0], nextMove[1]] = self.symbol
                
    def updateStateHistory(self,s):
        self.stateHistory.append(s)
    
    
    def update(self,environment):
        reward = environment.reward(self.symbol)
        target = reward
        for prev in reversed(self.stateHistory):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.resetHistory()
        
        
class Human:
    def __init__(self):
        pass
    
    def setSymbol(self,symbol):
        self.symbol = symbol
        
    def takeAction(self, environment):
        while True:
            
            move = input("Enter coordinates i,j for your next move (i,j=0,1,2):")
            i,j = move.split(',')
            i = int(i)
            j = int(j)
            
            if environment.isEmpty(i,j):
                environment.board[i,j] = self.symbol
                break
    
    def update(self,environment):
        pass
    def updateStateHistory(self,s):
        pass
    
    

def getStateHashAndWinner(env, i=0, j=0):
  results = []

  for v in (0, env.x, env.o):
    env.board[i,j] = v # if empty board it should already be 0
    if j == 2:
      # j goes back to 0, increase i, unless i = 2, then we are done
      if i == 2:
        # the board is full, collect results and return
        state = env.getState()
        ended = env.gameOver(forceRecalculate=True)
        winner = env.winner
        results.append((state, winner, ended))
      else:
        results += getStateHashAndWinner(env, i + 1, 0)
    else:
      # increment j, i stays the same
      results += getStateHashAndWinner(env, i, j + 1)

  return results


def initialVx(env, state_winner_triples):
  V = np.zeros(env.totalStates)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.x:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


def initialVo(env, state_winner_triples):
  V = np.zeros(env.totalStates)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.o:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


def play(player1, player2,environment, draw = False):
    currentPlayer = None
    while not environment.gameOver():
        if currentPlayer == player1:
            currentPlayer = player2
        else:
            currentPlayer = player1
            
        if draw:
            if draw == 1 and currentPlayer == player1:
                environment.drawGame()
            if draw == 2 and currentPlayer == player2:
                environment.drawGame()
        currentPlayer.takeAction(environment)
        
        state = environment.getState()
        player1.updateStateHistory(state)
        player2.updateStateHistory(state)
        
    if draw:
        environment.drawGame()
    
    player1.update(environment)
    player2.update(environment)
 
    


if __name__ == '__main__':
    player1 = Agent()
    player2 = Agent()
    
    
    env = Environment()
    stateWinner = getStateHashAndWinner(env)
    
    
    Vx = initialVx(env,stateWinner)
    player1.setValue(Vx)
    Vo = initialVo(env,stateWinner)
    player2.setValue(Vo)
    
    player1.setSymbol(env.x)
    player2.setSymbol(env.o)
    
T = 1000
for t in range(T):
    if t % 200 == 0:
      print(t)
    play(player1, player2, Environment())


human = Human()
human.setSymbol(env.o)

while True:
    player1.setVerbose(True)
    play(player1, human, Environment(), draw = 2)
    
    answer = input("Play again? [Y/n]: ")
    
    if answer and answer.lower()[0] == 'n':
        break
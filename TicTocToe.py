# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 19:39:27 2018

@author: Aidin
"""



def play(player1, player2,environment, draw = False):
    currentPlayer = None
    while not environment.over():
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
        player1.updateState(state)
        player2.updateState(state)
        
    if draw:
        environment.drawGame()
    
    player1.update(environment)
    player2.update(environment)
    
    
    

def environment:
    def __init__(self):
        self.board = np.zeros(LEN,LEN)
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
        return 1 if self.winner = sym else 0
    
    def getState(self):
        pos = 0
    num = 0
    for i in xrange(Len):
        for j in xrange(Len):
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
    
    for i in xrange(LEN):
        for player in (self.x,self.o):
            if self.board[i].sum() ==player*LEN:
                self.winner = player
                self.ended = True
                return True
    for j in xrange(LEN):
        for player in (self.x,self.o):
            if self.board[:j].sum() ==player*LEN:
                self.winner = player
                self.ended = True
                return True
    for player in (self.x, self.o):
        if self.board.trace() = player*LEN:
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
    self.winner = None
    return False


    drawBoard():
    
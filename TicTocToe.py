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
    
    
def state2num(self):
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
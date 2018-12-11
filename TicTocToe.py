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
    
    
    

class environment:
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
            return True
        self.winner = None
        return False


    def drawBoard():
        for i in xrange(LEN):
            print "-----------------------"
            for j in xrange(LEN):
                print " ",
                if self.board[i,j] = self.x:
                    print "x",
                elif self.board[i,j] = self.o:
                    print "o",
                else:
                    print " ",
            print ""
        print "-----------------------"
    

class Agent:
    def __init__(self,eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.state_history = []
    
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
                print "Taking a random action"
                
            possibleMoves = []
            for i in xrange(LEN):
                for j in xrange(LEN):
                    if environment.isEmpty(i,j):
                        possible_moves.append((i,j))
            index = np.random.choice((len(possible_moves)))
            nextMove = possibleMoves[index]
        else:
            pos2value = {}
            nextMove = None
            maxValue = -1
            for i in xrange(LEN):
                for j in xrange(LEN):
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
                print "Taking a greedy action"
                for i in xrange(LEN):
                    print "-----------------------"
                    for j in xrange(LEN):
                        if environment.isEmpty(i,j):
                            print "%.2f|" % pos2value[(i,j)]
                        else:
                            print " ",
                            if environment.board[i,j] = environment.x:                              
                                print "x |",
                            elif environment.board[i,j] = environment.o:  
                                print "o |",
                            else:
                                print " |",
                    print ""
                print "-----------------------"
    
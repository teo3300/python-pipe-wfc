#!/usr/bin/python

from operator import le
import os
import random

try: t_width = os.get_terminal_size().columns
except: t_width = 100
try: t_height = os.get_terminal_size().lines
except: t_height = 100

def en(bits):
    return int(bits, 2)

all_pipes = [
    [' ' , en('0000')],
    ['─' , en('0011')],
    ['┌' , en('0101')],
    ['┐' , en('0110')],
    ['┬' , en('0111')],
    ['└' , en('1001')],
    ['┘' , en('1010')],
    ['┴' , en('1011')],
    ['│' , en('1100')],
    ['├' , en('1101')],
    ['┤' , en('1110')],
    ['┼' , en('1111')]]

class Tile():

    __content = 'X'
    __neighbours = en('0000')

    def content(self):
        return self.__content

    def empty(self):
        return self.__content == 'x'

    def __init__(self):
        self.__content = 'x'
        self.__neighbours = 0
    
    def set(self, val):
        self.__content = val[0]
        self.__neighbours = val[1]
    
    def cN(self):
        return self.__neighbours & en('1000')
    def cS(self):
        return self.__neighbours & en('0100')
    def cW(self):
        return self.__neighbours & en('0010')
    def cE(self):
        return self.__neighbours & en('0001')

class Mat:
    def __init__(self, width, height, char_set):
        self.__width = width
        self.__height = height
        self.__char_set = char_set
        self.__vals = [Tile() for _ in range(width * height)]
    
    def toStr(self):
        ret = ''
        for i in range(0, self.__width * self.__height, self.__width):
            ret += str(''.join([self.__vals[j].content() for j in range(i, i+self.__width)]))
            if(i < self.__width * self.__height):   ret += '\n'
        return ret

    def get(self, i, j):
        ti = (self.__height + i) % self.__height
        tj = (self.__width + j) % self.__width
        return self.__vals[ti*self.__width + tj]

    def getN(self, i, j):
        return self.get(i-1, j)

    def getS(self, i, j):
        return self.get(i+1, j)

    def getW(self, i, j):
        return self.get(i, j-1)

    def getE(self, i, j):
        return self.get(i, j+1)

    def set(self, i, j, val):
        self.__vals[i*self.__width + j].set(val)

    def getAvails(self,i,j):
        availables = self.__char_set
        if not self.getN(i,j).empty():
            availables = list(filter(lambda x: (not (bool(x[1] & en('1000')) ^ bool(self.getN(i,j).cS()))), availables))
        if not self.getS(i,j).empty():
            availables = list(filter(lambda x: (not (bool(x[1] & en('0100')) ^ bool(self.getS(i,j).cN()))), availables))
        if not self.getW(i,j).empty():
            availables = list(filter(lambda x: (not (bool(x[1] & en('0010')) ^ bool(self.getW(i,j).cE()))), availables))
        if not self.getE(i,j).empty():
            availables = list(filter(lambda x: (not (bool(x[1] & en('0001')) ^ bool(self.getE(i,j).cW()))), availables))
        return availables

    def fill(self):
        for i in range(self.__height):
            for j in range(self.__width):
                avail = self.getAvails(i,j)
                if(len(avail) > 0):
                    self.set(i,j, avail[random.randint(0, len(avail)-1)])
                else:
                    self.set(i,j,['x',0])

if __name__ == '__main__':

    set_copy = all_pipes
    subset_size = random.randint(1, len(set_copy)-1)
    random_subset = [ set_copy.pop(random.randint(0, len(set_copy)-1)) for i in range(subset_size)]

    m = Mat(t_width, t_height, random_subset)
    m.fill()
    print(m.toStr())

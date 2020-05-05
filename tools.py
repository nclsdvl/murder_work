# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:23:25 2020

@author: MonOrdiPro
"""

def get_row_col (i) :
    if i < 5 :
        row = 1
        col = i+1
    elif i < 10 :
        row=2
        col= (i%5) +1
    elif i < 15 :
        row=3
        col= (i%5) +1
    elif i < 20 :
        row=4
        col= (i%5) +1
    elif i < 25 :
        row=5
        col= (i%5) +1
    elif i < 30 :
        row=6
        col= (i%5) +1
    elif i < 35 :
        row=7
        col= (i%5) +1 
        
    return (row, col) 
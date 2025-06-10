from tkinter import *
from math import sqrt


def inp_eval():
    global x
    x = inp.get()
    y = eval(x)
    inp.delete(0, 'end') 
    inp.insert(0, str(y))

def clear():
    inp.delete(0, 'end')  

def ins(a):
    p = inp.get()
    inp.insert(len(p), a) 

def sr():
    global x
    x = inp.get()
    y = eval(str(sqrt(int(x))))
    inp.delete(0, 'end') 
    inp.insert(0, str(y))

win = Tk()
win.geometry('200x100')
inp = Entry(win)
inp.bind('<Return>', (lambda event: inp_eval()))

q = Button(win, text = 'exit', command = quit,height=1, width=7)
c = Button(win, text = 'clear', command = clear,height=1, width=7)

b1 = Button(win, text = '1', command = (lambda: ins('1')),height=1, width=7)
b2 = Button(win, text = '2', command = (lambda: ins('2')),height=1, width=7)
b3 = Button(win, text = '3', command = (lambda: ins('3')),height=1, width=7)
b4 = Button(win, text = '4', command = (lambda: ins('4')),height=1, width=7)
b5 = Button(win, text = '5', command = (lambda: ins('5')),height=1, width=7)
b6 = Button(win, text = '6', command = (lambda: ins('6')),height=1, width=7)
b7 = Button(win, text = '7', command = (lambda: ins('7')),height=1, width=7)
b8 = Button(win, text = '8', command = (lambda: ins('8')),height=1, width=7)
b9 = Button(win, text = '9', command = (lambda: ins('9')),height=1, width=7)
b0 = Button(win, text = '0', command = (lambda: ins('0')),height=1, width=7)
plus = Button(win, text = '+', command = (lambda: ins('+')),height=1, width=7)
minus = Button(win, text = '-', command = (lambda: ins('-')),height=1, width=7)
mul = Button(win, text = 'x', command = (lambda: ins('*')),height=1, width=7)
div = Button(win, text = '/', command = (lambda: ins('/')),height=1, width=7)
power = Button(win, text = '^', command = (lambda: ins('**')),height=1, width=7)
p1 = Button(win, text = '(', command = (lambda: ins('(')),height=1, width=7)
p1 = Button(win, text = ')', command = (lambda: ins(')')),height=1, width=7)
eq = Button(win, text = '=', command = (lambda: inp_eval()),height=1, width=7)
dc = Button(win, text = '.', command = (lambda: ins('.')),height=1, width=7)
sqot = Button(win, text = 'sqrt', command = (lambda: sr()),height=1, width=7)

inp.grid(columnspan=4, ipadx=70)
c.grid(row= 7, column = 2)
q.grid(row= 8, column = 0)
sqot.grid(row = 8, column = 1)
b1.grid(row= 2, column = 0)
b2.grid(row= 2, column = 1)
b3.grid(row= 2, column = 2)
b4.grid(row= 3, column = 0)
b5.grid(row= 3, column = 1)
b6.grid(row= 3, column = 2)
b7.grid(row= 4, column = 0)
b8.grid(row= 4, column = 1)
b9.grid(row= 4, column = 2)
b0.grid(row= 5, column = 0)
plus.grid(row= 5, column = 1)
minus.grid(row= 5, column = 2)
mul.grid(row= 6, column = 0)
div.grid(row= 6, column = 1)
power.grid(row= 6, column = 2)
eq.grid(row= 7, column = 0)
dc.grid(row= 7, column = 1)

win.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:11:45 2015

@author: pi
"""

import Tkinter as tk
from driver import RGBLED
import socket
from time import sleep, time


#RGB=RGBLED(11, 13)    
 
def sockwrite(values):
    sock=socket.socket()
    sock.connect(("localhost", 5557))
    sock.sendall(",".join([str(i) for i in values]))
    sock.close()
 
def changeRGB():
    x=getsliders()
    RGB.SetColor(x[0], x[1], x[2], x[3])
    
def writeRGB(name="last.csv"):
    x=getsliders()
    with open(name, "w") as phil:
        phil.write(", ".join(map(str, x)))
        
def readRGB(name):
    with open(name) as phil:
        line=phil.readline()
    vals=map(int,line.split(", "))
    return vals
    
def loadRGB(name="last.csv"):
    vals=readRGB(name)
    setsliders(vals)
    sockwrite(vals)

    

def getsliders():
    return [Rslider.get(), Gslider.get(), Bslider.get(), Islider.get()]
    
def setsliders(x):
    Rslider.set(x[0])
    Gslider.set(x[1])
    Bslider.set(x[2])
    Islider.set(x[3])
   
def rgbi_to_hex(rgbi):
    rgb=[int(rgbi[3]*i*255/10000) for i in rgbi[0:3]]
    rgb=["%02x"%(i) for i in rgb]
    return "#"+"".join(rgb)
    
def get_button_set_func(button_ind):
    
    def button_set():
        global mem_buttons, memory, setmode
        if setmode:
            rgbi=getsliders()
            writeRGB(name="Memory%u.csv"%button_ind)
            memory[button_ind]=rgbi
            hexx=rgbi_to_hex(rgbi)
            mem_buttons[button_ind].config(bg=hexx, activebackground=hexx)
            toggle_setmode()
        else:
            setsliders(memory[button_ind])
            sockwrite(memory[button_ind])
            
        
    return button_set
    
def toggle_setmode():
    global setmode, mem_set_button
    if setmode:
        setmode=False
        mem_set_button.config(bg="white", activebackground="white")
    else:
        setmode=True
        mem_set_button.config(bg="red", activebackground="red")
    
window=tk.Tk()
window.resizable(width=False, height=False)
window.minsize(800, 400)
window.maxsize(800, 400)
base_frame=tk.Frame(window)
base_frame.pack(fill=tk.X, expand=True)

Rframe=tk.Frame(base_frame, bg="red")
Rslider=tk.Scale(Rframe, from_=100, to=0, bg="red", bd=0, highlightthickness=0)
Rlabel=tk.Label(Rframe, text="Red", bg="red")
Rslider.pack()
Rlabel.pack()

Gframe=tk.Frame(base_frame, bg="green")
Gslider=tk.Scale(Gframe, from_=100, to=0, bg="green", bd=0, highlightthickness=0)
Glabel=tk.Label(Gframe, text="Green", bg="green")
Gslider.pack()
Glabel.pack()

Bframe=tk.Frame(base_frame, bg="blue")
Bslider=tk.Scale(Bframe, from_=100, to=0, bg="blue", fg="white", bd=0, highlightthickness=0)
Blabel=tk.Label(Bframe, text="Blue", bg="blue", fg="white")
Bslider.pack()
Blabel.pack()

Iframe=tk.Frame(base_frame, bg="white")
Islider=tk.Scale(Iframe, from_=100, to=0, bg="white", bd=0, highlightthickness=0)
Ilabel=tk.Label(Iframe, text="Intensity", bg="white")
Islider.pack()
Ilabel.pack()

try:
    loadRGB()
except Exception as e:
    print e

last=getsliders()

Sframe=tk.Frame(base_frame)
Scanvas=tk.Canvas(Sframe, width=160, height=160)
color_oval=Scanvas.create_oval([20, 20, 140, 140], fill=rgbi_to_hex(last))
color_boarder=Scanvas.create_oval([20, 20, 140, 140], fill="", width=10)
Scanvas.pack()

memory_frame_top=tk.Frame(window)
memory=[]
for i in range(10):
    try:
        mem=readRGB("Memory%u.csv"%i)
    except:
        mem=[100, 100, 100, 100]
    memory.append(mem)
mem_buttons=[]
for ind, color in enumerate(memory):
    cb=get_button_set_func(ind)
    mem_button=tk.Button(memory_frame_top, bg=rgbi_to_hex(color), activebackground=rgbi_to_hex(color), command=cb, text="Mem%u"%(ind+1))
    mem_buttons.append(mem_button)
    mem_button.pack(side=tk.LEFT)

setmode=False    
mem_set_button=tk.Button(memory_frame_top, bg="white", activebackground="white", text="Memory Set", command=toggle_setmode)
mem_set_button.pack(side=tk.LEFT)


Rframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
Gframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
Bframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
Iframe.pack(side=tk.LEFT, fill=tk.X, expand=True)
Sframe.pack()
memory_frame_top.pack()

control_frame=tk.Frame(window)
control_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

writenext=False
lastwrite=time()


while True:
    current=getsliders()
    if current!=last:
        last=current
        sockwrite(current)
        writenext=True
        Scanvas.itemconfig(color_oval, fill=rgbi_to_hex(current))
    elif writenext and time()-lastwrite>5:
        writenext=False
        lastwrite=time()
        writeRGB()
        
    
    window.update()
    sleep(0.00001)
        
            
            
        


from turtle import *
from datetime import datetime

L = 30

x_offset = -220
x_dist = 3*L
y_offset = 150
delay_time = 0
dark_mode = True


turi = Turtle()
turi.hideturtle()
turi.speed(0)
screen = turi.getscreen()

myblue = "blue"
col_symb_0 = "gray"
if dark_mode:
    turi.getscreen().bgcolor("black")
    turi.clear()
    myblue = "blue"
    col_symb_0 = "white"

def decimal_to_binary(z):
    binary = ""
    while(z >= 1):
        binary = str(z%2) + binary
        z = z//2
    while len(binary) < 6:
        binary = "0"+binary
    return binary

def draw_circle(x,y,col,width):
    turi.pencolor(col)
    turi.width(width)
    turi.teleport(x,y+L)
    turi.setheading(0)
    turi.circle(L,360)

def draw_cross(x,y,col,width):
    turi.pencolor(col)
    turi.width(width)
    turi.teleport(x-L,y-L)
    turi.setheading(45)
    turi.forward(L*2*1.41)
    turi.teleport(x+L,y-L)
    turi.setheading(135)
    turi.forward(L*2*1.41)

def draw_square(x,y,col,width):
    turi.pencolor(col)
    turi.width(width)
    turi.teleport(x-L,y-L)
    turi.setheading(0)
    for _ in range(4):
        turi.forward(2*L)
        turi.right(90)

def replace_char_at_index(s,c,i):
    # replace char at index i in string with char c
    return s[:i] + c + s[i+1:]

h_bin_prev = "xxxxxx"
m_bin_prev = "xxxxxx"
s_bin_prev = "xxxxxx"

while True:
    screen.tracer(0, 0)
    now = datetime.now()
    h = now.hour
    m = now.minute
    s = now.second
    h_bin = decimal_to_binary(h)
    m_bin = decimal_to_binary(m)
    s_bin = decimal_to_binary(s)

    for i in range(6):
        if i > 0 and h_bin[i] != h_bin_prev[i]:
            h_bin_prev = replace_char_at_index(h_bin_prev,h_bin[i], i)
            if h_bin[i] == "1":
                draw_circle(x_offset+i*x_dist,y_offset,"red",5)
            else:
                draw_circle(x_offset+i*x_dist,y_offset,col_symb_0,5)            

        if m_bin[i] != m_bin_prev[i]:
            m_bin_prev = replace_char_at_index(m_bin_prev,m_bin[i], i)
            if m_bin[i] == "1":
                draw_cross(x_offset+i*x_dist,0,myblue,5)
            else:
                draw_cross(x_offset+i*x_dist,0,col_symb_0,5)
    
        if s_bin[i] != s_bin_prev[i]:
            s_bin_prev = replace_char_at_index(s_bin_prev,s_bin[i], i)
            if s_bin[i] == "1":
                draw_square(x_offset+i*x_dist,-y_offset,"green",5)
            else:
                draw_square(x_offset+i*x_dist,-y_offset,col_symb_0,5)
    screen.update()
            
    #print("{0}:{1}:{2}".format(h,m,s))

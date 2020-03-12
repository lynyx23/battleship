import random
import string
import numpy as np
from termcolor import colored,cprint

size=30

# Create matrixes filled with zeros
# a is the hidden matrix
# b is the matrix viewed by the player
# c is used to check the game state
a=np.zeros((size,size),dtype=np.int32)
b=np.zeros((size,size),dtype=np.int32)
c=np.zeros((size,size),dtype=np.int32)


# Relative position arrays
dx=[1,0,-1,0]
dy=[0,-1,0,1]

# 0 - down
# 1 - left
# 2 - up
# 3 - right

# Clears console
def cls():
    print ("\n" * 100)

# Split string in char array
def split(word):
    return [char for char in word]

# Delete chars in a string from a string - some kind of strip()
def clean(s,list):
    s=s.translate({ord(c): None for c in list})
    return s

# Deletes spaces from a char array
def space(a):
    for it in range(0,len(a)):
        for i in range(0,len(a)):
            if i==len(a):
                break
            if a[i]==" ":
                for j in range(i+1,len(a)):
                    a[j-1]=a[j]
                a.pop()

# Tests if every point of the ship can fit in the matrix
def test1(lg,x,y,dir):
    ok=1
    xx=dx[dir]
    yy=dy[dir]
    if x+xx*(lg-1)>=size or x+xx*(lg-1)<0 or y+yy*(lg-1)>=size or y+yy*(lg-1)<0:
        ok=0
    return ok

# Checks if there are any ship collisions
def test2(lg,x,y,dir):
    ok=1
    xx=dx[dir]
    yy=dy[dir]
    for j in range(1,lg):
        valx=x+xx*j
        valy=y+yy*j
        if a[valx][valy]!=0:
            ok=0
    return ok

# Generates a valid ship and places it in a
def gen(count,lg):
    for it in range(0,count):
        found=0
        while found==0:
            x1=random.randint(lg,size-1-lg)
            y1=random.randint(lg,size-1-lg)
            if a[x1][y1]==0:
                d=[0,1,2,3]
                random.shuffle(d)
                for i in range(0,4):
                    if test1(lg,x1,y1,d[i])==1:
                        if test2(lg,x1,y1,d[i])==1:
                            for j in range(0,lg):
                                valx=x1+dx[d[i]]*j
                                valy=y1+dy[d[i]]*j
                                #    print(valx,valy)
                                a[valx][valy]=lg
                        break
                if a[x1][y1]==lg:
                    found==1
                    break

def win_test():
    ok=0
    for row in range(0,size):
        for col in range(0,size):
            if a[row][col]!=0:
                if c[row][col]==0:
                    ok=1
                    break
        if ok==1:
            break
    return ok

# Prints final matrix
def matrix_print_c(m):
    cprint("  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 26 28 29","cyan")
    #Printing the matrix with associated colors for ships
    for row in range(0,size):
        x=np.array2string(m[row])
        x=clean(x,"[ ]")
        z=split(x)
        it=0
        for char in z:
            it+=1
            if it==1:
                if row<10:
                    cprint('0'+str(row),"cyan",end=' ')
                else:
                    cprint(row,"cyan",end=' ')
            if it==size:
                if char!='0':
                    cprint(char,"green",end='\n')
                else:
                    print(char,end='\n')
            else:
                if char!='0':
                    cprint(char,"green",end='  ')
                else:
                    print(char,end='  ')

# Print matrix viewed by player
def matrix_print(m):
    cprint("  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 26 28 29","cyan")
    #Printing the matrix with associated colors for ships
    for row in range(0,size):
        x=np.array2string(m[row])
        x=clean(x,"[]")
        z=split(x)
        space(z)
        it=0
        for char in z:
            it+=1
            if it==1:
                if row<10:
                    cprint('0'+str(row),"cyan",end=' ')
                else:
                    cprint(row,"cyan",end=' ')
            if it==size:
                if char=='8':
                    cprint('o',"yellow",end='\n')
                elif char=='9':
                    cprint('x',"red",end='\n')
                else:
                    print(char,end='\n')
            else:
                if char=='8':
                    cprint('o',"yellow",end='  ')
                elif char=='9':
                    cprint('x',"red",end='  ')
                else:
                    print(char,end='  ')

# Tests if the input is valid
def test3(a):
    if len(a)<3:
        return 0
    if a=="win":
        return 1
    if a.find(' ')==-1:
        return 0
    for c in a:
        if c!=" ":
            if c.isdigit()==0:
                return 0
                break
    sep=a.find(' ')
    x=a[:sep]
    y=a[sep+1:]
    x=int(x)
    y=int(y)
    if x>=size or x<0 or y>=size or y<0:
        return 0
    return 1

# Game logic
def game():
    gen(3,5)
    gen(5,4)
    gen(6,3)
    gen(8,2)
    cls()
    matrix_print(b)
    won=0
    while won==0:
        if win_test()==0 | won==1:
            print(colors.lightgreen+"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ You've Won!! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            matrix_print_c(a)
            print(colors.lightgreen+"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ You've Won!! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",colors.reset)
            won=1
            break
        else:
            valid=0
            while valid==0:
                coords=input(colors.green+"Type in your guess (x y): ")
                if test3(coords)==1:
                    valid=1
                    break
            if coords=="win":
                print(colors.lightgreen+"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ You've Won!! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                matrix_print_c(a)
                print(colors.lightgreen+"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ You've Won!! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",colors.reset)
                won=1
                break
            sep=coords.find(' ')
            x=coords[:sep]
            y=coords[sep+1:]
            x=int(x)
            y=int(y)
            if a[x][y]==0:
                b[x][y]=8
                cls()
                matrix_print(b)
                cprint("Miss!","yellow")
            else:
                c[x][y]=a[x][y]
                b[x][y]=9
                cls()
                matrix_print(b)
                cprint("Hit!","red")

# Custom colors for text (using ASCII color codes)
class colors:
    reset='\033[0m'
    bold='\033[01m'
    red='\033[31m'
    lightred='\033[91m'
    cyan='\033[36m'
    green='\033[32m'
    lightgreen='\033[92m'
    darkgrey='\033[90m'


# Menu text
def menu():
    print(colors.red+r"""
                ███████████             █████     █████    ████                   █████       ███
                ░░███░░░░░███           ░░███     ░░███    ░░███                  ░░███       ░░░
                 ░███    ░███  ██████   ███████   ███████   ░███   ██████   █████  ░███████   ████  ████████
                 ░██████████  ░░░░░███ ░░░███░   ░░░███░    ░███  ███░░███ ███░░   ░███░░███ ░░███ ░░███░░███
                 ░███░░░░░███  ███████   ░███      ░███     ░███ ░███████ ░░█████  ░███ ░███  ░███  ░███ ░███
                 ░███    ░███ ███░░███   ░███ ███  ░███ ███ ░███ ░███░░░   ░░░░███ ░███ ░███  ░███  ░███ ░███
                 ███████████ ░░████████  ░░█████   ░░█████  █████░░██████  ██████  ████ █████ █████ ░███████
                ░░░░░░░░░░░   ░░░░░░░░    ░░░░░     ░░░░░  ░░░░░  ░░░░░░  ░░░░░░  ░░░░ ░░░░░ ░░░░░  ░███░░░
                                                                                                    ░███
                                                                                                    █████
                                                                                                   ░░░░░     """+colors.lightred)

    print("""                                                        1.Rules""")
    print("""                                                       2.New Game""")
    print(colors.red+"""                                          ~ Make sure to play in fullscreen! ~"""+colors.lightred)

    # Option selection
    option=input("Select action: ")
    print(colors.reset)
    if option=='1':
        cls()
        rules()
    elif option=='2':
        game()

# Rules menu text
def rules():
    print(colors.cyan+r"""
                                  ███████████              ████
                                  ░░███░░░░░███            ░░███
                                   ░███    ░███  █████ ████ ░███   ██████   █████
                                   ░██████████  ░░███ ░███  ░███  ███░░███ ███░░
                                   ░███░░░░░███  ░███ ░███  ░███ ░███████ ░░█████
                                   ░███    ░███  ░███ ░███  ░███ ░███░░░   ░░░░███
                                   █████   █████ ░░████████ █████░░██████  ██████
                                  ░░░░░   ░░░░░   ░░░░░░░░ ░░░░░  ░░░░░░  ░░░░░░


                                                """)
    print("""
                                The rules are simple. The board is a 30 by 30 square.
                        There are four diffrent lenghts of ships: 5, 4 ,3 and 2 block ships.
             There are three 5 block ships, five 4 block ships, six 3 block ships and eight 2 block ships.
           There also are a few planes. If you destroy its tip or both wings, you destroy the whole aircraft.
                          You win when all of the ships and airplanes have been destroyed."""+colors.reset)
    print(colors.green+"\n                                                    Good Luck!"+colors.reset)
    print(colors.darkgrey+"\n\n                                            ~ Press enter to continue ~")
    input()
    cls()
    menu()

# Print menu
menu()

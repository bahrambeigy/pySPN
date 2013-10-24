#!/usr/bin/python2

from math import pow

try:
    import pyglet.graphics, pyglet.gl
except:
    print "Error! Can't Import Pyglet library - More Information : http://pyglet.org"

"""
***********************************************************************
********************* SIMPLE SPN Run Program **************************
************************ By : BahramBeigy *****************************
************* [project] https://github.com/bahramwhh/pySPN ************
************************** (CLI Version) ******************************

This program is a simple implementation of SPN (Substitution Permutation
Network) algorithm. It can perform with any numbers of S-Boxes and bits 
per them. for example you can set 10 numbers of s-boxes with capacity of
3 bits per s-box which will let you to enter a number as big as 1073741824.
This implementation uses a simple shift of key that is provided by user. 
All numbers should be given in decimal. (It can be changed to binary or 
other format if needed).

To run this program you should enter number of S-Boxes and capacity of 
them (how many bits) and S-Boxes and P-Boxes values to create tables 
from them.

**********************************************************************
"""

# Begin Functions
def binary(n, digits):
    return "{0:0>{1}}".format(bin(n)[2:], digits)

def decimal(n):
    decnum = 0
    for i in n:
        decnum = decnum * 2 + int(i)
    return decnum    

def oplus(op1, op2):
    if len(op1) != len(op2):
        return "error!"
    result = ""

    for i in range(len(op1)):
        if(int(op1[i]) ^ int(op2[i])):
            result += '1'
        else: 
            result +='0'
    return result

def shiftkey(key, step):
    result = ""
    if step >= len(key):
            step = step % len(key)
    index = step
    for i in range(len(key)):
        if index >= len(key):
            index = 0
        result += key[index]
        index += 1
    return result

def split_str(s, count):
    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

#############################################
############## Drawing Functions ############
#############################################
def set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
    if color is not None: pyglet.gl.glColor4f(*color)
    else: pyglet.gl.glColor4f(r,g,b,a)

def clear(win, r=1.0, g=1.0, b=1.0, a=1.0, color=None):
    """Clears the screen. Always called three times instead of the usual one or two."""
    if color is not None: pyglet.gl.glClearColor(*color)
    else: pyglet.gl.glClearColor(r,g,b,a);
    win.clear()

def line(x1, y1, x2, y2):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))

def rect(x1, y1, x2, y2, colors=None):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)) )

def rect_outline(x1, y1, x2, y2):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

# End Functions



# Start Main Program
nr = int(raw_input("Number of rounds: ")) # get number of rounds
bits_per_block = int(raw_input("Number of bits per block: ")) # get capacity of s-boxes
sboxes = int(raw_input("Number of S-Boxes per round: ")) # get number of s-boxes

sbox_table_length = int(pow(2, bits_per_block)) # bits per each s-box
key_length = int(pow(2, sboxes*bits_per_block)) # key length !

binary_digits = bits_per_block # indicates how long binary numbers should be

# get input from user (should be sboxes*bits_per_block long)

print "***** Enter your plain text ( 0 <= plaintext <=",key_length-1,") *****"
print "Enter your input (Decimal) : ",
current_value = int(raw_input())
while current_value >= key_length: # check it's not bigger than maximum
    print "Error ! Your input can't be bigger than ", key_length-1
    print "Again, Enter your input (Decimal) : "
    current_value = int(raw_input())
while current_value < 0: # check it's not negative ?!
    print "Error! Your input can't be negative !"
    print "Again, Enter your input (Decimal) : "
    current_value = int(raw_input())

plaintext = current_value
    
# get initial key from user
print "*********** Enter Master key (0 <= masterkey <=", key_length-1,") (Decimal)"
master_key = int(raw_input())
while master_key >= key_length or master_key < 0:
    print "Error! Master key length is not equal to plain text length ! try again : "
    master_key = int(raw_input())
    

# create and get Substitution-Box table 
sbox_table = [None]*sbox_table_length # create empty s-box table
print " ********* S-Box Substitution table : 0 <= sbox[i] <=", sbox_table_length-1, ") *********"
for i in range(sbox_table_length):
    print "Enter S-Box[",i,"] (Decimal): "
    current_value = int(raw_input())
    
    # check if the entered value has been set before ?!
    is_set_before = True
    while is_set_before:
        for j in range(sbox_table_length):
            if sbox_table[j] == current_value:
                print "Error! this value:", current_value, "has been set for sbox[",j,"] before ! enter another value!"
                print "Again, Enter S-Box[",i,"] (Decimal): ",
                current_value = int(raw_input())
                is_set_before = True
                break
            else:
                is_set_before = False
    
    while current_value >= sbox_table_length : # check it's not bigger than maximum
        print "Error ! S-Box values can't be bigger than ", sbox_table_length, " !"
        print "AgainEnter S-Box[",i,"] (Decimal): ",
        current_value = int(raw_input())
    while current_value < 0:
        print "Error ! S-Box values can't be negative !"
        print "AgainEnter S-Box[",i,"] (Decimal): ",
        current_value = int(raw_input())
                
    sbox_table[i] = current_value

# create and get Permutation-Box table
pbox_length = sboxes * bits_per_block
pbox_table = [None]*pbox_length # create empty p-box table
print "********** P-Box Permutation table : 1 <= pbox[i] <=", pbox_length, ") **********"
for i in range(pbox_length):
    if pbox_table[i] == None: # check if a value has been set before or not ?!
        print "Enter P-Box[",i+1,"] (Decimal): "
        current_value = int(raw_input())-1

        while current_value >= pbox_length:
            print "Error ! you can't set bigger values than ", pbox_length, "!"
            print "Again, Enter P-Box[",i,"] (Decimal): ",
            current_value = int(raw_input())-1
        while current_value < 0:
            print "Error ! P-Box values can't be negative !"
            print "Again, Enter P-Box[",i,"] (Decimal): ",
            current_value = int(raw_input())-1
        while pbox_table[current_value]:
            print "Error ! pbox[",current_value,"] is set to (=)",pbox_table[current_value],"please enter remaining entries"
            print "Again, Enter P-Box[",i,"] (Decimal): ",
            current_value = int(raw_input())-1    
        pbox_table[i] = current_value
        pbox_table[current_value] = i # set the reverse value in the table (automatic insertion)
    else:
        print "P-Box[",i+1,"] is set based what you have entered before :",
        print pbox_table[i]+1

print "***************** Program calculation has been started *********************"

# key generation part (we need Nr+1 keys)
subkeys = []
# convert master key to binary
bin_master_key = binary(master_key, pbox_length)
for i in range(nr+1):
    subkeys.append(shiftkey(bin_master_key, i+1)) # a simple shift of subkeys
print "Subkeys Are : " , subkeys

# loop part ( main algorithm )
temp_plain = binary(plaintext, pbox_length) # convert plaintext to binary
round_outputs = []
for i in range(nr):
    current_text = ""
    pkoplus = oplus(temp_plain, subkeys[i]) # XOR plaintext with subkey of current round
    
    current_blocks = split_str(pkoplus, bits_per_block) # split current text to capacity of each s-boxes
    for j in range(len(current_blocks)):
        current_decimal = decimal(current_blocks[j])
        current_decimal = sbox_table[current_decimal] # substitution phase ;)
        current_text += binary(current_decimal, binary_digits)
    
    permuted = [None] * (pbox_length) # permutation indexes array
    for j in range(pbox_length):
        permuted[j] = current_text[pbox_table[j]] # permutation phase
        
    temp_plain = permuted
    round_outputs.append(temp_plain)
    print "Output of round number", i+1, "is : ", temp_plain

# oplus last result with last subkey
last_result = oplus(temp_plain, subkeys[nr])
print "****************************************************"
print " THE RESULT OF SPN ENCRYPTION IS : (Binary)",last_result, "   (Decimal)", decimal(last_result)


##########################################################
################### Create Diagram #######################
##########################################################

window = pyglet.window.Window(resizable=True)
clear(window, 0.2, 0.2, 0.3, 0.5)
window.set_size(700, 650)
@window.event
def on_draw():
    window.clear()
    window.set_caption("SPN Implementation (CLI Version)")
    base_top = 40 # space gap from top
    number_of_bits = bits_per_block * sboxes # number of all bits
    space_between_lines = (window.width) / (number_of_bits+1) # space between each line (bit)

    plain_text_binary = binary(plaintext, pbox_length)

    bits_x_positions = [] # x position of each line (bit)

    spacing = (window.width - space_between_lines*number_of_bits)/2
    x = spacing
    if x < space_between_lines:
        x = space_between_lines
    for i in range(number_of_bits):    
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)
        current_plain_text_bit = str(plain_text_binary[i])
        label = pyglet.text.Label(current_plain_text_bit, font_name='Times New Roman', font_size=12, x=x, y=y1+10, anchor_x='center', anchor_y='center')
        label.draw()
        bits_x_positions.append(x)
        x = x + space_between_lines
    
    base_top += 20    
    rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
    label = pyglet.text.Label('Subkey K1 Mixing ('+subkeys[0]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
    label.draw()

    base_top += 30
    for i in range(number_of_bits):
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)

    # S-Boxes
    base_top += 20
    x1 = bits_x_positions[0]
    x2 = 0
    set_color(0.7, 0.5, 0.3, 0.8)
    for i in range(sboxes):
        y1 = (window.height - base_top)
        x2 += (bits_per_block * space_between_lines)
        y2 = (window.height - (base_top + 40) )

        rect(x1, y1, x2, y2, 1)
        label = pyglet.text.Label('S-Box'+str(i+1), font_name='Times New Roman', font_size=17, x=x1 + (space_between_lines*(bits_per_block-1)/2), y=window.height - (base_top + 20) , anchor_x='center', anchor_y='center')
        label.draw()
        x1 = x2 + (space_between_lines)

    set_color(1, 1, 0, 0.5)
    base_top += 40
    for i in range(number_of_bits):    
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)

    # Permutation Lines
    base_top += 20
    for i in range(number_of_bits):
        current_permutation = int(pbox_table[i])
        line(bits_x_positions[i], window.height - base_top, bits_x_positions[current_permutation], window.height - (base_top + 90) )

    
    ################ second round ##############    
    base_top += 90
    for i in range(number_of_bits):    
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)
        current_text_bit = str(round_outputs[0][i])
        label = pyglet.text.Label(current_text_bit, font_name='Times New Roman', font_size=12, x=x+3, y=y1-10, anchor_x='center', anchor_y='center')
        label.draw()

    set_color(0, 1, 1, 0.5)
    base_top += 20    
    rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
    label = pyglet.text.Label('Subkey K2 Mixing ('+subkeys[1]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
    label.draw()
    
    base_top += 30
    for i in range(number_of_bits):
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)

    # S-Boxes
    base_top += 20
    x1 = bits_x_positions[0]
    x2 = 0
    set_color(0.7, 0.5, 0.3, 0.8)
    for i in range(sboxes):
        y1 = (window.height - base_top)
        x2 += (bits_per_block * space_between_lines)
        y2 = (window.height - (base_top + 40) )

        rect(x1, y1, x2, y2, 1)
        label = pyglet.text.Label('S-Box'+str(i+1), font_name='Times New Roman', font_size=17, x=x1 + (space_between_lines*(bits_per_block-1)/2), y=window.height - (base_top + 20) , anchor_x='center', anchor_y='center')
        label.draw()
        x1 = x2 + (space_between_lines)

    set_color(1, 1, 0, 0.5)
    base_top += 40
    for i in range(number_of_bits):    
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)

    # Permutation Lines
    base_top += 20
    for i in range(number_of_bits):
        current_permutation = int(pbox_table[i])
        line(bits_x_positions[i], window.height - base_top, bits_x_positions[current_permutation], window.height - (base_top + 90) )
    
    ############## end of second round ################
    
    # Third round
    base_top += 90
    for i in range(number_of_bits):    
        x = bits_x_positions[i]
        y1 = (window.height - base_top)
        y2 = (window.height - (base_top + 20) )
        line(x, y1, x, y2)
        current_text_bit = str(round_outputs[1][i])
        label = pyglet.text.Label(current_text_bit, font_name='Times New Roman', font_size=12, x=x+3, y=y1-10, anchor_x='center', anchor_y='center')
        label.draw()

    set_color(0, 1, 1, 0.5)
    base_top += 20    
    rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
    label = pyglet.text.Label('Subkey K3 Mixing ('+subkeys[2]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
    label.draw()
    
    
    # Last result will be shown under page
    label = pyglet.text.Label('Last result after ' + str(nr) + ' rounds', font_name='Times New Roman', font_size=20, x=window.width//2, y=55, anchor_x='center', anchor_y='center')
    label.draw()
    
    for i in range(number_of_bits):
        current_cipher_text_bit = str(last_result[i])
        label = pyglet.text.Label(current_cipher_text_bit, font_name='Times New Roman', font_size=14, x=bits_x_positions[i], y=30, anchor_x='center', anchor_y='center')
        label.draw()
        
pyglet.app.run()

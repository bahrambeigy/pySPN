#!/usr/bin/python2

from math import pow
import sys
try:
    import pygtk
    pygtk.require('2.0')
except:
    print "Error! Can't Import PyGTK library - More Information: http://pygtk.org"
    sys.exit()
try:
    import gtk
except:
    print "Error! Can't Import GTK library - More Information: http://gtk.org"
    sys.exit()
try:
    import pyglet.graphics, pyglet.gl
except:
    print "Error! Can't Import Pyglet library - More Information : http://pyglet.org"


"""
***********************************************************************
********************* SIMPLE SPN Run Program **************************
************************ By : BahramBeigy *****************************
************* [project] https://github.com/bahramwhh/pySPN ************
************************** (GTK Version) ****************************** 

This program is a GTK front-end of SPN CLI implementation .... 

**********************************************************************
"""


# SPN Complete Implementation Class
class SPN_Implementation:

    # Begin Generic Functions
    def binary(self, n, digits):
        return "{0:0>{1}}".format(bin(n)[2:], digits)
    
    def decimal(self, n):
        decnum = 0
        for i in n:
            decnum = decnum * 2 + int(i)
        return decnum    
    
    def oplus(self, op1, op2):
        if len(op1) != len(op2):
            return "error!"
        result = ""
    
        for i in range(len(op1)):
            if(int(op1[i]) ^ int(op2[i])):
                result += '1'
            else: 
                result +='0'
        return result
    
    def shiftkey(self, key, step):
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
    
    def split_str(self, s, count):
        return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
    # End Generic Functions
    
    #############################################
    ############## Drawing Functions ############
    #############################################
    def set_color(self, r=0.0, g=0.0, b=0.0, a=1.0, color=None):
        if color is not None: pyglet.gl.glColor4f(*color)
        else: pyglet.gl.glColor4f(r,g,b,a)
    
    def clear(self, win, r=1.0, g=1.0, b=1.0, a=1.0, color=None):
        """Clears the screen. Always called three times instead of the usual one or two."""
        if color is not None: pyglet.gl.glClearColor(*color)
        else: pyglet.gl.glClearColor(r,g,b,a);
        win.clear()
    
    def line(self, x1, y1, x2, y2):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
    
    def rect(self, x1, y1, x2, y2, colors=None):
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)) )
    
    def rect_outline(self, x1, y1, x2, y2):
        pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
    
    # End Drawing Functions
    
    
    # make focus on widgets
    def set_focus(self, widget):
        widget.grab_focus()
        widget.select_region(0, len(widget.get_text()))
    
    def hide_about(self, widget, data):
        self.about_window.hide_all()
        
    def table_changed(self, widget, event, data=None):
        adj = self.sbox_window.get_vadjustment()
        adj.set_value( adj.upper - adj.page_size )
    
    def about_menu_show(self, widget):
        
        self.about_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.about_window.set_title("About ...")
        self.about_window.connect("delete_event", self.hide_about)
        self.about_window.set_transient_for(self.window)
        self.about_window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        
        self.about_window.set_border_width(20)
        self.about_window.set_size_request(400, 150)
        
        vbox = gtk.VBox(True, 2)
        self.about_window.add(vbox)
        
        label = gtk.Label("This SPN Implementation is Programmed by:")
        label2 = gtk.Label()
        label2.set_markup("<b>Bahram BahramBeigy</b>")
        label3 = gtk.Label("(bahramwhh@gmail.com)")
        space = gtk.Label()
        label4 = gtk.Label("just for network security project :)")
        
        vbox.pack_start(label, 1, 1, 0)
        vbox.pack_start(label2, 1, 1, 0)
        vbox.pack_start(label3, 1, 1, 0)
        vbox.pack_start(space, 1, 1, 0)
        vbox.pack_start(label4, 1, 1, 0)
        
        self.about_window.show_all()
    
    # control run spn and show diagram buttons
    def callbackButtons(self, widget):
        if widget == self.runButton: # Run SPN !
            if not self.ready_to_run_spn:
                self.messagesLabel.set_text("Error! Values are not yet completed ! please fill all fields")
                self.event_box_messages.show_all()
            else:
                self.event_box_messages.hide_all()
                
                pbox_length = self.sboxes * self.bits_per_block
                
                # key generation part (we need Nr+1 keys)
                self.subkeys = []
                # convert master key to binary
                bin_master_key = self.binary(self.masterkey_decimal, pbox_length)
                for i in range(self.nr+1):
                    self.subkeys.append(self.shiftkey(bin_master_key, i+1)) # a simple shift of subkeys
                
                output_window = gtk.ScrolledWindow()
                output_window.set_border_width(5)
                output_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
                
                output_table = gtk.Table(self.nr+4+self.nr, 1, True) # create sbox table layout
            
                output_window.add_with_viewport(output_table)
                
                self.rightcontainerVBox.add(output_window)
                
                temp_label = gtk.Label('')
                temp_label.set_markup("<b>Subkeys Are :</b>")
                output_table.attach(temp_label, 0, 1, 0, 1)
                for i in range(len(self.subkeys)):
                    output_table.attach(gtk.Label(self.subkeys[i]), 0, 1, i+1, i+2)
                                    
                
                # loop part ( main algorithm )
                current_index = len(self.subkeys)+2
                temp_label = gtk.Label('')
                temp_label.set_markup("<b>Output of "+str(self.nr)+" Rounds:</b>")
                output_table.attach(temp_label, 0, 1, current_index, current_index+1)
                temp_plain = self.binary(self.plaintext_decimal, pbox_length) # convert plaintext to binary
                self.round_outputs = []
                current_index = current_index + 1
                for i in range(self.nr):
                    current_text = ""
                    pkoplus = self.oplus(temp_plain, self.subkeys[i]) # XOR plaintext with subkey of current round
                    
                    current_blocks = self.split_str(pkoplus, self.bits_per_block) # split current text to capacity of each s-boxes
                    for j in range(len(current_blocks)):
                        current_decimal = self.decimal(current_blocks[j])
                        current_decimal = self.sbox_table_array[current_decimal] # substitution phase ;)
                        current_text += self.binary(current_decimal, self.bits_per_block)
                    
                    permuted = [None] * (pbox_length) # permutation indexes array
                    for j in range(pbox_length):
                        permuted[j] = current_text[self.pbox_table_array[j]] # permutation phase
                        
                    temp_plain = permuted
                    self.round_outputs.append(temp_plain)
                    
                    temp_output = ""
                    for k in range(len(temp_plain)):
                        temp_output += str(temp_plain[k])
                    
                    output_table.attach(gtk.Label("["+str(i+1)+"]: "+temp_output), 0, 1, current_index, current_index+1)
                    current_index = current_index + 1
                
                # oplus last result with last subkey
                self.last_result = self.oplus(temp_plain, self.subkeys[self.nr])
                
                self.event_box_messages.modify_bg(gtk.STATE_NORMAL, self.event_box_messages.get_colormap().alloc_color("green"))
                self.messagesLabel.set_text(" Result : (Binary) "+str(self.last_result)+" (Decimal) "+str(self.decimal(self.last_result)))
                self.event_box_messages.show_all()
                
                self.rightcontainerVBox.set_size_request(200, 400)
                self.showDiagram.set_sensitive(True)
                self.runButton.set_sensitive(False)
                self.rightcontainerVBox.show_all()
        
        if widget == self.showDiagram: # Create Diagram using pyglet
            window = pyglet.window.Window(resizable=True)
            self.clear(window, 0.2, 0.2, 0.3, 0.5)
            window.set_size(700, 650)
            @window.event
            def on_draw():
                window.clear()
                window.set_caption("SPN Implementation (GTK Version)")
                base_top = 40 # space gap from top
                number_of_bits = self.bits_per_block * self.sboxes # number of all bits
                space_between_lines = (window.width) / (number_of_bits+1) # space between each line (bit)
            
                pbox_length = self.sboxes * self.bits_per_block
                plain_text_binary = self.binary(self.plaintext_decimal, pbox_length)
            
                bits_x_positions = [] # x position of each line (bit)
            
                spacing = (window.width - space_between_lines*number_of_bits)/2
                x = spacing
                if x < space_between_lines:
                    x = space_between_lines
                for i in range(number_of_bits):    
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
                    current_plain_text_bit = str(plain_text_binary[i])
                    label = pyglet.text.Label(current_plain_text_bit, font_name='Times New Roman', font_size=12, x=x, y=y1+10, anchor_x='center', anchor_y='center')
                    label.draw()
                    bits_x_positions.append(x)
                    x = x + space_between_lines
                
                base_top += 20    
                self.rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
                label = pyglet.text.Label('Subkey K1 Mixing ('+self.subkeys[0]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
                label.draw()
            
                base_top += 30
                for i in range(number_of_bits):
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
            
                # S-Boxes
                base_top += 20
                x1 = bits_x_positions[0]
                x2 = 0
                self.set_color(0.7, 0.5, 0.3, 0.8)
                for i in range(self.sboxes):
                    y1 = (window.height - base_top)
                    x2 += (self.bits_per_block * space_between_lines)
                    y2 = (window.height - (base_top + 40) )
            
                    self.rect(x1, y1, x2, y2, 1)
                    label = pyglet.text.Label('S-Box'+str(i+1), font_name='Times New Roman', font_size=17, x=x1 + (space_between_lines*(self.bits_per_block-1)/2), y=window.height - (base_top + 20) , anchor_x='center', anchor_y='center')
                    label.draw()
                    x1 = x2 + (space_between_lines)
            
                self.set_color(1, 1, 0, 0.5)
                base_top += 40
                for i in range(number_of_bits):    
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
            
                # Permutation Lines
                base_top += 20
                for i in range(number_of_bits):
                    current_permutation = int(self.pbox_table_array[i])
                    self.line(bits_x_positions[i], window.height - base_top, bits_x_positions[current_permutation], window.height - (base_top + 90) )
            
                
                ################ second round ##############    
                base_top += 90
                for i in range(number_of_bits):    
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
                    current_text_bit = str(self.round_outputs[0][i])
                    label = pyglet.text.Label(current_text_bit, font_name='Times New Roman', font_size=12, x=x+3, y=y1-10, anchor_x='center', anchor_y='center')
                    label.draw()
            
                self.set_color(0, 1, 1, 0.5)
                base_top += 20    
                self.rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
                label = pyglet.text.Label('Subkey K2 Mixing ('+self.subkeys[1]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
                label.draw()
                
                base_top += 30
                for i in range(number_of_bits):
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
            
                # S-Boxes
                base_top += 20
                x1 = bits_x_positions[0]
                x2 = 0
                self.set_color(0.7, 0.5, 0.3, 0.8)
                for i in range(self.sboxes):
                    y1 = (window.height - base_top)
                    x2 += (self.bits_per_block * space_between_lines)
                    y2 = (window.height - (base_top + 40) )
            
                    self.rect(x1, y1, x2, y2, 1)
                    label = pyglet.text.Label('S-Box'+str(i+1), font_name='Times New Roman', font_size=17, x=x1 + (space_between_lines*(self.bits_per_block-1)/2), y=window.height - (base_top + 20) , anchor_x='center', anchor_y='center')
                    label.draw()
                    x1 = x2 + (space_between_lines)
            
                self.set_color(1, 1, 0, 0.5)
                base_top += 40
                for i in range(number_of_bits):    
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
            
                # Permutation Lines
                base_top += 20
                for i in range(number_of_bits):
                    current_permutation = int(self.pbox_table_array[i])
                    self.line(bits_x_positions[i], window.height - base_top, bits_x_positions[current_permutation], window.height - (base_top + 90) )
                
                ############## end of second round ################
                
                # Third round
                base_top += 90
                for i in range(number_of_bits):    
                    x = bits_x_positions[i]
                    y1 = (window.height - base_top)
                    y2 = (window.height - (base_top + 20) )
                    self.line(x, y1, x, y2)
                    current_text_bit = str(self.round_outputs[1][i])
                    label = pyglet.text.Label(current_text_bit, font_name='Times New Roman', font_size=12, x=x+3, y=y1-10, anchor_x='center', anchor_y='center')
                    label.draw()
            
                self.set_color(0, 1, 1, 0.5)
                base_top += 20    
                self.rect_outline(space_between_lines, window.height - base_top , (window.width - space_between_lines), window.height - (base_top + 30))
                label = pyglet.text.Label('Subkey K3 Mixing ('+self.subkeys[2]+')', font_name='Times New Roman', font_size=18, x=window.width//2, y=window.height - (base_top + 12) , anchor_x='center', anchor_y='center')
                label.draw()
                
                
                # Last result will be shown under page
                label = pyglet.text.Label('Last result after ' + str(self.nr) + ' rounds', font_name='Times New Roman', font_size=20, x=window.width//2, y=55, anchor_x='center', anchor_y='center')
                label.draw()
                
                for i in range(number_of_bits):
                    current_cipher_text_bit = str(self.last_result[i])
                    label = pyglet.text.Label(current_cipher_text_bit, font_name='Times New Roman', font_size=14, x=bits_x_positions[i], y=30, anchor_x='center', anchor_y='center')
                    label.draw()
                    
            pyglet.app.run()
    
    # control s-box table entries
    def callbackSBoxEntries(self, widget, data, index):
        try:
            if widget.get_text():
                temp = int(str(widget.get_text()))
                
                there_is_error = False
                for i in range(index):
                    if temp == int(self.sbox_entries[i].get_text()):
                        self.messagesLabel.set_text("Error ! "+str(temp)+" has been set to SBox["+str(i)+"] before !")
                        self.event_box_messages.show_all()
                        self.set_focus(self.sbox_entries[index])
                        there_is_error = True
                if temp >= self.sbox_table_length:
                    self.messagesLabel.set_text("Error ! Very Big value in SBox["+str(index)+"] !")
                    self.event_box_messages.show_all()
                    self.set_focus(self.sbox_entries[index])
                    there_is_error = True
                elif temp < 0:
                    self.messagesLabel.set_text("Error ! Negative value in SBox["+str(index)+"] !")
                    self.event_box_messages.show_all()
                    self.set_focus(self.sbox_entries[index])
                    there_is_error = True
                
                if not there_is_error:
                    self.sbox_table_array.append(temp)
                
                    widget.set_sensitive(False) # disable current entry
                    self.event_box_messages.hide_all() # hide errors
                
                    self.sbox_entries[index+1].set_sensitive(True) # enable next entry
                    self.sbox_entries[index+1].grab_focus() 
                    
                    # make scrollbar down ! :)
                    adj = self.sbox_window.get_vadjustment()
                    entry_alloc = widget.get_allocation()
                    if adj.get_page_size() != adj.get_upper(): # check if it has scrollbar ?!
                        if (adj.get_value()+entry_alloc.height) < (adj.get_upper() - adj.get_page_size()): # check scrollbar is reached end ?! 
                            adj.set_value(entry_alloc.y)
                        else:
                            adj.set_value(adj.get_upper() - adj.get_page_size())
                    
            
        except ValueError:
            self.messagesLabel.set_text("Invalid value for SBox["+str(index)+"]")
            self.event_box_messages.show_all()
            self.set_focus(widget)
        except IndexError:
            self.pbox_entries[0].set_sensitive(True)
            self.pbox_entries[0].grab_focus()
            self.event_box_messages.hide_all() # hide errors
            
    # control p-box table entries
    def callbackPBoxEntries(self, widget, data, index):
        try:            
            if widget.get_text():
                temp = int(str(widget.get_text()))
                temp = temp - 1
                
                if self.pbox_table_array[index] == None:
                    pbox_length = self.sboxes * self.bits_per_block
                    
                    there_is_error = False
                    try:
                        if self.pbox_table_array[temp] != None:
                            self.messagesLabel.set_text("Error ! "+str(temp)+" has been set for PBox["+str(index+1)+"] !")
                            self.event_box_messages.show_all()
                            self.set_focus(self.pbox_entries[index])
                            there_is_error = True
                    except:
                        pass
                    
                    if temp >= pbox_length:
                        self.messagesLabel.set_text("Error ! Very Big value in PBox["+str(index+1)+"] !")
                        self.event_box_messages.show_all()
                        self.set_focus(self.pbox_entries[index])
                        there_is_error = True
                    elif temp < 0:
                        self.messagesLabel.set_text("Error ! Negative value in PBox["+str(index+1)+"] !")
                        self.event_box_messages.show_all()
                        self.set_focus(self.pbox_entries[index])
                        there_is_error = True
                    
                    if not there_is_error:
                        self.pbox_table_array[index] = temp
                        self.pbox_table_array[temp] = index
                        self.pbox_entries[temp].set_text(str(index+1))
                    
                        widget.set_sensitive(False) # disable current entry
                        self.event_box_messages.hide_all() # hide errors
                    
                        index = index + 1
                        while self.pbox_table_array[index] != None:
                            self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD)
                            index = index + 1
                            
                        self.pbox_entries[index].set_sensitive(True) # enable next entry
                        self.pbox_entries[index].grab_focus()
                        
                        # make scrollbar down ! :)
                        adj = self.pbox_window.get_vadjustment()
                        entry_alloc = self.pbox_entries[index].get_allocation()
                        if adj.get_page_size() != adj.get_upper(): # check if it has scrollbar ?!
                            if (adj.get_value()+entry_alloc.height) < (adj.get_upper() - adj.get_page_size()): # check scrollbar is reached end ?! 
                                adj.set_value(entry_alloc.y)
                            else:
                                adj.set_value(adj.get_upper() - adj.get_page_size())
                else:
                    pass
            
        except ValueError:
            self.messagesLabel.set_text("Invalid value for PBox["+str(index)+"]")
            self.event_box_messages.show_all()
            self.set_focus(widget)
        except IndexError:
            self.runButton.grab_focus()
            self.ready_to_run_spn = True
            

    # control function for basic inputs and create s-box and p-box tables    
    def callbackFocusLoss(self, widget, data):
        if widget == self.input_number_of_rounds: # number of rounds
            try:
                if self.input_number_of_rounds.get_text():
                    self.nr = int(self.input_number_of_rounds.get_text())
                    self.event_box_messages.hide_all()
                    self.input_number_of_bits_per_block.set_sensitive(True)
                    self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD)
                    self.set_focus(self.input_number_of_bits_per_block)
                    self.input_number_of_rounds.set_sensitive(False)
            except ValueError:
                self.messagesLabel.set_text("Invalid Number for Number of Rounds")
                self.event_box_messages.show_all()
                self.nr = None
                self.set_focus(self.input_number_of_rounds)
            
        elif widget == self.input_number_of_bits_per_block: # number of bits per block
            try:
                if self.input_number_of_bits_per_block.get_text():
                    self.bits_per_block = int(self.input_number_of_bits_per_block.get_text())
                    self.sbox_table_length = int(pow(2, self.bits_per_block)) # bits per each s-box
                    self.event_box_messages.hide_all()
                    self.input_number_of_sboxes.set_sensitive(True)
                    self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD)
                    self.set_focus(self.input_number_of_sboxes)
                    self.input_number_of_bits_per_block.set_sensitive(False)
            except ValueError:
                self.messagesLabel.set_text("Invalid Number for Bits Per Block")
                self.event_box_messages.show_all()
                self.bits_per_block = None
                self.set_focus(self.input_number_of_bits_per_block)
                
        elif widget == self.input_number_of_sboxes: # number of s-boxes
            try:
                if self.input_number_of_sboxes.get_text():
                    self.sboxes = int(self.input_number_of_sboxes.get_text())
                    
                    if self.sbox_table_length != None:
                        self.key_length = int(pow(2, self.sboxes*self.bits_per_block)) # key length !
                        if self.plaintext_decimal == None:
                            self.input_plaintext.set_text('up to' + str(self.key_length-1)) # set plaintext maximum number
                        if self.masterkey_decimal == None:
                            self.input_masterkey.set_text('up to' + str(self.key_length-1)) # set masterkey maximum number
                    self.event_box_messages.hide_all()
                    self.input_plaintext.set_sensitive(True)
                    self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD)
                    self.set_focus(self.input_plaintext)
                    self.input_number_of_sboxes.set_sensitive(False)
            except ValueError:
                self.messagesLabel.set_text("Invalid Number for Number of S-Boxes")
                self.event_box_messages.show_all()
                self.sboxes = None
                self.set_focus(self.input_number_of_sboxes)
            
        elif widget == self.input_plaintext:
            try:
                if self.input_plaintext.get_text():
                    self.plaintext_decimal = int(self.input_plaintext.get_text())
                    
                    if self.plaintext_decimal >= self.key_length:
                        self.messagesLabel.set_text("Very big plaintext value!")
                        self.event_box_messages.show_all()
                        self.set_focus(self.input_plaintext)
                    elif self.plaintext_decimal < 1:
                        self.messagesLabel.set_text("Very small plaintext value!")
                        self.event_box_messages.show_all()
                        self.set_focus(self.input_plaintext)
                    else:
                        self.messagesLabel.set_text("") # remove errors
                        self.event_box_messages.hide_all()
                        self.input_masterkey.set_sensitive(True)
                        self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD) # set focus to next widget
                        self.set_focus(self.input_masterkey)
                        self.input_plaintext.set_sensitive(False)
            
            except ValueError:
                self.messagesLabel.set_text("Invalid number in plaintext !")
                self.event_box_messages.show_all()
                self.plaintext_decimal = None
                self.set_focus(self.input_plaintext)
        
        elif widget == self.input_masterkey:
            try:
                if self.input_masterkey.get_text():
                    self.masterkey_decimal = int(self.input_masterkey.get_text())
                    
                    if self.masterkey_decimal >= self.key_length:
                        self.messagesLabel.set_text("Very big masterkey value!")
                        self.event_box_messages.show_all()
                        self.set_focus(self.input_masterkey)
                    elif self.masterkey_decimal < 1:
                        self.messagesLabel.set_text("Very small master value!")
                        self.event_box_messages.show_all()
                        self.set_focus(self.input_masterkey)
                    else:
                        self.messagesLabel.set_text("")
                        self.event_box_messages.hide_all()
                        self.window.do_move_focus(self.window, gtk.DIR_TAB_FORWARD)
                        self.input_masterkey.set_sensitive(False)
                
            except ValueError:
                self.messagesLabel.set_text("Invalid number in masterkey !")
                self.event_box_messages.show_all()
                self.masterkey_decimal = None
                self.set_focus(self.input_masterkey)
        
        # create s-box and p-box tables when everything is ready ;)
        if self.nr != None and self.bits_per_block != None and self.sboxes != None and self.plaintext_decimal != None and self.masterkey_decimal != None and self.tables_is_shown == False:
            # make s-box table get interface
            self.sbox_window = gtk.ScrolledWindow()
            self.sbox_window.set_border_width(5)
            self.sbox_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
                    
            self.sbox_table = gtk.Table(self.sbox_table_length, 2, True) # create sbox table layout
            
            self.sbox_window.add_with_viewport(self.sbox_table)
            
            for i in range(self.sbox_table_length): # number of rows (sbox-table entries)
                sbox_label = gtk.Label('S['+str(i)+']')
                self.sbox_table.attach(sbox_label, 0, 1, i, i+1)
                
                self.sbox_entries.append(gtk.Entry(len(str(self.sbox_table_length))))
                self.sbox_entries[i].set_width_chars(4) ## limit width
                self.sbox_entries[i].set_sensitive(False)
                self.sbox_entries[i].connect("activate", self.callbackSBoxEntries, None, i)
                self.sbox_entries[i].connect("focus-out-event", self.callbackSBoxEntries, i)
                self.sbox_table.attach(self.sbox_entries[i], 1, 2, i, i+1)
                
            self.arraysleftVBox.pack_start(self.sbox_window, 1, 1, 1)
            
            # make first sbox entry active and grab focus
            self.sbox_entries[0].set_sensitive(True)
            self.sbox_entries[0].grab_focus()
                        
            # make p-box table get interface
            self.pbox_window = gtk.ScrolledWindow()
            self.pbox_window.set_border_width(5)
            self.pbox_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            
            self.pbox_table = gtk.Table(self.sboxes*self.bits_per_block, 2, True)
            
            self.pbox_window.add_with_viewport(self.pbox_table)
            
            for i in range(self.sboxes*self.bits_per_block): # number of rows (sbox-table entries)
                pbox_label = gtk.Label('P['+str(i+1)+']')
                self.pbox_table.attach(pbox_label, 0, 1, i, i+1)
                
                self.pbox_entries.append(gtk.Entry(len(str(self.sboxes*self.bits_per_block))))
                self.pbox_entries[i].set_width_chars(4) ## limit width
                self.pbox_entries[i].set_sensitive(False)
                self.pbox_entries[i].connect("activate", self.callbackPBoxEntries, None, i)
                self.pbox_entries[i].connect("focus-out-event", self.callbackPBoxEntries, i)
                self.pbox_table.attach(self.pbox_entries[i], 1, 2, i, i+1)
                
            self.arraysrightVBox.pack_start(self.pbox_window, 1, 1, 1)
            
            # create empty array for permutation box
            self.pbox_table_array = [None] * (self.sboxes * self.bits_per_block)
            
            self.arraysinputHBox.show_all()
            
            self.tables_is_shown = True
        
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # main part of program starts here
    def __init__(self):
        self.nr = None # number of rounds
        self.bits_per_block = None # number of bits per each s-box
        self.sboxes = None # number of s-boxes
        self.sbox_table_length = None # number of s-box table entries
        self.key_length = None # master and subkeys length
        self.binary_digits = None # number of digits in binary representation
        self.plaintext_decimal = None # plaintext in decimal representation
        self.masterkey_decimal = None # masterkey in decimal representation
        self.tables_is_shown = False # permission to show s-box and p-box tables
        self.ready_to_run_spn = False # permission to run spn calculation
        
        self.sbox_table_array = [] # s-box values holder
        self.pbox_table_array = [] # p-box values holder
        
        self.sbox_entries = [] # s-box input fields
        self.pbox_entries = [] # p-box input fields
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("SPN Implementation")
        self.window.connect("delete_event", self.delete_event)

        self.window.set_border_width(0)

        self.godContainerVBox = gtk.VBox(False, 0) # contains everything !
        self.topContainerHBox = gtk.HBox(False, 2) # contains all widgets
        self.leftcontainerVBox = gtk.VBox(False, 2) # contains left widgets
        self.rightcontainerVBox = gtk.VBox(False, 2) # contains right widgets
        self.basicinputsVBox = gtk.VBox(False, 0) # contains get initial values from user, Nr, Sboxes, etc
        self.arraysinputHBox = gtk.HBox(True, 10) # contains two Horizontal Box left and right
        self.arraysleftVBox = gtk.VBox(True, 2) # Substitution-Box table
        self.arraysrightVBox = gtk.VBox(True, 2) # Permutation-Box table

        
        self.topContainerHBox.set_border_width(5)
        
        # create a small menu ;)
        menu1 = gtk.Menu()
        exit_item = gtk.MenuItem("_Exit")
        exit_item.set_use_underline(True)
        menu1.append(exit_item)
        exit_item.connect("activate", self.delete_event, None)
        file_menu = gtk.MenuItem("_File")
        file_menu.set_use_underline(True)
        file_menu.set_submenu(menu1)
        
        menu2 = gtk.Menu()
        about_item = gtk.MenuItem("_About")
        about_item.set_use_underline(True)
        menu2.append(about_item)
        about_item.connect("activate", self.about_menu_show)
        help_menu = gtk.MenuItem("_Help")
        help_menu.set_use_underline(True)
        help_menu.set_submenu(menu2)
        
        menu_bar = gtk.MenuBar()
        menu_bar.append(file_menu)
        menu_bar.append(help_menu)
        self.godContainerVBox.pack_start(menu_bar, False, False, 0)
        self.window.menu_get_for_attach_widget()
        
        
        # messages section
        self.event_box_messages = gtk.EventBox()
        self.messagesLabel = gtk.Label("")
        self.messagesLabel.set_use_markup(True)
        self.event_box_messages.add(self.messagesLabel)
        self.event_box_messages.modify_bg(gtk.STATE_NORMAL, self.event_box_messages.get_colormap().alloc_color("red"))
        self.leftcontainerVBox.pack_start(self.event_box_messages, 0, 0, 0)
        
        hsep0 = gtk.HSeparator()
        self.leftcontainerVBox.pack_start(hsep0, 0, 0, 0)
        
        self.leftcontainerVBox.add(self.basicinputsVBox)
        self.leftcontainerVBox.add(self.arraysinputHBox)
        self.arraysinputHBox.add(self.arraysleftVBox)
        self.arraysinputHBox.add(self.arraysrightVBox)
        self.topContainerHBox.add(self.leftcontainerVBox)
        self.topContainerHBox.add(self.rightcontainerVBox)
        self.godContainerVBox.add(self.topContainerHBox)
        self.window.add(self.godContainerVBox)
        
        # Get number of round from user
        self.number_of_rounds_HBox = gtk.HBox(True, 2)
        self.label_number_of_rounds = gtk.Label("Number of Rounds :")
        self.input_number_of_rounds = gtk.Entry(0)
        self.input_number_of_rounds.connect("activate", self.callbackFocusLoss, None)
        self.input_number_of_rounds.connect("focus-out-event", self.callbackFocusLoss)
        self.input_number_of_rounds.set_tooltip_text("Type your value and press 'ENTER' or 'TAB'")
        self.number_of_rounds_HBox.pack_start(self.label_number_of_rounds, 1, 1, 0)
        self.number_of_rounds_HBox.pack_start(self.input_number_of_rounds, 1, 1, 0)
        self.basicinputsVBox.pack_start(self.number_of_rounds_HBox, 1, 1, 0)

        
        # Get number bits per block from user
        self.number_of_bits_per_block_HBox = gtk.HBox(True, 2)
        self.label_number_of_bits_per_block = gtk.Label("Number of Bits Per Block :")
        self.input_number_of_bits_per_block = gtk.Entry(0)
        self.input_number_of_bits_per_block.set_sensitive(False)
        self.input_number_of_bits_per_block.connect("activate", self.callbackFocusLoss, None)
        self.input_number_of_bits_per_block.connect("focus-out-event", self.callbackFocusLoss)
        self.number_of_bits_per_block_HBox.pack_start(self.label_number_of_bits_per_block, 1, 1, 0)
        self.number_of_bits_per_block_HBox.pack_start(self.input_number_of_bits_per_block, 1, 1, 0)
        self.basicinputsVBox.pack_start(self.number_of_bits_per_block_HBox, 1, 1, 0)
        
        # Get number of S-Boxes from user
        self.number_of_sboxes_HBox = gtk.HBox(True, 2)
        self.label_number_of_sboxes = gtk.Label("Number of S-Boxes :")
        self.input_number_of_sboxes = gtk.Entry(0)
        self.input_number_of_sboxes.set_sensitive(False)
        self.input_number_of_sboxes.connect("activate", self.callbackFocusLoss, None)
        self.input_number_of_sboxes.connect("focus-out-event", self.callbackFocusLoss)
        self.number_of_sboxes_HBox.pack_start(self.label_number_of_sboxes, 1, 1, 0)
        self.number_of_sboxes_HBox.pack_start(self.input_number_of_sboxes, 1, 1, 0)
        self.basicinputsVBox.pack_start(self.number_of_sboxes_HBox, 1, 1, 0)
        
        # Horizontal Seperator
        self.horizontal_seperator = gtk.HSeparator()
        self.basicinputsVBox.pack_start(self.horizontal_seperator)
        
        # get PlainText from user
        self.plaintext_HBox = gtk.HBox(True, 2)
        self.label_plaintext = gtk.Label("Your Plain Text (decimal) :")
        self.input_plaintext = gtk.Entry(0)
        self.input_plaintext.set_sensitive(False)
        self.input_plaintext.connect("activate", self.callbackFocusLoss, None)
        self.input_plaintext.connect("focus-out-event", self.callbackFocusLoss)
        self.plaintext_HBox.pack_start(self.label_plaintext, 1, 1, 0)
        self.plaintext_HBox.pack_start(self.input_plaintext, 1, 1, 0)
        self.basicinputsVBox.pack_start(self.plaintext_HBox, 1, 1, 0)
        
        # get Master key from user
        self.masterkey_HBox = gtk.HBox(True, 2)
        self.label_masterkey = gtk.Label("Your Master Key (decimal) :")
        self.input_masterkey = gtk.Entry(0)
        self.input_masterkey.set_sensitive(False)
        self.input_masterkey.connect("activate", self.callbackFocusLoss, None)
        self.input_masterkey.connect("focus-out-event", self.callbackFocusLoss)
        self.masterkey_HBox.pack_start(self.label_masterkey, 1, 1, 0)
        self.masterkey_HBox.pack_start(self.input_masterkey, 1, 1, 0)
        self.basicinputsVBox.pack_start(self.masterkey_HBox, 1, 1, 0)
        
        self.horizontal_seperator = gtk.HSeparator()
        self.basicinputsVBox.pack_start(self.horizontal_seperator)
        
        ## place of s-box and pbox-tables
        
        self.arraysinputHBox.set_size_request(200, 400)
        
        hsep = gtk.HSeparator()
        self.rightcontainerVBox.pack_start(hsep, 0, 0, 0)
        
        self.runButton = gtk.Button("Run SPN")
        self.rightcontainerVBox.pack_start(self.runButton, 0, 0, 0)
        self.runButton.connect("clicked", self.callbackButtons)
        
        self.showDiagram = gtk.Button("Show Diagram")
        self.showDiagram.set_sensitive(False)
        self.showDiagram.connect("clicked", self.callbackButtons)
        self.rightcontainerVBox.pack_start(self.showDiagram, 0, 0, 0)
        
        hsep2 = gtk.HSeparator()
        self.rightcontainerVBox.pack_start(hsep2, 0, 0, 0)
        
        # Show all widgets
        self.godContainerVBox.show_all()
        
        # Hide widgets
        self.event_box_messages.hide_all()
        self.arraysinputHBox.hide_all()
        
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    run = SPN_Implementation()
    main()
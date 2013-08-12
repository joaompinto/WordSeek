#!/usr/bin/python

# communicate.py

import wx
import wordengine

	
class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
	
	self.CLICKED_COLOUR = wx.Colour(180,237,233)
	self.LAST_CLICKED_COLOUR = wx.Colour(180,184,237)

        self.text = parent.GetParent().rightPanel.text
	self.played_list = parent.GetParent().rightPanel.played_list
	self.play_buttons = []
	self.selected_letters = []
	self.last_clicked = None
	self.current_word = ""

        sizer = wx.BoxSizer(wx.VERTICAL)
	buttons_sizer = wx.GridSizer(5, 5)  
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(18)
	self.letter_generator = wordengine.LetterGenerator(25, 10, ("K","Y","W"))
	self.word_list = wordengine.WordList("i18n/pt_PT/wordlist.txt.bz2")
	for x in range(0,5):
		for y in range(0,5):
			letter = self.letter_generator.get_letter((x*5)+y)
			button = wx.Button(self, -1, letter, (50,50))
			button.board_pos = wx.Point(x,y)
			button.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
			button.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
			button.is_clicked = False
			self.Bind(wx.EVT_BUTTON, self.OnClick, id=button.GetId())
			button.SetFont(font)
			button.defaultColour = button.GetBackgroundColour()
			buttons_sizer.Add(button, 0, wx.EXPAND)
			self.play_buttons.append(button)

	sizer.Add(buttons_sizer, 0, wx.EXPAND)	
	self.current_word_label = wx.StaticText(self, -1, '')
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(30)
	self.current_word_label.SetFont(font)
	sizer.Add(self.current_word_label, 0, wx.EXPAND)
	button = wx.Button(self, -1, "Verificar", (50,50))
	button.Bind(wx.EVT_BUTTON, self.onCheck, id=button.GetId())
	sizer.Add(button, 0, wx.EXPAND)		
        self.SetSizer(sizer)
        self.Centre()
        self.Show(True)

    def UpdateCurrentWord(self):
	word = ""
	for a_button in self.selected_letters:
		word = word+a_button.GetLabel()
	self.current_word_label.SetLabel(word)

    def ResetSelection(self):
	for a_button in self.selected_letters:
		a_button.is_clicked = False
		a_button.SetBackgroundColour(a_button.defaultColour)
	self.selected_letters = []
	self.last_clicked = None
	self.UpdateCurrentWord()
	self.Refresh()

    def RollBackLetter(self):
	self.selected_letters.pop()
	if self.last_clicked:	
		self.last_clicked.SetBackgroundColour(self.last_clicked.defaultColour)
		self.last_clicked.is_clicked = False
	if len(self.selected_letters)>0:
		self.last_clicked = self.selected_letters[len(self.selected_letters)-1]
		self.last_clicked.SetBackgroundColour(self.LAST_CLICKED_COLOUR)
	else:
		self.last_clicked = None
	self.UpdateCurrentWord()
	self.Refresh()

    def onCheck(self, event):
	word = self.current_word_label.GetLabel()
	
	self.ResetSelection()

    def onMouseOver(self, event):
	event.GetEventObject().SetBackgroundColour('Gray')
	self.Refresh()
	event.Skip()

    def onMouseLeave(self, event):
	button =  event.GetEventObject()
	if button == self.last_clicked:
		button.SetBackgroundColour(self.LAST_CLICKED_COLOUR)
	elif button.is_clicked:
		button.SetBackgroundColour(self.CLICKED_COLOUR)
	else:
		button.SetBackgroundColour(button.defaultColour)
	event.Skip()

    def OnClick(self, event):
	button =  event.GetEventObject()
	""" We reset the selection if an already selected button is clicked
	or the current clicked button is not adjancent to the last clicked """
	if button.is_clicked: # Re-clicking clears the current selection
		if button == self.last_clicked:
			self.RollBackLetter()
			return
		else:
			self.ResetSelection()
	elif self.last_clicked: # Check if letter is adjancent to last click
		posDiff = button.board_pos - self.last_clicked.board_pos
		if abs(posDiff.x)>1 or abs(posDiff.y)>1: # Not adjacent, 
			self.ResetSelection()	
	
	# Change the last clicked color to just clicked
	if self.last_clicked:
		self.last_clicked.is_clicked = True
		self.last_clicked.SetBackgroundColour(self.CLICKED_COLOUR)

	# Now set the last clicked color
	button.is_clicked = True
	button.SetBackgroundColour(self.LAST_CLICKED_COLOUR)

	# Update the current word

	self.last_clicked = button
	self.selected_letters.append(button)
	self.UpdateCurrentWord()
	self.Refresh()




class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
	sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, -1, '0', (40, 60))
	


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 400))

        panel = wx.Panel(self, -1)
        self.rightPanel = RightPanel(panel, -1)

        leftPanel = LeftPanel(panel, -1)

        hbox = wx.BoxSizer()
        hbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.rightPanel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(hbox) 
        self.Centre()
        self.Show(True)

app = wx.App()
MainFrame(None, -1, 'WordSeek')
app.MainLoop()


import string
import random
import bz2

class LetterGenerator:
	def __init__(self, letterCount, vowelsMin, exclude_list=()):
		self.vowels = ('A','E','I','O','U')
		self.letter_list = []
		self.exclude_list = exclude_list
		vowelsCount = 0

		if letterCount < vowelsMin: # Sanity check
			vowelsMin = letterCount

		for i in range(0, letterCount):
			while 1:
				random_letter = string.uppercase[random.randint(0,len(string.uppercase)-1)]
				if random_letter not in self.exclude_list:
					break
			if random_letter in self.vowels:
				vowelsCount = vowelsCount + 1
			if random_letter == "Q":
				random_letter = "Qu"	
			self.letter_list.append(random_letter)	

		# Randomly assign vowels until reaching vowelsmin	
		while vowelsCount < vowelsMin:
			random_pos = random.randint(0, len(self.letter_list)-1)
			if self.letter_list[random_pos] not in self.vowels:
				self.letter_list[random_pos] =	self.vowels[random.randint(0, len(self.vowels)-1)]
			vowelsCount = vowelsCount + 1

	def get_letter(self, pos):
		return self.letter_list[pos]

class WordList:
	def __init__(self, filename):
		wordlistfile = bz2.BZ2File(filename, "r")
		self.word_list = wordlistfile.readlines()
		wordlistfile.close()
	""" Use binary search """
	def FindWord(self, word):
		R = len(self.word_list)-1
		L = 0
		while 1:
			p = (R-L)/2
			if p == 0:
				break
			p = L + p
			diff = cmp(self.word_list[p], word)
			if diff == 0:
				return True
			elif diff < 0:
				L = p
			else:
				R = p
		return False

		

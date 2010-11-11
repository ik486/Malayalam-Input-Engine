# -*- coding: utf-8 -*-
# vim: set noet ts=4:
#
# scim-python-malayalm
#
# Copyright (c) 2008-2009 Ignatius Kunjumon <ignatius.kunjumon@gmail.com>
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA
#
# $Id: $
#
import scim
from scim import KeyCode
from scim import KeyMask
from scim import IMEngine
from scim import IMEngineFactory
import os
import re
import traceback
#import enchant
import locale
from time import strftime

from gettext import dgettext
_  = lambda a : dgettext ("scim-python", a)
N_ = lambda a : a

class Engine (IMEngine):
	def __init__ (self, factory, config, encoding, id):
		IMEngine.__init__ (self, factory, config, encoding, id)
		self._config = config
		self._preedit_string = u""
		self._cursor = 0
		self.keys = []
		self.keyCount = []
		self.oldkey = None


	def update (self):
		attrs = []
		attrs.append (scim.Attribute (0, len (self._preedit_string), scim.ATTR_FOREGROUND, 0x00ff0000))
		attrs.append (scim.Attribute (0, len (self._preedit_string), scim.ATTR_DECORATE, scim.ATTR_DECORATE_UNDERLINE))
		self.update_preedit_string (self._preedit_string, attrs)
		self.update_preedit_caret (self._cursor)
		if self._preedit_string:
			self.show_preedit_string ()
		else:
			self.hide_preedit_string ()
		
	def myfn(self,m):
		val = m.group()
		if len(val) > 2: return m
		if len(val) < 2: return m
		if val[1] == unichr(0x1111): return unichr(0x0073) + val[0] + unichr(0x006d)
		if val[1] == unichr(0x1112): return unichr(0x0074) + val[0] + unichr(0x006d)
		if val[1] == unichr(0x1113): return unichr(0x0073) + unichr(0x0073) + val[0]
		return val[1] + val[0]


	def malkeyFirst(self, key, keyCount):

                val = {	"a" : [ unichr(0x0041),  unichr(0x0042),  unichr(0x006d),  unichr(0x0075),  unichr(0x006d)],
                        "b" : [ unichr(0x005f),  unichr(0x0060)],
						"c" : [ unichr(0x004e),  unichr(0x004f)],
						"d" : [ unichr(0x0055),  unichr(0x0056),  unichr(0x005a),  unichr(0x005b)],
						"e" : [ unichr(0x0046),  unichr(0x0047),  unichr(0x0073),  unichr(0x0074), unichr(0x0073)+unichr(0x0073)],
						"f" : [ unichr(0x005e)],
						"g" : [ unichr(0x004b),  unichr(0x004c),  unichr(0x004d)],
						"h" : [ unichr(0x0078),  unichr(0x006c)],
						"i" : [ unichr(0x0043),  unichr(0x0043) + unichr(0x0075),  unichr(0x006e),  unichr(0x006f)],
						"j" : [ unichr(0x0050),  unichr(0x0051),  unichr(0x0052)],
						"k" : [ unichr(0x0049),  unichr(0x004a)],
						"l" : [ unichr(0x0065),  unichr(0x0066),  unichr(0x00c2),  unichr(0x00c4)],
						"m" : [ unichr(0x0061),  unichr(0x0077)],
						"n" : [ unichr(0x005c),  unichr(0x0057),  unichr(0x00ac), unichr(0x00b3)],
						"o" : [ unichr(0x0048),  unichr(0x0048)+unichr(0x006d), unichr(0x0048)+unichr(0x0075)],
						"p" : [ unichr(0x005d),  unichr(0x005e)],
						"q" : [ unichr(0x0076)],
						"r" : [ unichr(0x0063),  unichr(0x0064),  unichr(0x00c0)],
						"s" : [ unichr(0x0069),  unichr(0x006a),  unichr(0x006b)],
						"t" : [ unichr(0x0053),  unichr(0x0054),  unichr(0x0058),  unichr(0x0059)],
						"u" : [ unichr(0x0044),  unichr(0x0044)+unichr(0x0075),  unichr(0x0070),  unichr(0x0071)],
						"v" : [ unichr(0x0068)],
						"w" : [ unichr(0x0068)],
                        'x' : [ unichr(0x00fe), unichr(0x00e5)],
						"y" : [ unichr(0x0062)],
						"z" : [ unichr(0x0045),  unichr(0x0067),  unichr(0x0072)],
                        "A" : [  unichr(0x0042) ],
                        "B" : [  unichr(0x00BA),  unichr(0x00BB) ],
                        "C" : [  unichr(0x00A8),  unichr(0x00D1) ],
                        "D" : [  unichr(0x00B1),  unichr(0x00CD) ],
                        "E" : [  unichr(0x0047) ],
                        "F" : [  unichr(0x005E) ],
                        "G" : [  unichr(0x00A4),  unichr(0x00A7) ],
                        "H" : [  unichr(0x00CB), unichr(0x00D3) ],
                        "I" : [  unichr(0x0043) + unichr(0x0075) ],
                        "J" : [  unichr(0x00AA),  unichr(0x00DA),  unichr(0x00D6) ],
                        "K" : [  unichr(0x00A1),  unichr(0x00A2),  unichr(0x00A3) ],
                        "L" : [  unichr(0x00C3),  unichr(0x00C5) ],
                        "M" : [  unichr(0x00BD),  unichr(0x00BE) ],
                        "N" : [  unichr(0x00AE), unichr(0x00B6),  unichr(0x00E2) ],
                        "O" : [  unichr(0x0048) + unichr(0x006D) ],
                        "P" : [  unichr(0x00B8),  unichr(0x00B9),  unichr(0x00D2) ],
                        "Q" : [  unichr(0x0076) ],
                        "R" : [  unichr(0x00E4) ],
                        "S" : [  unichr(0x00C8),  unichr(0x00CA),  unichr(0x00CC) ],
                        "T" : [  unichr(0x00AB),  unichr(0x00AF),  unichr(0x00B0) ],
                        "U" : [  unichr(0x0044) + unichr(0x0075) ],
                        "V" : [  unichr(0x00C6) ],
                        "W" : [  unichr(0x00C6) ],
                        "X" : [  unichr(0x00E5) ],
                        "Y" : [  unichr(0x00BF) ],
                        "Z" : [  unichr(0x0045) ] }

                if key in val:
                        arr = val[key]
                        no = keyCount % len(arr)
                        return arr[no]
                else:
                        return key

	def malkeySecond(self, key, keyCount):

                val = { "a" : [ unichr(0x006d),  unichr(0x0075)],
                        "b" : [ unichr(0x005f),  unichr(0x0060)],
                        "c" : [ unichr(0x004e),  unichr(0x004f)],
                        "d" : [ unichr(0x0055),  unichr(0x0056),  unichr(0x005a),  unichr(0x005b)],
                        "e" : [ unichr(0x0073),  unichr(0x0074),  unichr(0x1113)],
                        "f" : [ unichr(0x005e)],
                        "g" : [ unichr(0x004b),  unichr(0x004c),  unichr(0x004d)],
                        "h" : [ unichr(0x0078),  unichr(0x006c)],
                        "i" : [ unichr(0x006e),  unichr(0x006f)],
                        "j" : [ unichr(0x0050),  unichr(0x0051),  unichr(0x0052)],
                        "k" : [ unichr(0x0049),  unichr(0x004a)],
                        "l" : [ unichr(0x0065),  unichr(0x0066),  unichr(0x00c2),  unichr(0x00c4)],
						"m" : [ unichr(0x0061),  unichr(0x0077)],
                        "n" : [ unichr(0x0057),  unichr(0x005c),  unichr(0x00ac),  unichr(0x00b3)],
                        "o" : [ unichr(0x1111),  unichr(0x1112)],
                        "p" : [ unichr(0x005d),  unichr(0x005e)],
                        "q" : [ unichr(0x0076)],
                        "r" : [ unichr(0x0063),  unichr(0x0064),  unichr(0x00c0)],
                        "s" : [ unichr(0x0069),  unichr(0x006a),  unichr(0x006b)],
                        "t" : [ unichr(0x0053),  unichr(0x0054),  unichr(0x0058),  unichr(0x0059)],
                        "u" : [ unichr(0x0070),  unichr(0x0071)],
                        "v" : [ unichr(0x0068)],
                        "w" : [ unichr(0x0068)],
                        'x' : [ unichr(0x00fe), unichr(0x00e5)],
                        "y" : [ unichr(0x0062)],
                        "z" : [ unichr(0x0072), unichr(0x0067)], 
                        "A" : [  unichr(0x0042) ],
                        "B" : [  unichr(0x00BA),  unichr(0x00BB) ],
                        "C" : [  unichr(0x00A8),  unichr(0x00D1) ],
                        "D" : [  unichr(0x00B1),  unichr(0x00CD) ],
                        "E" : [  unichr(0x0047) ],
                        "F" : [  unichr(0x005E) ],
                        "G" : [  unichr(0x00A4),  unichr(0x00A7) ],
                        "H" : [  unichr(0x00CB), unichr(0x00D3) ],
                        "I" : [  unichr(0x0043) + unichr(0x0075) ],
                        "J" : [  unichr(0x00AA),  unichr(0x00DA),  unichr(0x00D6) ],
                        "K" : [  unichr(0x00A1),  unichr(0x00A2),  unichr(0x00A3) ],
                        "L" : [  unichr(0x00C3),  unichr(0x00C5) ],
                        "M" : [  unichr(0x00BD),  unichr(0x00BE) ],
                        "N" : [  unichr(0x00AE), unichr(0x00B6),  unichr(0x00E2) ],
                        "O" : [  unichr(0x0048) + unichr(0x006D) ],
                        "P" : [  unichr(0x00B8),  unichr(0x00B9),  unichr(0x00D2) ],
                        "Q" : [  unichr(0x0076) ],
                        "R" : [  unichr(0x00E4) ],
                        "S" : [  unichr(0x00CA),  unichr(0x00C8),  unichr(0x00CC) ],
                        "T" : [  unichr(0x00AB),  unichr(0x00AF),  unichr(0x00B0) ],
                        "U" : [  unichr(0x0044) + unichr(0x0075) ],
                        "V" : [  unichr(0x00C6) ],
                        "W" : [  unichr(0x00C6) ],
                        "X" : [  unichr(0x00E5) ],
                        "Y" : [  unichr(0x00BF) ],
                        "Z" : [  unichr(0x0045) ]}

                if key in val:
                        arr = val[key]
                        no = keyCount % len(arr)
                        return arr[no]
                else:
                        return key


	def koot_replace(self, val):
			pppp = val[:]

			pppp = pppp.replace(unichr(0x006b)+unichr(0x0076)+unichr(0x0064)+unichr(0x0076)+unichr(0x0064), unichr(0x00cc))
			pppp = pppp.replace(unichr(0x0049)+unichr(0x0076)+unichr(0x0058), unichr(0x00e0))
			pppp = pppp.replace(unichr(0x0057)+unichr(0x0076)+unichr(0x005b), unichr(0x00de))
			pppp = pppp.replace(unichr(0x0069)+unichr(0x0076)+unichr(0x004e), unichr(0x00dd))
			pppp = pppp.replace(unichr(0x004b)+unichr(0x0076)+unichr(0x0061), unichr(0x00dc))
			pppp = pppp.replace(unichr(0x0058)+unichr(0x0076)+unichr(0x0060), unichr(0x00db))
			pppp = pppp.replace(unichr(0x0050)+unichr(0x0076)+unichr(0x0052), unichr(0x00da))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x0059), unichr(0x00d9))
			pppp = pppp.replace(unichr(0x006c)+unichr(0x0076)+unichr(0x0061), unichr(0x00d2))
			pppp = pppp.replace(unichr(0x004e)+unichr(0x0076)+unichr(0x004f), unichr(0x00d1))
			pppp = pppp.replace(unichr(0x005f)+unichr(0x0076)+unichr(0x005a), unichr(0x00d0))
			pppp = pppp.replace(unichr(0x005f)+unichr(0x0076)+unichr(0x005b), unichr(0x00cf))
			pppp = pppp.replace(unichr(0x0049)+unichr(0x0076)+unichr(0x0053), unichr(0x00ce))
			pppp = pppp.replace(unichr(0x006c)+unichr(0x0076)+unichr(0x0066), unichr(0x00cb))
			pppp = pppp.replace(unichr(0x006b)+unichr(0x0076)+unichr(0x006b), unichr(0x00ca))
			pppp = pppp.replace(unichr(0x006b)+unichr(0x0076)+unichr(0x0066), unichr(0x00c9))
			pppp = pppp.replace(unichr(0x005f)+unichr(0x0076)+unichr(0x0066), unichr(0x00bb))
			pppp = pppp.replace(unichr(0x0062)+unichr(0x0076)+unichr(0x0062), unichr(0x00bf))
			pppp = pppp.replace(unichr(0x0068)+unichr(0x0076)+unichr(0x0068), unichr(0x00c6))
			pppp = pppp.replace(unichr(0x0058)+unichr(0x0076)+unichr(0x0058), unichr(0x00af))
			pppp = pppp.replace(unichr(0x0064)+unichr(0x0076)+unichr(0x0064), unichr(0x00e4))
			pppp = pppp.replace(unichr(0x0050)+unichr(0x0076)+unichr(0x0050), unichr(0x00d6))
			pppp = pppp.replace(unichr(0x005a)+unichr(0x0076)+unichr(0x005a), unichr(0x00b1))
			pppp = pppp.replace(unichr(0x005f)+unichr(0x0076)+unichr(0x005f), unichr(0x00ba))
			pppp = pppp.replace(unichr(0x004e)+unichr(0x0076)+unichr(0x004e), unichr(0x00a8))
			pppp = pppp.replace(unichr(0x0055)+unichr(0x0076)+unichr(0x0055), unichr(0x00cd))
			pppp = pppp.replace(unichr(0x0055)+unichr(0x0076)+unichr(0x0056), unichr(0x00B2))
			pppp = pppp.replace(unichr(0x004b)+unichr(0x0076)+unichr(0x004b), unichr(0x00a4))
			pppp = pppp.replace(unichr(0x004b)+unichr(0x0076)+unichr(0x0061), unichr(0x00DC))
			pppp = pppp.replace(unichr(0x004b)+unichr(0x0076)+unichr(0x005c), unichr(0x00e1))
			pppp = pppp.replace(unichr(0x004d)+unichr(0x0076)+unichr(0x004e), unichr(0x00a9))
			pppp = pppp.replace(unichr(0x004d)+unichr(0x0076)+unichr(0x004d), unichr(0x00a7))
			pppp = pppp.replace(unichr(0x0052)+unichr(0x0076)+unichr(0x0052), unichr(0x00aa))
			pppp = pppp.replace(unichr(0x006c)+unichr(0x0076)+unichr(0x0066), unichr(0x00CB))
			pppp = pppp.replace(unichr(0x006c)+unichr(0x0076)+unichr(0x005c), unichr(0x00d3))
			pppp = pppp.replace(unichr(0x0049)+unichr(0x0076)+unichr(0x0049), unichr(0x00a1))
			pppp = pppp.replace(unichr(0x0049)+unichr(0x0076)+unichr(0x0066), unichr(0x00a2))
			pppp = pppp.replace(unichr(0x0049)+unichr(0x0076)+unichr(0x006a), unichr(0x00a3))
			pppp = pppp.replace(unichr(0x0065)+unichr(0x0076)+unichr(0x0065), unichr(0x00c3))
			pppp = pppp.replace(unichr(0x0066)+unichr(0x0076)+unichr(0x0066), unichr(0x00c5))
			pppp = pppp.replace(unichr(0x0065)+unichr(0x0076)+unichr(0x005d), unichr(0x00e5))
			pppp = pppp.replace(unichr(0x0061)+unichr(0x0076)+unichr(0x0066), unichr(0x00be))
			pppp = pppp.replace(unichr(0x0061)+unichr(0x0076)+unichr(0x0061), unichr(0x00bd))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x005a), unichr(0x00b5))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x005b), unichr(0x00d4))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x0049), unichr(0x00a6))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x0061), unichr(0x00b7))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x005c), unichr(0x00b6))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x005d), unichr(0x00bc))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x0058), unichr(0x00b4))
			pppp = pppp.replace(unichr(0x005c)+unichr(0x0076)+unichr(0x0059), unichr(0x00B4))
			pppp = pppp.replace(unichr(0x0057)+unichr(0x0076)+unichr(0x0056), unichr(0x00DE))
			pppp = pppp.replace(unichr(0x0057)+unichr(0x0076)+unichr(0x0061), unichr(0x00d7))
			pppp = pppp.replace(unichr(0x0057)+unichr(0x0076)+unichr(0x0057), unichr(0x00ae))
			pppp = pppp.replace(unichr(0x00b3)+unichr(0x0076)+unichr(0x0064), unichr(0x00e2))
			pppp = pppp.replace(unichr(0x005d)+unichr(0x0076)+unichr(0x0066), unichr(0x00b9))
			pppp = pppp.replace(unichr(0x005d)+unichr(0x0076)+unichr(0x005d), unichr(0x00b8))
			pppp = pppp.replace(unichr(0x006b)+unichr(0x0076)+unichr(0x0059), unichr(0x00d8))
			pppp = pppp.replace(unichr(0x0069)+unichr(0x0076)+unichr(0x0066), unichr(0x00c7))
			pppp = pppp.replace(unichr(0x0069)+unichr(0x0076)+unichr(0x0069), unichr(0x00c8))
			pppp = pppp.replace(unichr(0x006a)+unichr(0x0076)+unichr(0x0066), unichr(0x00c7))
			pppp = pppp.replace(unichr(0x006a)+unichr(0x0076)+unichr(0x006a), unichr(0x00c8))
			pppp = pppp.replace(unichr(0x006a)+unichr(0x0076)+unichr(0x0053), unichr(0x00e3))
			pppp = pppp.replace(unichr(0x0053)+unichr(0x0076)+unichr(0x0053), unichr(0x00ab))
			pppp = pppp.replace(unichr(0x0054)+unichr(0x0076)+unichr(0x0054), unichr(0x00ab))
			pppp = pppp.replace(unichr(0x0054)+unichr(0x0076)+unichr(0x0058), unichr(0x00b0))
			pppp = pppp.replace(unichr(0x0058)+unichr(0x0076)+unichr(0x006b), unichr(0x00d5))
			pppp = pppp.replace(unichr(0x0058)+unichr(0x0076)+unichr(0x0061), unichr(0x00df))
			pppp = pppp.replace(unichr(0x0058)+unichr(0x0076)+unichr(0x0069), unichr(0x00D5))
			pppp = pppp.replace(unichr(0x0062)+unichr(0x0076)+unichr(0x0049), unichr(0x00ed))
			pppp = pppp.replace(unichr(0x0076)+unichr(0x0062), unichr(0x0079))
			pppp = pppp.replace(unichr(0x0076)+unichr(0x0068), unichr(0x007a))
			pppp = pppp.replace(unichr(0x0076)+unichr(0x0063), unichr(0x007b))
			pppp = pppp.replace(unichr(0x0076)+unichr(0x0064), unichr(0x007b))
			pppp = re.sub(".["+unichr(0x1111)+unichr(0x1112)+unichr(0x1113)+unichr(0x0073)+unichr(0x0074)+unichr(0x007b)+"]",self.myfn,pppp)
			ppp1 = ""
			fset  = [unichr(0x0073), unichr(0x0074), unichr(0x007b)] 
			bset  = [unichr(0x0076), unichr(0x0070), unichr(0x0071)] 
			bset += [unichr(0x006d), unichr(0x0075), unichr(0x0077)] 
			bset += [unichr(0x0078), unichr(0x007a), unichr(0x0079)] 
			bset += [unichr(0x0072), unichr(0x006e), unichr(0x006f)] 
			nn = len(pppp) -1
			for i in range(nn):
				if pppp[i] in fset:
						ppp1 = ppp1 + pppp[i]
						continue
				if pppp[i+1] in bset:
						ppp1 = ppp1 + pppp[i]
						continue
				ppp1 = ppp1 + pppp[i] + '-'
			return ppp1 + pppp[-1] + '-'

	def processData(self):
		if not len(self.keys): return u""
		out = self.malkeyFirst(self.keys[0], self.keyCount[0])
		for i in range(1, len(self.keys)):
			if self.keys[i] in ['a', 'e', 'i', 'o', 'u', 'z', 'q']:
				out = out + self.malkeySecond(self.keys[i], self.keyCount[i])
			else:
				out += self.malkeySecond(self.keys[i], self.keyCount[i])
		out = self.koot_replace(out)
		self._preedit_string = out
		return out


	def process_key_event (self, key):
		if key.mask & KeyMask.ReleaseMask: # Ignore release event
			return False
		if key.mask & KeyMask.ControlMask:
			return False
		
		if ((key.code >= KeyCode.KEY_A and key.code <= KeyCode.KEY_Z) or (key.code >= KeyCode.KEY_a and key.code <= KeyCode.KEY_z)):
			if self.oldkey == key.code:
				last = self.keyCount.pop()
				self.keyCount.append(last+1)
			else:
				self.keys.append(chr(key.code))
				self.keyCount.append(0)
			self.processData()
			self._cursor = len(self._preedit_string)
			self.update()
			self.oldkey = key.code
			return True

		if key == KeyCode.KEY_BackSpace:
			txt = self.keys
			if len(txt):
				last = self.keyCount.pop()
				if last:
					self.keyCount.append(last-1)
				else:
					last = self.keys.pop()
			self.processData()
			self._cursor = len(self._preedit_string)
			self.update()
			self.oldkey = key.code
			return True

		
		if self._preedit_string:
			self.commit_string ()
			self.keys = []
			self.keyCount = []
			self.oldkey = None
			self._preedit_string = u""
		return False
		

	
	def commit_string (self, string1 = None):
		string = self._preedit_string
		self._preedit_string = u""
		self._cursor = 0
		IMEngine.commit_string (self, string)
		self.update ()
		self.keys = []
		self.keyCount = []
		self.oldkey = 0

	def move_preedit_caret (self, pos):
		IMEngine.move_preedit_caret (self, pos)
	
	def select_candidate (self, index):
		IMEngine.select_candidate (self, index)

	def reset (self):
		#self._preedit_string = u"RESET"
		self.oldkey = 0
		self._cursor = 0
		self.update ()
		IMEngine.reset (self)

	def focus_in (self):
		IMEngine.focus_in (self)
		self.update ()
	
	def focus_out (self):
		self.reset ()
		IMEngine.focus_out (self)

	def trigger_property (self, property):
		IMEngine.trigger_property (self, property)

	def process_helper_event (self, helper_uuid, trans):
		IMEngine.process_helper_event (self, helper_uuid, trans)

	def update_client_capabilities (self, cap):
		IMEngine.update_client_capabilities (self, cap)


class Factory (IMEngineFactory):
	def __init__ (self, config):
		IMEngineFactory.__init__ (self, config)
		self._config	= config
		self.name 		= _(u"ikcusat ASCII")
		self.uuid 		= "7fsddae9-2222-4d7a-b255-f4332134df99"
		self.authors	= u"Ignatius Kunjumon <ignatius.kunjumon@gmail.com>"
		self.icon_file 	= "/usr/share/scim/icons/scim-python.png"
		self.credits 	= u"GPL"
		self.help		= _(u"Help For IKCUSAT Malayalam\nok")
		self.set_languages ("ml")
		# locale.setlocale (locale.LC_ALL, "en_US.UTF-8")

	def create_instance (self, encoding, id):
		return Engine (self, self._config, encoding, id)

	def reload_config (self, config):
		pass		

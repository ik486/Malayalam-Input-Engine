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
import traceback
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
		
	def englishKey(self, key):
		if   key == KeyCode.KEY_A: self._preedit_string = u"a"
		elif key == KeyCode.KEY_B: self._preedit_string = u"b"
		elif key == KeyCode.KEY_C: self._preedit_string = u"c"
		elif key == KeyCode.KEY_D: self._preedit_string = u"d"
		elif key == KeyCode.KEY_E: self._preedit_string = u"e"
		elif key == KeyCode.KEY_F: self._preedit_string = u"f"
		elif key == KeyCode.KEY_G: self._preedit_string = u"g"
		elif key == KeyCode.KEY_H: self._preedit_string = u"h"
		elif key == KeyCode.KEY_I: self._preedit_string = u"i"
		elif key == KeyCode.KEY_J: self._preedit_string = u"j"
		elif key == KeyCode.KEY_K: self._preedit_string = u"k"
		elif key == KeyCode.KEY_L: self._preedit_string = u"l"
		elif key == KeyCode.KEY_M: self._preedit_string = u"m"
		elif key == KeyCode.KEY_N: self._preedit_string = u"n"
		elif key == KeyCode.KEY_O: self._preedit_string = u"o"
		elif key == KeyCode.KEY_P: self._preedit_string = u"p"
		elif key == KeyCode.KEY_Q: self._preedit_string = u"q"
		elif key == KeyCode.KEY_R: self._preedit_string = u"r"
		elif key == KeyCode.KEY_S: self._preedit_string = u"s"
		elif key == KeyCode.KEY_T: self._preedit_string = u"t"
		elif key == KeyCode.KEY_U: self._preedit_string = u"u"
		elif key == KeyCode.KEY_V: self._preedit_string = u"v"
		elif key == KeyCode.KEY_W: self._preedit_string = u"w"
		elif key == KeyCode.KEY_X: self._preedit_string = u"x"
		elif key == KeyCode.KEY_Y: self._preedit_string = u"y"
		elif key == KeyCode.KEY_Z: self._preedit_string = u"z"
		elif key == KeyCode.KEY_a: self._preedit_string = u"A"
		elif key == KeyCode.KEY_b: self._preedit_string = u"B"
		elif key == KeyCode.KEY_c: self._preedit_string = u"C"
		elif key == KeyCode.KEY_d: self._preedit_string = u"D"
		elif key == KeyCode.KEY_e: self._preedit_string = u"E"
		elif key == KeyCode.KEY_f: self._preedit_string = u"F"
		elif key == KeyCode.KEY_g: self._preedit_string = u"G"
		elif key == KeyCode.KEY_h: self._preedit_string = u"H"
		elif key == KeyCode.KEY_i: self._preedit_string = u"I"
		elif key == KeyCode.KEY_j: self._preedit_string = u"J"
		elif key == KeyCode.KEY_k: self._preedit_string = u"K"
		elif key == KeyCode.KEY_l: self._preedit_string = u"L"
		elif key == KeyCode.KEY_m: self._preedit_string = u"M"
		elif key == KeyCode.KEY_n: self._preedit_string = u"N"
		elif key == KeyCode.KEY_o: self._preedit_string = u"O"
		elif key == KeyCode.KEY_p: self._preedit_string = u"P"
		elif key == KeyCode.KEY_q: self._preedit_string = u"Q"
		elif key == KeyCode.KEY_r: self._preedit_string = u"R"
		elif key == KeyCode.KEY_s: self._preedit_string = u"S"
		elif key == KeyCode.KEY_t: self._preedit_string = u"T"
		elif key == KeyCode.KEY_u: self._preedit_string = u"U"
		elif key == KeyCode.KEY_v: self._preedit_string = u"V"
		elif key == KeyCode.KEY_w: self._preedit_string = u"W"
		elif key == KeyCode.KEY_x: self._preedit_string = u"X"
		elif key == KeyCode.KEY_y: self._preedit_string = u"Y"
		elif key == KeyCode.KEY_z: self._preedit_string = u"Z"
		else: return False
		self.commit_string ()
		self.keys = []
		self.keyCount = []
		self.oldkey = None
		self._preedit_string = u""
		return True

	def malkeyFirst(self, key, keyCount):
                bbb = unichr(0x0d4d)
                ZWJ  = unichr(0x200d)
                ZWNJ = unichr(0x200c)
                val =  {'a' : [unichr(0x0d05), unichr(0x0d06), unichr(0x0d3e)],
                        'b' : [unichr(0x0d2c), unichr(0x0d2d)],
                        'c' : [unichr(0x0d1a), unichr(0x0d1b)],
                        'd' : [unichr(0x0d21), unichr(0x0d22), unichr(0x0d27), unichr(0x0d26)],
                        'e' : [unichr(0x0d0e), unichr(0x0d0f), unichr(0x0d10), unichr(0x0d46), unichr(0x0d47), unichr(0x0d48)],
                        'f' : [unichr(0x0d2b)],
                        'g' : [unichr(0x0d17), unichr(0x0d18), unichr(0x0d19)],
                        'h' : [unichr(0x0d39), unichr(0x0d03)],
                        'i' : [unichr(0x0d07), unichr(0x0d08), unichr(0x0d3f), unichr(0x0d40)],
                        'j' : [unichr(0x0d1e), unichr(0x0d1c), unichr(0x0d1d)],
                        'k' : [unichr(0x0d15), unichr(0x0d16)],
                        'l' : [unichr(0x0d32), unichr(0x0d33), unichr(0x0d34)],
                        'm' : [unichr(0x0d2e), unichr(0x0d02)],
                        'n' : [unichr(0x0d28), unichr(0x0d23)],
                        'o' : [unichr(0x0d12), unichr(0x0d13), unichr(0x0d14), unichr(0x0d4a), unichr(0x0d4b), unichr(0x0d57)],
                        'p' : [unichr(0x0d2a), unichr(0x0d2b)],
                        'q' : [bbb, bbb + ZWJ, bbb + ZWNJ],
                        'r' : [unichr(0x0d31), unichr(0x0d30)],
                        's' : [unichr(0x0d38), unichr(0x0d36), unichr(0x0d37)],
                        't' : [unichr(0x0d24), unichr(0x0d1f), unichr(0x0d20), unichr(0x0d25)],
                        'u' : [unichr(0x0d09), unichr(0x0d0a), unichr(0x0d41), unichr(0x0d42)],
                        'v' : [unichr(0x0d35)],
                        'w' : [unichr(0x0d35)],
                        'x' : [],
                        'y' : [unichr(0x0d2f)],
                        'z' : [unichr(0x0d0b), unichr(0x0d60), unichr(0x0d0c), unichr(0x0d61), unichr(0x0d43)]}

                if key == 'x':
                        return key
                elif key in val:
                        arr = val[key]
                        no = keyCount % len(arr)
                        return arr[no]
                else:
                        return key

	def malkeySecond(self, key, keyCount):
                bbb = unichr(0x0d4d)
                ZWJ  = unichr(0x200d)
                ZWNJ = unichr(0x200c)
                val =  {'a' : [unichr(0x0d3e)],
                        'b' : [unichr(0x0d2c), unichr(0x0d2d)],
                        'c' : [unichr(0x0d1a), unichr(0x0d1b)],
                        'd' : [unichr(0x0d21), unichr(0x0d22), unichr(0x0d27), unichr(0x0d26)],
                        'e' : [unichr(0x0d46), unichr(0x0d47), unichr(0x0d48)],
                        'f' : [unichr(0x0d2b)],
                        'g' : [unichr(0x0d17), unichr(0x0d18), unichr(0x0d19)],
                        'h' : [unichr(0x0d39), unichr(0x0d03)],
                        'i' : [unichr(0x0d3f), unichr(0x0d40)],
                        'j' : [unichr(0x0d1e), unichr(0x0d1c), unichr(0x0d1d)],
                        'k' : [unichr(0x0d15), unichr(0x0d16)],
                        'l' : [unichr(0x0d32), unichr(0x0d33), unichr(0x0d34)],
                        'm' : [unichr(0x0d2e), unichr(0x0d02)],
                        'n' : [unichr(0x0d28), unichr(0x0d23)],
                        'o' : [unichr(0x0d4a), unichr(0x0d4b), unichr(0x0d57)],
                        'p' : [unichr(0x0d2a), unichr(0x0d2b)],
                        'q' : [bbb, bbb + ZWJ, bbb + ZWNJ],
                        'r' : [unichr(0x0d31), unichr(0x0d30)],
                        's' : [unichr(0x0d38), unichr(0x0d36), unichr(0x0d37)],
                        't' : [unichr(0x0d24), unichr(0x0d1f), unichr(0x0d20), unichr(0x0d25)],
                        'u' : [unichr(0x0d41), unichr(0x0d42)],
                        'v' : [unichr(0x0d35)],
                        'w' : [unichr(0x0d35)],
                        'x' : [],
                        'y' : [unichr(0x0d2f)],
                        'z' : [unichr(0x0d43)]}

                if key == 'x':
                        return key
                elif key in val:
                        arr = val[key]
                        no = keyCount % len(arr)
                        return arr[no]
                else:
                        return key

	def koot(self, out, i):
		if i > 0:
			key = self.keys[i-1]
			if key == 'a' or key == 'e' or key == 'i' or key == 'o' or key == 'u' or key == 'z' or key == 'q':
				return out
		bbb = unichr(0x0d4d)
		count = self.keyCount[i] + 1
		if len(out) >= 1:
			if count == 1:
				out = out + bbb + out[-1]
			elif count % 2:
				out = out[:-2]
			else:
				out = out + bbb + out[-1]
			return out
		else: return out

	def processData(self):
		if not len(self.keys): return u""
		out = self.malkeyFirst(self.keys[0], self.keyCount[0])
		for i in range(1, len(self.keys)):
			if self.keys[i] in ['a', 'e', 'i', 'o', 'u', 'z', 'q']:
				if i > 1:
					j = i - 1
					if self.keys[j] in ['a', 'e', 'i', 'o', 'u', 'z', 'q']:
						if out[-1] == unichr(0x200c) or out[-1] == unichr(0x200d):
							out = out[:-2] + self.malkeySecond(self.keys[i], self.keyCount[i])
						else:
							out = out[:-1] + self.malkeySecond(self.keys[i], self.keyCount[i])
					else:
						out = out + self.malkeySecond(self.keys[i], self.keyCount[i])
				else:
					out = out + self.malkeySecond(self.keys[i], self.keyCount[i])
			elif self.keys[i] == 'x':
				out = self.koot(out, i)
			else:
				out += self.malkeySecond(self.keys[i], self.keyCount[i])
		self._preedit_string = out
		return out


	def process_key_event (self, key):
		if key.mask & KeyMask.ReleaseMask: # Ignore release event
			return False
		if key.mask & KeyMask.ControlMask:
			return False
		if key.mask & KeyMask.CapsLockMask:
			return self.englishKey(key.code)
		
		if (key.code >= KeyCode.KEY_A and key.code <= KeyCode.KEY_Z):
			pass

		if (key.code >= KeyCode.KEY_a and key.code <= KeyCode.KEY_z):
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
		

	def rightChar(self, ch):
		if ord(ch) == 0x200d: return 1
		if ord(ch) == 0x200c: return 1
		if ord(ch) == 0x0D3e: return 1
		if ord(ch) == 0x0D3f: return 1
		if ord(ch) == 0x0D40: return 1
		if ord(ch) == 0x0D41: return 1
		if ord(ch) == 0x0D42: return 1
		if ord(ch) == 0x0D43: return 1
		if ord(ch) == 0x0D46: return 1
		if ord(ch) == 0x0D47: return 1
		if ord(ch) == 0x0D48: return 1
		if ord(ch) == 0x0D4a: return 1
		if ord(ch) == 0x0D4b: return 1
		if ord(ch) == 0x0D4c: return 1
		if ord(ch) == 0x0D4d: return 1
		if ord(ch) == 0x0D02: return 1
		if ord(ch) == 0x0D03: return 1
		return 0

	def leftChar(self, ch):
		if ord(ch) == 0x0D4d: return 1
		return 0


	def addZWS(self, string):
		n = len(string)
		if not n: return string
		if ord(string[0]) < 3000: return string
		aa = u""
		ZWS = unichr(0x200b)
		for i in range(n-1):
			if i < n-3:
				if ord(string[i+3]) == 0x200d:
					aa = aa + string[i]
					continue
			if self.rightChar(string[i+1]):
				aa = aa + string[i]
				continue
			if self.leftChar(string[i]):
				aa = aa + string[i]
				continue
			aa = aa + string[i] + ZWS
		aa = aa + string[-1]
		aa = ZWS + aa
		return aa

	
	def commit_string (self, string1 = None):
		self._preedit_string = self.addZWS(self._preedit_string)
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
		self.name 		= _(u"ikcusat UNICODE")
		self.uuid 		= "7fb43ae9-1111-4d7a-b255-f437ce28d599"
		self.authors	= u"Ignatius Kunjumon <ignatius.kunjumon@gmail.com>"
		self.icon_file 	= "/usr/share/scim/icons/scim-python.png"
		self.credits 	= u"GPL"
		self.help		= _(u"Help For GNUSofts Malayalam\nok")
		self.set_languages ("ml")
		# locale.setlocale (locale.LC_ALL, "en_US.UTF-8")

	def create_instance (self, encoding, id):
		return Engine (self, self._config, encoding, id)

	def reload_config (self, config):
		pass		

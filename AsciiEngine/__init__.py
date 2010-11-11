# -*- coding: utf-8 -*-
# vim: set noet ts=4:
#
# scim-python
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
import MalayalamAscii

def get_factorys (config):
	return [MalayalamAscii.Factory (config)]

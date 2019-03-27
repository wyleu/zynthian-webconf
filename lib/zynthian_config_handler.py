# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: Zynthian Web Configurator
#
# Zynthian Configuration Handler base class
#
# Copyright (C) 2017 Fernando Moyano <jofemodo@zynthian.org>
#
#********************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
#
#********************************************************************

import os
import re
import sys
import liblo
import logging
import tornado.web
from subprocess import check_output

sys.path.append(os.environ.get('ZYNTHIAN_UI_DIR'))
import zynconf

#------------------------------------------------------------------------------
# Zynthian-UI OSC Address
#------------------------------------------------------------------------------

zynthian_ui_osc_addr = liblo.Address('localhost',1370,liblo.UDP)

#------------------------------------------------------------------------------
# Zynthian Basic Handler
#------------------------------------------------------------------------------

class ZynthianBasicHandler(tornado.web.RequestHandler):

	def get_current_user(self):
		return self.get_secure_cookie("user")


	def prepare(self):
		self.genjson=False
		try:
			if self.get_query_argument("json"):
				self.genjson=True
		except:
			pass


	def restart_ui(self):
		try:
			check_output("systemctl daemon-reload;systemctl stop zynthian;systemctl start zynthian", shell=True)
		except Exception as e:
			logging.error("Restarting UI: %s" % e)


	def reload_midi_config(self):
		liblo.send(zynthian_ui_osc_addr, "RELOAD_MIDI_CONFIG")


	def needs_reboot(self):
		return False


#------------------------------------------------------------------------------
# Zynthian Config Handler
#------------------------------------------------------------------------------

class ZynthianConfigHandler(ZynthianBasicHandler):

	def prepare(self):
		zynconf.load_config()
		zynconf.load_midi_config()
		super().prepare()


	def update_config(self, config):
		sconfig={}
		for vn in config:
			sconfig[vn]=config[vn][0]

		zynconf.save_config(sconfig, update_sys=True)


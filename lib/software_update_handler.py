# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: Zynthian Web Configurator
#
# Software Update Handler
#
# Copyright (C) 2017 Markus Heidt <markus@heidt-tech.com>
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

import logging

import tornado.web
import tornado.websocket
from collections import OrderedDict
import subprocess
import jsonpickle
from lib.zynthian_websocket_handler import ZynthianWebSocketMessageHandler, ZynthianWebSocketMessage

UPDATE_COMMANDS = OrderedDict([
		#['Diagnosis', 'echo "Not implemented yet"'],
		#['Reset to Factory Settings', 'echo "Not implemented yet"'],
		['Update Software', '/zynthian/zynthian-sys/scripts/update_zynthian.sh']
	]
)

#------------------------------------------------------------------------------
# SoftwareUpdateHandler Config Handler
#------------------------------------------------------------------------------

class SoftwareUpdateHandler(tornado.web.RequestHandler):

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def prepare(self):
		self.genjson=False
		try:
			if self.get_query_argument("json"):
				self.genjson=True
		except:
			pass

	@tornado.web.authenticated
	def get(self, errors=None):
		config=OrderedDict([])

		config['UPDATE_COMMANDS'] = UPDATE_COMMANDS.keys()

		if self.genjson:
			self.write(config)
		else:
			self.render("config.html", body="update.html", config=config, title="Update", errors=errors)


class SoftwareUpdateMessageHandler(ZynthianWebSocketMessageHandler):
	@classmethod
	def is_registered_for(cls, handler_name):
		return handler_name == 'SoftwareUpdateMessageHandler'

	def on_websocket_message(self, update_command):
		p = subprocess.Popen(UPDATE_COMMANDS[update_command], shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		for line in p.stdout:
			logging.info(line.decode())
			message = ZynthianWebSocketMessage('SoftwareUpdateMessageHandler', line.decode())
			self.websocket.write_message(jsonpickle.encode(message))

		message = ZynthianWebSocketMessage('SoftwareUpdateMessageHandler', "EOCOMMAND")
		self.websocket.write_message(jsonpickle.encode(message))

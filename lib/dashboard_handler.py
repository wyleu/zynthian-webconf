# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: Zynthian Web Configurator
#
# Dashboard Handler
#
# Copyright (C) 2018 Fernando Moyano <jofemodo@zynthian.org>
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
import logging
import tornado.web
from subprocess import check_output
from collections import OrderedDict
from lib.zynthian_config_handler import ZynthianConfigHandler

sys.path.append(os.environ.get('ZYNTHIAN_UI_DIR'))
import zynconf

#------------------------------------------------------------------------------
# Dashboard Handler
#------------------------------------------------------------------------------

class DashboardHandler(ZynthianConfigHandler):

	@tornado.web.authenticated
	def get(self):
		# Get git info
		git_info_zyncoder=self.get_git_info("/zynthian/zyncoder")
		git_info_ui=self.get_git_info("/zynthian/zynthian-ui")
		git_info_sys=self.get_git_info("/zynthian/zynthian-sys")
		git_info_webconf=self.get_git_info("/zynthian/zynthian-webconf")
		git_info_data=self.get_git_info("/zynthian/zynthian-data")

		# Get Memory & SD Card info
		ram_info=self.get_ram_info()
		sd_info=self.get_sd_info()

		config=OrderedDict([
			['HARDWARE', OrderedDict([
				['RBPI_VERSION', {
					'title': os.environ.get('RBPI_VERSION')
				}],
				['SOUNDCARD_NAME', {
					'title': 'Soundcard',
					'value': os.environ.get('SOUNDCARD_NAME'),
					'url': "/hw-audio"
				}],
				['DISPLAY_NAME', {
					'title': 'Display',
					'value': os.environ.get('DISPLAY_NAME'),
					'url': "/hw-display"
				}],
				['WIRING_LAYOUT', {
					'title': 'Wiring',
					'value': os.environ.get('ZYNTHIAN_WIRING_LAYOUT'),
					'url': "/hw-wiring"
				}],
				['GPIO_EXPANDER', {
					'title': 'GPIO Expander',
					'value': self.get_gpio_expander(),
					'url': "/hw-wiring"
				}]
			])],
			['SYSTEM', OrderedDict([
				['OS_INFO', {
					'title': 'OS',
					'value': "{}".format(self.get_os_info())
				}],
				['BUILD_DATE', {
					'title': 'Build Date',
					'value': self.get_build_info()['Timestamp'],
				}],
				['RAM', {
					'title': 'Memory',
					'value': "{} ({}/{})".format(ram_info['usage'],ram_info['used'],ram_info['total'])
				}],
				['SD CARD', {
					'title': 'SD Card',
					'value': "{} ({}/{})".format(sd_info['usage'],sd_info['used'],sd_info['total'])
				}],
				['TEMPERATURE', {
					'title': 'Temperature',
					'value': self.get_temperature()
				}]
			])],
			['MIDI', OrderedDict([
				['PROFILE', {
					'title': 'Profile',
					'value': os.path.basename(os.environ.get('ZYNTHIAN_SCRIPT_MIDI_PROFILE',"")),
					'url': "/ui-midi-options"
				}],
				['FINE_TUNING', {
					'title': 'Fine Tuning',
					'value': "{} Hz".format(os.environ.get('ZYNTHIAN_MIDI_FINE_TUNING',"440")),
					'url': "/ui-midi-options"
				}],
				['MASTER_CHANNEL', {
					'title': 'Master Channel',
					'value': os.environ.get('ZYNTHIAN_MIDI_MASTER_CHANNEL',"16"),
					'url': "/ui-midi-options"
				}],
				['QMIDINET', {
					'title': 'QmidiNet',
					'value': str(self.is_service_active("qmidinet")),
					'url': "/ui-midi-options"
				}],
				['TOUCHOSC', {
					'title': 'TouchOSC',
					'value': str(self.is_service_active("touchosc2midi")),
					'url': "/ui-midi-options"
				}]
			])],
			['SOFTWARE', OrderedDict([
				['ZYNCODER', {
					'title': 'zyncoder',
					'value': "{} ({})".format(git_info_zyncoder['branch'], git_info_zyncoder['gitid'][0:7]),
					'url': "https://github.com/zynthian/zyncoder/commit/{}".format(git_info_zyncoder['gitid'])
				}],
				['UI', {
					'title': 'zynthian-ui',
					'value': "{} ({})".format(git_info_ui['branch'], git_info_ui['gitid'][0:7]),
					'url': "https://github.com/zynthian/zynthian-ui/commit/{}".format(git_info_ui['gitid'])
				}],
				['SYS', {
					'title': 'zynthian-sys',
					'value': "{} ({})".format(git_info_sys['branch'], git_info_sys['gitid'][0:7]),
					'url': "https://github.com/zynthian/zynthian-sys/commit/{}".format(git_info_sys['gitid'])
				}],
				['DATA', {
					'title': 'zynthian-data',
					'value': "{} ({})".format(git_info_data['branch'], git_info_data['gitid'][0:7]),
					'url': "https://github.com/zynthian/zynthian-data/commit/{}".format(git_info_data['gitid'])
				}],
				['WEBCONF', {
					'title': 'zynthian-webconf',
					'value': "{} ({})".format(git_info_webconf['branch'], git_info_webconf['gitid'][0:7]),
					'url': "https://github.com/zynthian/zynthian-webconf/commit/{}".format(git_info_webconf['gitid'])
				}]
			])],
			['LIBRARY', OrderedDict([
				['SNAPSHOTS', {
					'title': 'Snapshots',
					'value': str(self.get_num_of_files(os.environ.get('ZYNTHIAN_MY_DATA_DIR')+"/snapshots")),
					'url': "/lib-snapshot"
				}],
				['USER_PRESETS', {
					'title': 'User Presets',
					'value': str(self.get_num_of_presets(os.environ.get('ZYNTHIAN_MY_DATA_DIR')+"/presets")),
					'url': "/lib-presets"
				}],
				['USER_SOUNDFONTS', {
					'title': 'User Soundfonts',
					'value': str(self.get_num_of_files(os.environ.get('ZYNTHIAN_MY_DATA_DIR')+"/soundfonts")),
					'url': "/lib-soundfont"
				}],
				['AUDIO_CAPTURES', {
					'title': 'Audio Captures',
					'value': str(self.get_num_of_files(os.environ.get('ZYNTHIAN_MY_DATA_DIR')+"/capture","*.wav")),
					'url': "/lib-captures"
				}],
				['MIDI_CAPTURES', {
					'title': 'MIDI Captures',
					'value': str(self.get_num_of_files(os.environ.get('ZYNTHIAN_MY_DATA_DIR')+"/capture","*.mid")),
					'url': "/lib-captures"
				}]
			])],
			['NETWORK', OrderedDict([
				['HOSTNAME', {
					'title': 'Hostname',
					'value': self.get_host_name(),
					'url': "/sys-security"
				}],
				['WIFI', {
					'title': 'Wifi',
					'value': zynconf.get_current_wifi_mode(),
					'url': "/sys-wifi"
				}],
				['IP', {
					'title': 'IP',
					'value': self.get_ip(),
					'url': "/sys-wifi"
				}]
			])]
		])

		if self.genjson:
			self.write(config)
		else:
			self.render("config.html", body="dashboard_block.html", config=config, title="Dashboard", errors=None)


	def get_git_info(self, path):
		branch = check_output("cd %s; git branch | grep '*'" % path, shell=True).decode()[2:-1]
		gitid = check_output("cd %s; git rev-parse HEAD" % path, shell=True).decode()[:-1]
		return { "branch": branch, "gitid": gitid }


	def get_host_name(self):
		with open("/etc/hostname") as f:
			hostname=f.readline()
			return hostname
		return ""


	def get_os_info(self):
		return check_output("lsb_release -ds", shell=True).decode()


	def get_build_info(self):
		info = {}
		try:
			zynthian_dir = os.environ.get('ZYNTHIAN_DIR',"/zynthian")
			with open(zynthian_dir + "/build_info.txt", 'r') as f:
				rows = f.read().split("\n")
				f.close()
				for row in rows:
					try:
						k,v = row.split(": ")
						info[k] = v
						logging.debug("Build info => {}: {}".format(k,v))
					except:
						pass
		except Exception as e:
			logging.warning("Can't get build info! => {}".format(e))
			info['Timestamp'] = '???'

		return info


	def get_ip(self):
		#out=check_output("hostname -I | cut -f1 -d' '", shell=True).decode()
		out=check_output("hostname -I", shell=True).decode()
		return out


	def get_gpio_expander(self):
		try:
			out=check_output("gpio i2cd", shell=True).decode().split("\n")
			if len(out)>3 and out[3].startswith("20: 20"):
				return "MCP23017"
		except:
			pass
		return "No detected"


	def get_ram_info(self):
		out=check_output("free -m | grep 'Mem'", shell=True).decode()
		parts=re.split('\s+', out)
		return { 'total': parts[1]+"M", 'used': parts[2]+"M", 'free': parts[3]+"M", 'usage': "{}%".format(int(100*float(parts[2])/float(parts[1]))) }


	def get_temperature(self):
		try:
			return check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True).decode()[5:-3] + "ºC"
		except:
			return "???"


	def get_sd_info(self):
		try:
			out=check_output("df -h / | grep '/dev/root'", shell=True).decode()
			parts=re.split('\s+', out)
			return { 'total': parts[1], 'used': parts[2], 'free': parts[3], 'usage': parts[4] }
		except:
			return { 'total': 'NA', 'used': 'NA', 'free': 'NA', 'usage': 'NA' }


	def get_num_of_files(self, path, pattern=None):
		if pattern:
			pattern = "-name \"{}\"".format(pattern)
		else:
			pattern = ""
		n=check_output("find {} -type f -follow {} | wc -l".format(path, pattern), shell=True).decode()
		return n


	def get_num_of_presets(self, path):
		# LV2 presets
		n1 = int(check_output("find {}/lv2 -type f -prune -name manifest.ttl | wc -l".format(path), shell=True).decode())
		logging.debug("LV2 presets => {}".format(n1))
		# Pianoteq presets
		n2 = int(check_output("find {}/pianoteq -type f -prune | wc -l".format(path), shell=True).decode())
		logging.debug("Pianoteq presets => {}".format(n2))
		# Puredata presets
		n3 = int(check_output("find {}/puredata/*/* -type d -prune | wc -l".format(path), shell=True).decode())
		logging.debug("Puredata presets => {}".format(n3))
		# ZynAddSubFX presets
		n4 = int(check_output("find {}/zynaddsubfx -type f -name *.xiz | wc -l".format(path), shell=True).decode())
		logging.debug("ZynAddSubFX presets => {}".format(n4))
		return n1 + n2 + n3 + n4


	def is_service_active(self, service):
		cmd="systemctl is-active %s" % service
		try:
			result=check_output(cmd, shell=True).decode('utf-8','ignore')
		except Exception as e:
			result="ERROR: %s" % e
		#print("Is service "+str(service)+" active? => "+str(result))
		if result.strip()=='active': return True
		else: return False

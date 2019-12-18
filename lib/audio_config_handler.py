# -*- coding: utf-8 -*-
#********************************************************************
# ZYNTHIAN PROJECT: Zynthian Web Configurator
#
# Audio Configuration Handler
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
import logging
import tornado.web
from collections import OrderedDict
from subprocess import check_output, call
from lib.zynthian_config_handler import ZynthianConfigHandler

#------------------------------------------------------------------------------
# Audio Configuration
#------------------------------------------------------------------------------

class AudioConfigHandler(ZynthianConfigHandler):

	soundcard_presets=OrderedDict([
		['HifiBerry DAC+ ADC PRO', {
			'SOUNDCARD_CONFIG': 'dtoverlay=hifiberry-dacplusadcpro,slave',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Digital,ADC,ADC Left Input,ADC Right Input'
		}],
		['HifiBerry DAC+ ADC', {
			'SOUNDCARD_CONFIG': 'dtoverlay=hifiberry-dacplusadc',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Digital,Analogue'
		}],
		['HifiBerry DAC+', {
			'SOUNDCARD_CONFIG': 'dtoverlay=hifiberry-dacplus',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Digital'
		}],
		['HifiBerry DAC+ light', {
			'SOUNDCARD_CONFIG':'dtoverlay=hifiberry-dac',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Digital'
		}],
		['HifiBerry DAC+ RTC', {
			'SOUNDCARD_CONFIG':'dtoverlay=hifiberry-dac\ndtoverlay=i2c-rtc,ds130',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Digital'
		}],
		['HifiBerry Digi', {
			'SOUNDCARD_CONFIG':'dtoverlay=hifiberry-digi',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -P -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['HifiBerry Amp', {
			'SOUNDCARD_CONFIG': 'dtoverlay=hifiberry-amp',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:sndrpihifiberry -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['AudioInjector', {
			'SOUNDCARD_CONFIG': 'dtoverlay=audioinjector-wm8731-audio',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:audioinjectorpi -S -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Master,Capture'
		}],
		['AudioInjector Ultra', {
			'SOUNDCARD_CONFIG': 'dtoverlay=audioinjector-ultra',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:audioinjectorul -r 48000 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'DAC,PGA'
		}],
		['IQAudio DAC', {
			'SOUNDCARD_CONFIG': 'dtoverlay=iqaudio-dac',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['IQAudio DAC+', {
			'SOUNDCARD_CONFIG': 'dtoverlay=iqaudio-dacplus',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['IQAudio Digi', {
			'SOUNDCARD_CONFIG': 'dtoverlay=iqaudio-digi-wm8804-audio',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['PiSound', {
			'SOUNDCARD_CONFIG': 'dtoverlay=pisound',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['JustBoom DAC', {
			'SOUNDCARD_CONFIG': 'dtoverlay=justboom-dac',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['JustBoom Digi', {
			'SOUNDCARD_CONFIG': 'dtoverlay=justboom-digi',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['Fe-Pi Audio', {
			'SOUNDCARD_CONFIG': 'dtoverlay=fe-pi-audio',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['Generic USB device', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['Behringer UCA222 (USB)', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -d alsa -d hw:CODEC -r 48000 -p 256 -n 3 -s -S -X raw',
			'SOUNDCARD_MIXER': 'PCM'
		}],
		['Behringer UMC404HD (USB)', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -d alsa -d hw:CARD=U192k -r 48000 -p 256 -n 3 -s -S -X raw',
			'SOUNDCARD_MIXER': 'UMC404HD_192k_Output,Mic'
		}],
		['Steinberg UR22 mkII (USB)', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': 'Clock_Source_41_Validity'
		}],
		['Edirol UA1-EX (USB)', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -d alsa -d hw:UA1EX -r 44100 -p 1024 -n 2 -S -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['RBPi On-Board Analog Audio', {
			'SOUNDCARD_CONFIG': 'dtparam=audio=on\naudio_pwm_mode=2',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:ALSA -r 44100 -p 512 -n 3 -X raw',
			'SOUNDCARD_MIXER': 'PCM'
		}],
		['Dummy device', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}],
		['Custom device', {
			'SOUNDCARD_CONFIG': '',
			'JACKD_OPTIONS': '-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw',
			'SOUNDCARD_MIXER': ''
		}]
	])


	@tornado.web.authenticated
	def get(self, errors=None):

		if os.environ.get('ZYNTHIAN_KIT_VERSION')!='Custom':
			enable_custom_text = " (select Custom kit to enable)"
		else:
			enable_custom_text = ""

		config=OrderedDict([
			['SOUNDCARD_NAME', {
				'type': 'select',
				'title': "Soundcard{}".format(enable_custom_text),
				'value': os.environ.get('SOUNDCARD_NAME'),
				'options': list(self.soundcard_presets.keys()),
				'presets': self.soundcard_presets,
				'disabled': enable_custom_text!=""
			}],
			['SOUNDCARD_CONFIG', {
				'type': 'textarea',
				'title': "Config{}".format(enable_custom_text),
				'cols': 50,
				'rows': 4,
				'value': os.environ.get('SOUNDCARD_CONFIG'),
				'advanced': True,
				'disabled': enable_custom_text!=""
			}],
			['JACKD_OPTIONS', {
				'type': 'text',
				'title': "Jackd Options{}".format(enable_custom_text),
				'value': os.environ.get('JACKD_OPTIONS',"-P 70 -t 2000 -s -d alsa -d hw:0 -r 44100 -p 256 -n 2 -X raw"),
				'advanced': True,
				'disabled': enable_custom_text!=""
			}],
			['ZYNTHIAN_AUBIONOTES_OPTIONS', {
				'type': 'text',
				'title': "Aubionotes Options",
				'value': os.environ.get('ZYNTHIAN_AUBIONOTES_OPTIONS',"-O complex -t 0.5 -s -88  -p yinfft -l 0.5"),
				'advanced': True
			}],
			['ZYNTHIAN_LIMIT_USB_SPEED', {
				'type': 'boolean',
				'title': "Limit USB speed to 12Mb/s",
				'value': os.environ.get('ZYNTHIAN_LIMIT_USB_SPEED','0'),
				'advanced': True
			}],
			['SOUNDCARD_MIXER', {
				'type': 'text',
				'title': "Mixer Controls{}".format(enable_custom_text),
				'value': os.environ.get('SOUNDCARD_MIXER'),
				'advanced': True,
				'disabled': enable_custom_text!=""
			}],
			['AUDIO_MIXER_JS', {
				'type': 'jscript',
				'script_file': "audio_mixer.js"
			}]
		])

		self.get_mixer_controls(config)

		super().get("Audio", config, errors)


	@tornado.web.authenticated
	def post(self):
		self.request.arguments['ZYNTHIAN_LIMIT_USB_SPEED'] = self.request.arguments.get('ZYNTHIAN_LIMIT_USB_SPEED', '0')
		postedConfig = tornado.escape.recursive_unicode(self.request.arguments)
		errors=self.update_config(postedConfig)
		self.reboot_flag = True
		self.get(errors)


	def get_mixer_controls(self, config):
		mixerControl = None
		controlName = ''
		is_capture = False
		is_playback = False

		device_name = self.get_device_name()
		logging.debug("AUDIO DEVICE NAME => {}".format(device_name))

		try:
			scMixer = config['SOUNDCARD_MIXER']['value']
			if scMixer is None:
				scMixer = self.soundcard_presets[os.environ.get('SOUNDCARD_NAME')]['SOUNDCARD_MIXER']
				config['SOUNDCARD_MIXER']['value'] = scMixer
				self.soundcard_mixer = scMixer.split(',')
			elif scMixer.strip()=='':
				self.soundcard_mixer = None
			else:
			 self.soundcard_mixer = scMixer.split(',')
		except:
			self.soundcard_mixer = None

		volumePercent = ''
		idx = 0
		try:
			for byteLine in check_output("amixer -M -c {}".format(device_name), shell=True).splitlines():
				line = byteLine.decode("utf-8")

				if line.find('Simple mixer control')>=0:
					if controlName and (is_capture or is_playback):
						if is_capture:
							self.add_mixer_control(config, mixerControl, controlName, volumePercent, 'Capture')
						else:
							self.add_mixer_control(config, mixerControl, controlName, volumePercent, 'Playback')

					mixerControl = {
						'type': 'slider',
						'id': idx,
						'title': '',
						'value': 0,
						'min': 0,
						'max': 100,
						'step': 1,
						'advanced': False
					}
					controlName = ''
					is_capture = False
					is_playback = False


					volumePercent = ''
					idx += 1
					m = re.match("Simple mixer control '(.*?)'.*", line, re.M | re.I)
					if m:
						controlName = m.group(1).strip()

				elif line.find('Capture channels:')>=0:
						is_capture = True

				elif line.find('Playback channels:')>=0:
						is_playback = True

				else:
					m = re.match(".*(Playback|Capture).*\[(\d*)%\].*", line, re.M | re.I)
					if m:
						volumePercent = m.group(2)
						if m.group(1) == 'Capture':
							is_capture = True
						else:
							is_playback = True
					else:
						m = re.match(".*\[(\d*)%\].*", line, re.M | re.I)
						if m:
							volumePercent = m.group(1)

			if controlName and (is_playback or is_capture):
				if is_playback:
					self.add_mixer_control(config, mixerControl, controlName, volumePercent, 'Playback')
				else:
					self.add_mixer_control(config, mixerControl, controlName, volumePercent, 'Capture')

		except Exception as err:
			logging.error(err)


	def add_mixer_control(self, config, mixerControl, controlName, volumePercent, channelType):
		logging.debug("ADD MIXER CONTROL '{}' => {}".format(mixerControl, controlName))

		realControlName = controlName.replace(' ','_')
		if not self.soundcard_mixer or realControlName in self.soundcard_mixer:
			configKey = 'ALSA_VOLUME_' + channelType + '_' + realControlName
			mixerControl['title'] = channelType + ' ' + controlName
			mixerControl['value'] = volumePercent
			config[configKey] = mixerControl


	def get_device_name(self):
		try:
			jack_opts=os.environ.get('JACKD_OPTIONS')
			res = re.compile(r" hw:([^\s]+) ").search(jack_opts)
			return res.group(1)
		except:
			return "0"


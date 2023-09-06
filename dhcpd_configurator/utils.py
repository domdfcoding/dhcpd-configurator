#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import warnings
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
	# this package
	from dhcpd_configurator.device import Device

__all__ = ["check_for_duplicates", "parse_mac"]


def parse_mac(mac: str) -> str:
	"""
	Parse a MAC address with either colon or hyphen separators.

	:param mac:
	"""

	mac = str(mac)

	if len(mac.split(':')) == 6:
		return mac
	elif len(mac.split('-')) == 6:
		return mac.replace('-', ':')
	else:
		raise ValueError("Unknown MAC Address format")


def check_for_duplicates(devices: List["Device"]) -> List["Device"]:
	"""
	Warn and skip devices with duplicated hostnames or IP & MAC addresses.

	:param devices:
	"""

	validated_devices: List["Device"] = []

	for device in devices:

		for existing_device in validated_devices:
			if device.hostname == existing_device.hostname:
				warnings.warn(f"A device with the hostname `{device.hostname}` is already in the list. Skipping.")
				break
			elif device.mac == existing_device.mac:
				warnings.warn(f"A device with the mac address `{device.mac}` is already in the list. Skipping.")
				break
			elif device.ip == existing_device.ip:
				warnings.warn(f"A device with the ip address `{device.ip}` is already in the list. Skipping.")
				break
		else:
			validated_devices.append(device)

	return validated_devices

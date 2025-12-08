#!/usr/bin/env python3
#
#  device.py
"""
Models a network device.
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
from typing import Any, Dict, Union

# 3rd party
import attr
from enum_tools import IntEnum
from mac_vendor_lookup import MacLookup  # type: ignore[import-untyped]

# this package
from dhcpd_configurator.utils import parse_mac

__all__ = ["Device", "DeviceType"]


class DeviceType(IntEnum):
	"""
	Represents the general category of the device.
	"""

	INFRA = 0
	DESKTOP = 1
	LAPTOP = 2
	ALL_IN_ONE = 3
	PHONE = 4
	PRINTER = 5
	TABLET = 6
	SMART_SPEAKER = 7
	GAMES_CONSOLE = 9
	SMART_HOME = 10
	TELEVISION = 11

	UNKNOWN = 99
	OTHER = -1

	@classmethod
	def from_string(cls, value: str) -> "DeviceType":
		"""
		Lookup an enum value by name.

		:param value:
		"""

		return getattr(cls, value.upper())


def _convert_device_type(value: Union[str, int, DeviceType]) -> DeviceType:
	if isinstance(value, str):
		return DeviceType.from_string(value)
	else:
		return DeviceType(value)


@attr.define
class Device:
	"""
	Represents a device on the network.
	"""

	#: The hostname of the device.
	hostname: str = attr.field(converter=str)

	#: The MAC address of the device.
	mac: str = attr.field(converter=parse_mac)

	#: The final segment of the device IP.
	ip: str = attr.field(converter=str)

	#: The general category of the device.
	type: DeviceType = attr.field(converter=_convert_device_type)

	def to_dict(self) -> Dict[str, Any]:
		"""
		Return a dictionary representation of the :class:`~.Device`.
		"""

		return {
				"hostname": self.hostname,
				"mac": self.mac,
				"ip": self.ip,
				"type": int(self.type),
				}

	@property
	def vendor(self) -> str:
		"""
		The name of the vendor corresponding to the device's MAC address.

		If no vendor found in the database ``"unknown"`` is returned,
		"""

		try:
			return MacLookup().lookup(self.mac)
		except KeyError:
			return "unknown"

#!/usr/bin/env python3
#
#  writers.py
"""
Write configuration files.
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
import socket
from typing import List, Optional

# 3rd party
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from jinja2 import Template

# this package
import dhcpd_configurator.templates
from dhcpd_configurator.device import Device

__all__ = ["write_dhcpd_conf", "write_hosts_file"]

dhcpd_template = Template(importlib_resources.read_text(dhcpd_configurator.templates, "dhcpd.conf.template"))
hosts_template = Template(importlib_resources.read_text(dhcpd_configurator.templates, "hosts.template"))


def _dhcp_entry(device: Device, subnet: str) -> str:
	return f"host	{device.hostname}	{{ hardware ethernet	{device.mac};	fixed-address {subnet}{device.ip};}}"


def write_dhcpd_conf(
		devices: List[Device],
		filename: PathLike = "/etc/dhcp/dhcpd.conf",
		subnet: str = "192.168.0.",
		*,
		ddns_update_style: str = "none",
		default_lease_time: int = 3600,
		max_lease_time: int = 7200,
		authoritative: bool = False,
		router: str = "192.168.0.1",
		subnet_mask: str = "255.255.255.0",
		domain_name_servers: str = "192.168.0.1",
		ip_range: str = "192.168.0.100 192.168.0.255",
		domain_name: Optional[str] = None,
		mqtt_telemetry: bool = True,
		) -> None:
	"""
	Write the generated `/etc/dhcp/dhcpd.conf` file to disk.

	:param devices: The list of devices.
	:param filename: The target filename.
	:param subnet: The subnet (i.e. all but the last part) of the device IPs.
	:param ddns_update_style:
	:param default_lease_time:
	:param max_lease_time:
	:param authoritative:
	:param router:
	:param subnet_mask:
	:param domain_name_servers:
	:param ip_range:
	:param domain_name:
	:param mqtt_telemetry:
	"""

	subnet = subnet.strip('.') + '.'

	rendered = dhcpd_template.render(
			devices=devices,
			subnet=subnet,
			ddns_update_style=ddns_update_style,
			default_lease_time=default_lease_time,
			max_lease_time=max_lease_time,
			authoritative=authoritative,
			router=router,
			subnet_mask=subnet_mask,
			domain_name_servers=domain_name_servers,
			ip_range=ip_range,
			domain_name=domain_name,
			mqtt_telemetry=mqtt_telemetry,
			dhcp_entry=_dhcp_entry,
			)
	PathPlus(filename).write_clean(rendered)


def write_hosts_file(
		devices: List[Device],
		filename: PathLike = "/etc/hosts",
		subnet: str = "192.168.0.",
		) -> None:
	"""
	Write the generated `/etc/hosts` file to disk.

	:param devices: The list of devices.
	:param filename: The target filename.
	:param subnet: The subnet (i.e. all but the last part) of the device IPs.
	"""

	subnet = subnet.strip('.') + '.'

	rendered = hosts_template.render(
			devices=devices,
			subnet=subnet,
			socket=socket,
			)
	PathPlus(filename).write_clean(rendered)

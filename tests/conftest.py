# stdlib
from typing import List

# 3rd party
import pytest

# this package
from dhcpd_configurator.device import Device
from dhcpd_configurator.utils import check_for_duplicates

pytest_plugins = ("coincidence", )


@pytest.fixture(scope="module")
def devices() -> List[Device]:

	devices = []

	def add_device(*args, **kwargs) -> None:
		devices.append(Device(*args, **kwargs))

	add_device("evolis", "00:1A:FD:06:B1:CA", '3', "printer")
	add_device("mx490", "F8:0D:60:DC:76:9A", "12", "printer")
	add_device("mono-printer", "30:05:5C:31:10:D0", "17", "printer")
	add_device("hp-printer", "C4:34:6B:D7:06:EE", "33", "printer")
	add_device("dominic-stream", "C4:8E:8F:8F:30:39", "86", "laptop")
	add_device("argon", "dc:a6:32:ba:59:fc", "87", "laptop")
	add_device("cluster-1", "b8:27:eb:cc:ad:d9", "88", "laptop")
	add_device("cluster-2", "b8:27:eb:31:6c:e5", "89", "laptop")

	return check_for_duplicates(devices)

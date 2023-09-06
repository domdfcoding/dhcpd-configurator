# stdlib
from typing import List

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from dhcpd_configurator.device import Device


def test_mac_vendors(
		devices: List[Device],
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	device_vendor_map = []

	for device in devices:
		device_vendor_map.append((device.to_dict(), device.vendor))

	advanced_data_regression.check(device_vendor_map)

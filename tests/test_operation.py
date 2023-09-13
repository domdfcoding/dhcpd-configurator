# stdlib
import socket
from typing import List

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from dhcpd_configurator.device import Device
from dhcpd_configurator.writers import write_dhcpd_conf, write_hosts_file


@pytest.mark.parametrize("mqtt_telemetry", [True, False])
def test_dhcpd_conf(
		tmp_pathplus: PathPlus,
		devices: List[Device],
		advanced_file_regression: AdvancedFileRegressionFixture,
		mqtt_telemetry: bool
		):

	write_dhcpd_conf(
			devices,
			filename=tmp_pathplus / "dhcpd.conf",
			subnet="192.168.1.",
			domain_name_servers="192.168.1.14",
			authoritative=True,
			ip_range="192.168.1.190 192.168.1.255",
			domain_name="stoke",
			router="192.168.1.1",
			mqtt_telemetry=mqtt_telemetry,
			)

	advanced_file_regression.check_file(tmp_pathplus / "dhcpd.conf")


def test_hosts_file(
		tmp_pathplus: PathPlus,
		devices: List[Device],
		advanced_file_regression: AdvancedFileRegressionFixture,
		monkeypatch,
		):

	monkeypatch.setattr(socket, "gethostname", lambda: "server")

	write_hosts_file(
			devices,
			filename=tmp_pathplus / "hosts.txt",
			subnet="192.168.1.",
			)

	advanced_file_regression.check_file(tmp_pathplus / "hosts.txt")

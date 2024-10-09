# 3rd party
import pytest

# this package
from dhcpd_configurator.utils import parse_mac


@pytest.mark.parametrize("mac", ["01-23-45-67-89-AB", "01:23:45:67:89:AB"])
def test_parse_mac(mac: str):
	assert parse_mac(mac) == "01:23:45:67:89:AB"


def test_parse_mac_unknown():
	with pytest.raises(ValueError, match="Unknown MAC Address format"):
		parse_mac("0123.4567.89AB")

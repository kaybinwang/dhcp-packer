from unittest import TestCase

from dhcp.packets import (
    DhcpDiscover,
    DhcpOffer,
    DhcpOptions,
    HardwareType,
    OperationCode,
)
from dhcp.utils import endian


class PacketsTestCase(TestCase):
    def test_discover_round_trip(self) -> None:
        discover = DhcpDiscover(
            operation_code=OperationCode.CLIENT_REQUEST,
            transaction_id=0x12345678,
            mac_address="AB:CD:EF:12:34:56",
        )
        with self.assertRaises(NotImplementedError):
            packet = discover.pack(endian.BIG)
            unpacked = DhcpDiscover.unpack(packet, endian.BIG)
            self.assertEqual(unpacked, discover)

    def test_offer_round_trip(self) -> None:
        offer = DhcpOffer(
            operation_code=OperationCode.SERVER_RESPONSE,
            hardware_type=HardwareType.ETHERNET,
            hardware_address_len=6,
            hops=0,
            transaction_id=0x12345678,
            seconds=0,
            flags=b"\x04",
            client_ip="192.168.1.50",
            offer_ip="192.168.1.72",
            next_server_ip="192.168.1.5",
            gateway_ip="192.168.1.1",
            client_hardware_address="AB:CD:EF:12:34:56",
            server_name=None,
            boot_filename=None,
            options=DhcpOptions(
                subnet_mask="255.255.0.0",
                router_ip="192.168.1.1",
                dns_servers=["1.1.1.1", "8.8.8.8"],
                domain_name=None,
                lease_time=86400,
                dhcp_message_type=3,
                dhcp_server_ip="192.168.1.5",
            ),
        )
        with self.assertRaises(NotImplementedError):
            packet = offer.pack(endian.BIG)
            unpacked = DhcpOffer.unpack(packet, endian.BIG)
            self.assertEqual(unpacked, offer)

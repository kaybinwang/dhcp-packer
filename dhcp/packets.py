from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence

from dhcp.utils.endian import ByteOrder
from dhcp.utils.stream import DhcpPacketIO


class OperationCode(Enum):
    """Specifies the operation code for a DHCP packet."""

    CLIENT_REQUEST = 1
    SERVER_RESPONSE = 2


class HardwareType(Enum):
    """Specifies the hardware type."""

    ETHERNET = 1


class DhcpOptionCode(Enum):
    """Specifies an option type for a DHCP option."""

    SUBNET_MASK = 1
    ROUTER = 3
    DNS_SERVER = 6
    DOMAIN_NAME = 15
    LEASE_TIME = 51
    DHCP_MESSAGE_TYPE = 53
    DHCP_SERVER = 54
    END = 255


@dataclass(frozen=True)
class DhcpDiscover:
    """A DHCP Discover packet that is initally broadcasted by a client."""

    operation_code: OperationCode
    transaction_id: int
    mac_address: str

    @classmethod
    def unpack(self, packet: bytes, byteorder: ByteOrder) -> DhcpDiscover:
        """Deserialize the bytes into a DhcpDiscover.

        :param packet: are the bytes to deserialize
        :param byteorder: specifies the endianness of the bytes

        :return: an instance of DhcpDiscover
        """
        raise NotImplementedError

    def pack(self, byteorder: ByteOrder) -> bytes:
        """Serialize the packet into bytes.

        :param byteorder: specifies the endianness of the bytes

        :return: the serialized packet as bytes
        """
        packet = b""
        packet += b"\x01"  # Message type: Boot Request (1)
        packet += b"\x01"  # Hardware type: Ethernet
        packet += b"\x06"  # Hardware address length: 6
        packet += b"\x00"  # Hops: 0
        packet += self.transaction_id.to_bytes(4, byteorder)
        packet += b"\x00\x00"  # Seconds elapsed: 0
        packet += b"\x80\x00"  # Bootp flags: 0x8000 (Broadcast) + reserved flags
        packet += b"\x00\x00\x00\x00"  # Client IP address: 0.0.0.0
        packet += b"\x00\x00\x00\x00"  # Your (client) IP address: 0.0.0.0
        packet += b"\x00\x00\x00\x00"  # Next server IP address: 0.0.0.0
        packet += b"\x00\x00\x00\x00"  # Relay agent IP address: 0.0.0.0
        # packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
        packet += self.mac_address
        packet += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # padding
        packet += b"\x00" * 67  # Server host name not given
        packet += b"\x00" * 125  # Boot file name not given
        packet += b"\x63\x82\x53\x63"  # Magic cookie: DHCP
        packet += (
            b"\x35\x01\x01"  # Option: (t=53,l=1) DHCP Message Type = DHCP Discover
        )
        # packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'  #Option: (t=61,l=6) ClientIden
        packet += b"\x3d\x06" + self.mac_address
        packet += b"\x37\x03\x03\x01\x06"  # Option: (t=55,l=3) Parameter Request List
        packet += b"\xff"  # End Option
        return packet


@dataclass(frozen=True)
class DhcpOffer:
    """A DHCP Offer packet that is sent from the server."""

    operation_code: OperationCode
    hardware_type: HardwareType
    hardware_address_len: int
    hops: int
    transaction_id: int
    seconds: int
    flags: bytes
    client_ip: str
    offer_ip: str
    next_server_ip: str
    gateway_ip: str
    client_hardware_address: str
    server_name: Optional[str]
    boot_filename: Optional[str]
    options: DhcpOptions

    @classmethod
    def unpack(cls, packet: bytes, byteorder: ByteOrder) -> DhcpOffer:
        """Deserialize the bytes into a DhcpOffer.

        :param packet: are the bytes to deserialize
        :param byteorder: specifies the endianness of the bytes

        :return: an instance of DhcpOffer
        """
        packet_stream = DhcpPacketIO(packet)
        operation_code = packet_stream.read_enum(OperationCode, 1, byteorder)
        hardware_type = packet_stream.read_enum(HardwareType, 1, byteorder)
        hardware_address_len = packet_stream.read_int(1, byteorder)
        hops = packet_stream.read_int(1, byteorder)
        transaction_id = packet_stream.read_int(4, byteorder)
        seconds = packet_stream.read_int(2, byteorder)
        flags = packet_stream.read(2)  # TODO: parse into Flag
        client_ip = packet_stream.read_ip()
        offer_ip = packet_stream.read_ip()
        next_server_ip = packet_stream.read_ip()
        gateway_ip = packet_stream.read_ip()
        client_hardware_address = packet_stream.read_mac_address(16)
        server_name = packet_stream.read_string(64)
        boot_filename = packet_stream.read_string(128)

        magic_cookie = packet_stream.read(4)
        assert magic_cookie.hex() == "63825363"

        options = DhcpOptions.unpack(packet_stream.read(), byteorder)
        return cls(
            operation_code=operation_code,
            hardware_type=hardware_type,
            hardware_address_len=hardware_address_len,
            hops=hops,
            transaction_id=transaction_id,
            seconds=seconds,
            flags=flags,
            client_ip=client_ip,
            offer_ip=offer_ip,
            next_server_ip=next_server_ip,
            gateway_ip=gateway_ip,
            client_hardware_address=client_hardware_address,
            server_name=server_name,
            boot_filename=boot_filename,
            options=options,
        )

    def pack(self, byteorder: ByteOrder) -> bytes:
        """Serialize the packet into bytes.

        :param byteorder: specifies the endianness of the bytes

        :return: the serialized packet as bytes
        """
        raise NotImplementedError


@dataclass(frozen=True)
class DhcpOptions:
    """An additional set of data that's included in a DHCP packet."""

    subnet_mask: Optional[str]
    router_ip: Optional[str]
    dns_servers: Sequence[str]
    domain_name: Optional[str]
    lease_time: Optional[int]
    dhcp_message_type: Optional[int]
    dhcp_server_ip: Optional[str]

    @classmethod
    def unpack(cls, packet: bytes, byteorder: ByteOrder) -> DhcpOptions:
        """Deserialize the bytes into a DhcpOptions.

        :param packet: are the bytes to deserialize
        :param byteorder: specifies the endianness of the bytes

        :return: an instance of DhcpOptions
        """
        subnet_mask = None
        router_ip = None
        dns_servers: List[str] = []
        domain_name = None
        lease_time = None
        dhcp_message_type = None
        dhcp_server_ip = None

        num_bytes = len(packet)
        packet_stream = DhcpPacketIO(packet)
        while packet_stream.tell() < num_bytes:
            option_code = packet_stream.read_enum(DhcpOptionCode, 1, byteorder)
            option_len = packet_stream.read_int(1, byteorder)

            if option_code is DhcpOptionCode.SUBNET_MASK:
                assert subnet_mask is None
                subnet_mask = packet_stream.read_ip(option_len)
            elif option_code is DhcpOptionCode.ROUTER:
                assert router_ip is None
                router_ip = packet_stream.read_ip(option_len)
            elif option_code is DhcpOptionCode.DNS_SERVER:
                dns_server = packet_stream.read_ip(option_len)
                dns_servers.append(dns_server)
            elif option_code is DhcpOptionCode.DOMAIN_NAME:
                assert domain_name is None
                domain_name = packet_stream.read_string(option_len)
            elif option_code is DhcpOptionCode.LEASE_TIME:
                assert lease_time is None
                lease_time = packet_stream.read_int(option_len, byteorder)
            elif option_code is DhcpOptionCode.DHCP_MESSAGE_TYPE:
                assert dhcp_message_type is None
                dhcp_message_type = packet_stream.read_int(option_len, byteorder)
            elif option_code is DhcpOptionCode.DHCP_SERVER:
                assert dhcp_server_ip is None
                dhcp_server_ip = packet_stream.read_ip(option_len)
            elif option_code is DhcpOptionCode.END:
                break
            else:
                raise ValueError(option_code)

        return cls(
            router_ip=router_ip,
            subnet_mask=subnet_mask,
            dns_servers=tuple(dns_servers),
            domain_name=domain_name,
            lease_time=lease_time,
            dhcp_message_type=dhcp_message_type,
            dhcp_server_ip=dhcp_server_ip,
        )

    def pack(self, byteorder: ByteOrder) -> bytes:
        """Serialize the packet into bytes.

        :param byteorder: specifies the endianness of the bytes

        :return: the serialized packet as bytes
        """
        raise NotImplementedError

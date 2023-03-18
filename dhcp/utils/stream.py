from enum import Enum
from io import BytesIO
from typing import List, Type, TypeVar

from dhcp.utils.endian import ByteOrder

E = TypeVar("E", bound=Enum)


class DhcpPacketIO(BytesIO):
    """A wrapper around io.BytesIO that streams bytes from DHCP packets.

    This is useful for reading bytes from the stream and converting them into Python
    objects.
    """

    def read_int(self, num_bytes: int, byteorder: ByteOrder) -> int:
        """Read an integer from the IO stream.

        :param num_bytes: is the number of bytes to read for the integer
        :param byteorder: specifies the endianness of the bytes

        :return: the requested bytes as an integer
        """
        return int.from_bytes(self.read(num_bytes), byteorder)

    def read_enum(self, enum_cls: Type[E], num_bytes: int, byteorder) -> E:
        """Read an integer from the IO stream and convert it into an enum.

        :param num_bytes: is the number of bytes to read for the enum's integer value
        :param byteorder: specifies the endianness of the bytes

        :return: the requested bytes as an instance of `enum_cls`
        """
        return enum_cls(int.from_bytes(self.read(num_bytes), byteorder))

    def read_ip(self, num_bytes: int = 4) -> str:
        """Read an IP address from the IO stream.

        The IP address is returned in an `X.X.X.X` format.

        :param num_bytes: is the number of bytes to read for the IP address

        :return: the requested bytes as an IP address
        """
        return ".".join(self._read_chars(num_bytes))

    def read_mac_address(self, num_bytes) -> str:
        """Read a MAC address from the IO stream.

        The MAC address is returned in an `X:X:X:X` format where each `X` is a hex
        string.

        :param num_bytes: is the number of bytes to read for the MAC address

        :return: the requested bytes as a MAC address
        """
        return self.read(num_bytes).hex(":")

    def read_string(self, num_bytes) -> str:
        """Read a string address from the IO stream.

        :param num_bytes: is the number of bytes to read for the string

        :return: the requested bytes as a string
        """
        return "".join(self._read_chars(num_bytes))

    def _read_chars(self, num_bytes: int) -> List[str]:
        return [str(b) for b in self.read(num_bytes)]

# dhcp-packer
![Build](https://github.com/kaybinwang/dhcp-packer/actions/workflows/build.yaml/badge.svg)

A Python library for serializing and deserializing DHCP packets into Python
objects.

Note that this library was created for testing purposes. It is not meant to be
used in production environments or any environment that demands performance
and/or stability.

I created this library because I manage my own DHCP server at home and needed a
way to run automated tests against the server in local, staging, and production
environments.

Special thanks to `hassane` who provided the
[script](https://code.activestate.com/recipes/577649-dhcp-query/) that this
library is based off of. I spent a lot of time looking into how to simulate a
DHCP client/server interaction. Without his work, I probably would've given up
much earlier on trying to write E2E tests for my DHCP servers.

## Installation
Requires Python 3.7+

TODO: need to upload to pip

## Usage
`dhcp-packer` contains Python objects for each DHCP packet type. These objects
are designed to be schematized and immutable.

```python
from dhcp.packets import DhcpDiscover, OperationCode

# create the dhcp discover packet
discover = DhcpDiscover(
    operation_code=OperationCode.CLIENT_REQUEST,
    transaction_id=0x12345678,
    mac_address="AB:CD:EF:12:34:56",
    # ...
)

operation_code: OperationCode = discover.operation_code  # all fields are typed
discover.operation_code = OperationCode.SERVER_RESPONSE  # raises Exception!
```

You can use these data models to hold the packet data before serializing them to
the wire format. Similarly, you can deserialize the binary format into the
Python object.

```python
from dhcp.packets import DhcpDiscover
from dhcp.utils import endian

# serialize the discover packet into bytes
packet = discover.pack(endian.BIG)
# deserialize the packet
discover = DhcpDiscover.unpack(packet, endian.BIG)
```

### Example
Here's an example of how you might use the library to broadcast a DHCP discover
packet over the network while listening for a DHCP offer packet.

```python
from dhcp.packets import DhcpDiscover, OperationCode
from dhcp.utils import endian
import socket

# open a socket on port 68 and listen to broadcasts
dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
try:
    # send & receive on port 68
    dhcps.bind(("", 68))

    # serialize the discover packet and broadcast on port 67
    discover = DhcpDiscover(
        operation_code=OperationCode.CLIENT_REQUEST,
        transaction_id=transaction_id,
        mac_address=mac_address,
        # ...
    )
    dhcps.sendto(discover.pack(endian.BIG), ("<broadcast>", 67))

    # wait on receiving an offer packet
    dhcps.settimeout(timeout)
    while True:
        data = dhcps.recv(1024)
        offer = DhcpOffer.unpack(data, endian.BIG)
        if offer.transaction_id == discover.transaction_id:
            return offer
finally:
    dhcps.close()
```

## Development
First create a virtual environment if you don't already have one.
```bash
$ python -m venv dhcp-packer
$ pip install -r requirements.txt
```

Next, you can install the `dhcp-packer` into your virtualenv by running this
command.
```bash
$ make install
```

Now you should be able to run tests.
```bash
$ make test
```

import asyncio
from bleak import BleakClient, BleakScanner
import logging

WRITE_UUID = "49535343-8841-43f4-a8d4-ecbe34729bb3"
LOGGER = logging.getLogger(__name__)

async def discover():
    devices = await BleakScanner.discover()
    LOGGER.debug("Discovered devices: %s", [{"address": device.address, "name": device.name} for device in devices])
    return [device for device in devices if device.name.startswith("Hello")]

class FairyDev:
    def __init__(self, mac: str) -> None:
        self._mac = mac
        self._device = BleakClient(self._mac)
        self._is_on = None
        self._connected = None
        self._brightness = None

    async def _send(self, data: bytearray):
        LOGGER.debug(''.join(format(x, ' 03x') for x in data))      
        if (not self._connected):
            await self.connect()
        await self._device.write_gatt_char(WRITE_UUID, data, response=False)

    @property
    def mac(self):
        return self._mac

    @property
    def is_on(self):
        return self._is_on

    async def turn_on(self):
        command = bytes.fromhex("aa0200aa")
        await self._send(command)
        self._is_on = True

    async def turn_off(self):
        command = bytes.fromhex("aa020100ad")
        await self._send(command)
        self._is_on = False

    async def connect(self):
        await self._device.connect(timeout=20)
        await asyncio.sleep(1)
        self._connected = True

    async def disconnect(self):
        if self._device.is_connected:
            await self._device.disconnect()
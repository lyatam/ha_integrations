from __future__ import annotations
import logging
from .hello_fairy import FairyDev
import voluptuous as vol
from pprint import pformat
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (PLATFORM_SCHEMA, LightEntity)
from homeassistant.const import CONF_NAME, CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("hello_fairy")


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:

    _LOGGER.info(pformat(config))
    
    light = {
        "name": config[CONF_NAME],
        "mac": config[CONF_MAC]
    }
    
    add_entities([HelloFairyLight(light)])

class HelloFairyLight(LightEntity):

    def __init__(self, light) -> None:
        _LOGGER.info(pformat(light))
        self._light = FairyDev(light["mac"])
        self._name = light["name"]
        self._state = None
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool | None:
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._light.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._light.turn_off()

    def update(self) -> None:
        self._state = self._light.is_on
    
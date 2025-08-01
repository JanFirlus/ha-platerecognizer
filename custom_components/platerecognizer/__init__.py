import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .api import get_plate_info

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async def handle_scan(call: ServiceCall):
        data = await get_plate_info(
            hass,
            entry.data["camera_entity"],
            entry.data["token"],
            entry.data["camera_id"]
        )

        if data:
            hass.states.async_set(f"{DOMAIN}.last_plate", data["plate"], {
                "region": data["region"],
                "e_vehicle": data["e_vehicle"],
                "camera": entry.data["camera_id"]
            })
        else:
            hass.states.async_set(f"{DOMAIN}.last_plate", "unbekannt")

    hass.services.async_register(DOMAIN, "scan", handle_scan)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
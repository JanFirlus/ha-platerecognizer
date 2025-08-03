from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .api import send_image_to_api
import os

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async def handle_scan(call: ServiceCall):
        image_path = hass.config.path("www/platecheck.jpg")

        if not os.path.exists(image_path):
            hass.states.async_set(f"{DOMAIN}.last_plate", "kein Bild vorhanden")
            return

        data = await send_image_to_api(
            hass=hass,
            image_path=image_path,
            token=entry.data["token"],
            camera_id=entry.data["camera_id"]
        )

        if data:
            hass.states.async_set(f"{DOMAIN}.last_plate", data["plate"], {
                "region": data["region"],
                "e_vehicle": data["e_vehicle"],
                "camera": entry.data["camera_id"]
            })
        else:
            hass.states.async_set(f"{DOMAIN}.last_plate", "unbekannt")

    await hass.config_entries.async_forward_entry_setup(entry, "sensor")


    # Dienst registrieren
    hass.services.async_register(DOMAIN, "scan", handle_scan)

    return True

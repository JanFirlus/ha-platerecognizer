from homeassistant.helpers.entity import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([PlateRecognizerSensor(hass)], True)

class PlateRecognizerSensor(SensorEntity):
    def __init__(self, hass):
        self._attr_name = "Plate Recognizer Last Plate"
        self._attr_unique_id = f"{DOMAIN}_last_plate"
        self._aattr_native_value = "unbekannt"
        self.hass = hass

    async def async_update(self):
        entity = self.hass.states.get(f"{DOMAIN}.last_plate")
        if entity and entity.state not in (None, "", "unknown"):
            self._attr_native_value = entity.state
        else:
            self._attr_native_value = "unbekannt"
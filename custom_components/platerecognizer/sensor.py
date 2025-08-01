from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([PlateRecognizerSensor(hass)], True)

class PlateRecognizerSensor(Entity):
    def __init__(self, hass):
        self._attr_name = "Plate Recognizer Last Plate"
        self._attr_unique_id = f"{DOMAIN}_last_plate"
        self._state = None
        self.hass = hass

    async def async_update(self):
        # Optional: Hier könntest du selbst abrufen oder Zustand übernehmen
        self._state = self.hass.states.get(f"{DOMAIN}.last_plate").state if self.hass.states.get(f"{DOMAIN}.last_plate") else None

    @property
    def state(self):
        return self._state

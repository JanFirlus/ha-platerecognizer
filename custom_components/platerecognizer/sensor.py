from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    # Wird durch Dienst aufgerufen und setzt Entity direkt über `hass.states.async_set`
    return True

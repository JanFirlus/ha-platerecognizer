import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_component
from homeassistant.helpers.selector import selector
from .const import DOMAIN, CONF_TOKEN, CONF_CAMERA_ID, CONF_CAMERA_ENTITY

class PlateRecognizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_CAMERA_ID], data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_TOKEN): str,
            vol.Required(CONF_CAMERA_ID): str,
            vol.Required(CONF_CAMERA_ENTITY): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

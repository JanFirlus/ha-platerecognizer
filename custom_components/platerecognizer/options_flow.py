from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_TOKEN, CONF_RTSP_URL, CONF_CAMERA_ID

class PlateRecognizerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_TOKEN, default=self.config_entry.options.get(CONF_TOKEN, "")): str,
                vol.Required(CONF_RTSP_URL, default=self.config_entry.options.get(CONF_RTSP_URL, "")): str,
                vol.Required(CONF_CAMERA_ID, default=self.config_entry.options.get(CONF_CAMERA_ID, "")): str,
            })
        )

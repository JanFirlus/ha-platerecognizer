import os
import aiohttp
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def get_plate_info(hass: HomeAssistant, camera_entity_id: str, token: str, camera_id: str):
    image_path = f"/tmp/snapshot_{camera_id}.jpg"

    await hass.services.async_call(
        "camera",
        "snapshot",
        {
            "entity_id": camera_entity_id,
            "filename": image_path
        },
        blocking=True
    )

    if not os.path.exists(image_path):
        _LOGGER.error("Snapshot not created")
        return None

    url = "https://api.platerecognizer.com/v1/plate-reader/"

    async with aiohttp.ClientSession() as session:
        with open(image_path, "rb") as img:
            response = await session.post(url, data={"camera_id": camera_id}, headers={"Authorization": f"Token {token}"}, files={"upload": img})

        if response.status != 200:
            _LOGGER.error("Error from Plate Recognizer API: %s", response.status)
            return None

        result = await response.json()
        if not result["results"]:
            return None

        plate_data = result["results"][0]
        return {
            "plate": plate_data["plate"],
            "region": plate_data.get("region", {}).get("code", ""),
            "e_vehicle": "ja" if plate_data.get("vehicle", {}).get("type", "") == "electric" else "nein"
        }
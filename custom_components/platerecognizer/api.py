import aiohttp
import os

async def send_image_to_api(hass, image_path, token, camera_id):
    if not os.path.exists(image_path):
        return None

    url = "https://api.platerecognizer.com/v1/plate-reader/"

    async with aiohttp.ClientSession() as session:
        with open(image_path, 'rb') as image_file:
            form = aiohttp.FormData()
            form.add_field("upload", image_file, filename="plate.jpg", content_type="image/jpeg")
            form.add_field("camera_id", camera_id)

            headers = {"Authorization": f"Token {token}"}

            async with session.post(url, headers=headers, data=form) as resp:
                if resp.status != 200:
                    return None
                result = await resp.json()

    plate = result.get("results", [{}])[0].get("plate", "")
    region = result.get("results", [{}])[0].get("region", {}).get("code", "")

    if not plate:
        hass.states.async_set("platerecognizer.last_plate", "Keine Erkennung")
        return None

    hass.states.async_set("platerecognizer.last_plate", plate)

    return {
        "plate": plate,
        "region": region,
        "e_vehicle": "ja" if plate.endswith("e") else "nein"
    }


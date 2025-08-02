import aiohttp
import os

async def send_image_to_api(hass, image_path, token, camera_id):
    if not os.path.exists(image_path):
        hass.states.async_set("platerecognizer.last_plate", "Bild nicht gefunden")
        return None

    url = "https://api.platerecognizer.com/v1/plate-reader/"
    form = aiohttp.FormData()

    # Asynchron Datei öffnen
    def open_file():
        return open(image_path, 'rb')

    image_file = await hass.async_add_executor_job(open_file)
    form.add_field("upload", image_file, filename="plate.jpg", content_type="image/jpeg")
    form.add_field("camera_id", camera_id)

    headers = {"Authorization": f"Token {token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=form) as resp:
            if resp.status != 200:
                image_file.close()
                hass.states.async_set("platerecognizer.last_plate", f"Fehler {resp.status}")
                return None

            result = await resp.json()

    image_file.close()

    plates = result.get("results", [])
    if not plates:
        hass.states.async_set("platerecognizer.last_plate", "Keine Erkennung")
        return None

    plate = plates[0].get("plate", "")
    region = plates[0].get("region", {}).get("code", "")
    is_ev = "ja" if plate.lower().endswith("e") else "nein"

    hass.states.async_set("platerecognizer.last_plate", plate)

    return {
        "plate": plate,
        "region": region,
        "e_vehicle": is_ev
    }

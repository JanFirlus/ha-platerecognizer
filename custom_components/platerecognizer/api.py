import subprocess
import requests

async def get_plate_info(rtsp_url, token, camera_id):
    image_path = "/tmp/snapshot.jpg"
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", rtsp_url,
        "-frames:v", "1", image_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError:
        return None

    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://api.platerecognizer.com/v1/plate-reader/",
            headers={"Authorization": f"Token {token}"},
            files={"upload": image_file},
            data={"camera_id": camera_id}
        )

    if response.status_code != 200:
        return None

    data = response.json()
    if not data.get("results"):
        return None

    result = data["results"][0]
    plate = result.get("plate", "")
    region = result.get("region", {}).get("code", "")
    e_vehicle = "ja" if plate.endswith("e") else "nein"
    return {"plate": plate, "region": region, "e_vehicle": e_vehicle}

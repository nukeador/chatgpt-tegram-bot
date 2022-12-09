import os
import requests

def text_to_image(engine_id, api_host, api_key, text):
    url = f"{api_host}/v1alpha/generation/{engine_id}/text-to-image"

    if api_key is None:
        raise Exception("Missing Stability API key.")

    payload = {
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": 1,
        "seed": 0,
        "steps": 30,
        "text_prompts": [
            {
                "text": text,
                "weight": 1
            }
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "image/png",
        "Authorization": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Return the bytes from response.content
    return response.content

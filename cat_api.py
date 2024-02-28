import os
import requests
from dotenv import load_dotenv

load_dotenv()

CAT_FACT_API_URL = os.getenv('CAT_FACT_API_URL')
CAT_IMAGE_API_URL = os.getenv('CAT_IMAGE_API_URL')
API_KEY = os.getenv('CAT_API_KEY')

def get_cat_fact():
    try:
        response = requests.get(CAT_FACT_API_URL)
        data = response.json()
        cat_fact = data["fact"]
        return cat_fact
    except Exception as e:
        print("Error fetching cat fact:", e)
        return "Sorry, I couldn't fetch a cat fact at the moment."


def get_cat_image():
    try:
        headers = {'x-api-key': API_KEY}
        response = requests.get(CAT_IMAGE_API_URL, headers=headers)
        data = response.json()

        if not data or len(data) == 0:
            print("No data found in the API response.")
            return None, None, None

        cat_info = data[0].get('breeds', [])
        if cat_info:
            cat_name = cat_info[0].get('name')
            cat_description = cat_info[0].get('description')
        else:
            cat_name = None
            cat_description = None

        cat_image_url = data[0].get("url", None)

        return cat_image_url, cat_name, cat_description
    except Exception as e:
        print("Error fetching cat image:", e)
        return None, None, None


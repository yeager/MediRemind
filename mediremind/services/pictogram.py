"""ARASAAC pictogram API client with caching."""

import os
import json
import urllib.request
from mediremind.utils.paths import get_cache_dir, get_app_data_dir

ARASAAC_API = "https://api.arasaac.org/v1"

FALLBACK_ICONS = {
    "pill": "pill.svg",
    "injection": "injection.svg",
    "drops": "drops.svg",
    "inhaler": "inhaler.svg",
    "ointment": "ointment.svg",
}


class PictogramService:
    def __init__(self):
        self.cache_dir = os.path.join(get_cache_dir(), "pictograms")
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_pictogram_path(self, medication):
        if medication.custom_image_path and os.path.exists(medication.custom_image_path):
            return medication.custom_image_path
        if medication.pictogram_id:
            cached = os.path.join(self.cache_dir, f"{medication.pictogram_id}.png")
            if os.path.exists(cached):
                return cached
            try:
                return self._download_pictogram(medication.pictogram_id)
            except Exception:
                pass
        return self._get_fallback(medication.form)

    def search_pictograms(self, keyword, language="sv"):
        url = f"{ARASAAC_API}/pictograms/{language}/search/{keyword}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                return [{"id": p["_id"], "keyword": keyword} for p in data[:10]]
        except Exception:
            return []

    def _download_pictogram(self, picto_id):
        url = f"{ARASAAC_API}/pictograms/{picto_id}?download=true"
        cached = os.path.join(self.cache_dir, f"{picto_id}.png")
        urllib.request.urlretrieve(url, cached)
        return cached

    def _get_fallback(self, form):
        filename = FALLBACK_ICONS.get(form, "pill.svg")
        path = os.path.join(get_app_data_dir(), "icons", "fallback", filename)
        if os.path.exists(path):
            return path
        return None

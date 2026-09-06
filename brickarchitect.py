#!/bin/env python3

import requests
from pathlib import Path
from PIL import Image
from base64 import b64encode
from io import BytesIO

class BrickArchitect:
    def __init__(self, url: str, cache: Path):
        self.base_url = url
        if not cache.is_dir():
            raise NotADirectoryError("The cache directory isn't a directory")
        self.cache = cache

    def get_image(self, part: str) -> Image:
        cached_name = self.cache / f"{part}.png"
        if not cached_name.exists():            
            res = requests.get(self.base_url + f"/content/parts-large/{part}.png")
            if res.status_code != 200 and 'pb' in part:
                base_part = part.split('pb')[0]
                res = requests.get(self.base_url + f"/content/parts-large/{base_part}.png")
                
            res.raise_for_status()
            cached_name.write_bytes(res.content)

        return Image.open(cached_name)


    def get_image_data(self, part: str) -> str:
        try:
            img: Image = self.get_image(part)
        except Exception as e:
            print(f"Can't get image for {part}.  Returning None")
            return None
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        b64data = b64encode(buffer.getvalue()).decode('utf-8')
        return "data:image/png;base64," + b64data
#!/bin/env python3
# routines for interfacing with bricklink

from typing import Any
import pickle
import requests
import sys

from pathlib import Path
from pydantic import BaseModel, Field
import csv
from base64 import b64encode
from io import BytesIO
from PIL import Image


class Category(BaseModel):
    id: int = Field(alias="Category ID")
    name: str = Field(alias="Category Name")


class Code(BaseModel):
    item: str = Field(alias="Item No")
    color: str = Field(alias="Color")
    code: str = Field(alias="Code")


class Color(BaseModel):
    id: int = Field(alias="Color ID")
    name: str = Field(alias="Color Name")
    rgb: str = Field(None, alias="RGB")
    type: str = Field(alias="Type")
    parts: int = Field(0, alias="Parts")
    sets: int = Field(0, alias="In Sets")
    wanted: int = Field(0, alias="Wanted")
    for_sale: int  = Field(0, alias="For Sale")
    year_from: int = Field(0, alias="Year From")
    year_to: int = Field(0, alias="Year To")


class CatalogItem(BaseModel):
    type_id: str = Field('')
    category_id: int = Field(alias="Category ID")
    category_name: str = Field(alias="Category Name")
    number: str = Field(alias="Number")
    name: str = Field(alias="Name")
    alternate: str | None=Field(None, alias="Alternate Item Number")


class ItemType(BaseModel):
    id: str = Field(alias="Item Type ID")
    name: str = Field(alias="Item Type Name")


CATALOG_PARAMS = {
    'category': {'file': ('categories.txt',), 'class': Category},
    'code': {'file': ('codes.txt',), 'class': Code},
    'color': {'file': ('colors.txt',), 'class': Color},
    'catalog': {'file': ('Instructions.txt', 'Minifigures.txt', 'Parts.txt'),
                'class': CatalogItem},
    }


class BrickLink:
    def __init__(self):
        self.cache_dir = Path(sys.path[0], 'cache')
        self.cache: dict[str, Any] = {}
        self.image_base_url = "https://img.bricklink.com"
        self.catalog_url = "https://bricklink.com/catalogDownload.asp?a=a"
        for k in CATALOG_PARAMS.keys():
            self._fetch_catalog(k)


    def _fetch_catalog(self, type: str):
        data = []
        for file in CATALOG_PARAMS[type]['file']:
            print(type, file)
            with open(Path(sys.path[0], 'raw_data', file)) as f:                
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    row = {k: v for k, v in row.items() if v != '' and k is not None}
                    #print(row)
                    if file[0] in ('S', 'I', 'M', 'P'):
                        row['type_id'] = file[0]
                    data.append(CATALOG_PARAMS[type]['class'](**row))
            self.cache[type] = data


    def get_image(self, item: CatalogItem, color_id: int) -> Image:
        cached_name = self.cache_dir / f"bl-{item.number}-{color_id}.png"
        if not cached_name.exists():            
            res = requests.get(self.image_base_url + f"/ItemImage/{item.type_id}N/{color_id}/{item.number}.png",
                               headers={'Referrer': 'https://bricklink.com/',
                                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
            res.raise_for_status()
            cached_name.write_bytes(res.content)

        return Image.open(cached_name)


    def get_image_data(self, item: CatalogItem, color_id: int) -> str:
        try:
            img: Image = self.get_image(item, color_id)
        except Exception as e:
            print(f"Can't get image for {item.number}.  Returning None ({e})")
            return None
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        b64data = b64encode(buffer.getvalue()).decode('utf-8')
        return "data:image/png;base64," + b64data

    def color_by_name(self, name: str) -> Color:
        for r in self.cache['color']:
            if r.name == name:
                return r
        return None


    def color_by_id(self, id: int) -> Color:
        for r in self.cache['color']:
            if r.id == id:
                return r
        return None


    def category_by_name(self, name: str) -> Category:  
        for r in self.cache['category']:
            if r.name == name:
                return r
        return None        


    def category_by_id(self, id: int) -> Category:
        for r in self.cache['category']:
            if r.id == id:
                return r
        return None


    def catalog_by_number(self, number: str) -> CatalogItem:
        for r in self.cache['catalog']:
            if r.number == number:
                return r
        return None


#!/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field

class BSItem(BaseModel):
    id: str = Field(alias='ItemID')
    type_id: str = Field(alias='ItemTypeID')
    color: int = Field(alias='ColorID')
    name: str = Field(alias='ItemName')
    type_name: str = Field(alias='ItemTypeName')
    color_name: str = Field(alias='ColorName')
    category_id: int = Field(alias='CategoryID')
    category_name: str = Field(alias='CategoryName')
    status: str = Field(alias='Status')
    qty: int = Field(alias='Qty')
    price: float = Field(alias='Price')
    condition: str = Field(alias='Condition')
    date_added: str | None = Field(None, alias='DateAdded')


class BrickStore:
    def __init__(self, file: Path):
        tree = ET.parse(file)
        self.root = tree.getroot()
        self.items: list[BSItem] = []
        for i in self.root.findall('Inventory/Item'):
            itm = {}
            for c in i:
                itm.update({c.tag: c.findtext('.')})
            self.items.append(BSItem(**itm))
            #print(self.cache[-1])





#!/bin/env python3

from base64 import b64encode
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
import sys
import time
import re


class BrickSet:
    def __init__(self, cache: Path):
        self.cache = cache
        
    def get_image(self, setnum: str) -> Image.Image:
        cname = self.cache / f"{setnum}.jpg"
        if not cname.exists():
            # get the image
            while True:
                res = requests.get(f"https://images.brickset.com/sets/images/{cname.name}")
                if res.status_code != 429:
                    break
                time.sleep(1)
            res.raise_for_status()
            with open(cname, "wb") as f:
                f.write(res.content)
        return Image.open(cname)

    def get_set_data(self, setnum: str) -> str:
        cname = self.cache / f"{setnum}.html"
        if not cname.exists():
            # the the html page
            while True:
                res = requests.get(f"https://brickset.com/sets/{setnum}")
                if res.status_code != 429:
                    break
                time.sleep(1)
            res.raise_for_status()
            with open(cname, "wb") as f:
                f.write(res.content)
        text = cname.read_text()
        #print(cname)
        data = {}
        name_map = {'Number': 'Id',
                    'Name': 'Name',
                    'Theme': 'Theme',
                    'Subtheme': 'Subtheme',
                    'Year released': 'Year',
                    'Pieces': 'Parts',
                    'Minifigs': 'Minifigs',
                    'RRP': "Retail",
                    "Designer": 'Designer'}
        if m := re.search(r"featurebox.+?Details.+?<dl>(.+?)</dl>", text, re.DOTALL):
            for m2 in re.findall(r"<dt>(.+?)</dt>.*?<dd>(.+?)</dd>", m.group(1), re.DOTALL):
                if m2[0] in name_map:
                    data[name_map[m2[0]]] = re.sub('<.+?>', '', m2[1])

        return data
    



def main():
    cache_dir = Path(sys.path[0], 'cache', 'brickset')
    cache_dir.mkdir(parents=True, exist_ok=True) 
    bs = BrickSet(cache_dir)

    html = "<html><head>"
    html += """<style>
body {
    font-family: Arial, sans-serif;
}
    
.container {
    display: flex;
    flex-wrap: wrap;
}
    
.box {
    width: 5in;
    height: 3in;
    border: 1pt solid black;
    display: flex;
    padding: 2px;
    gap: 2px;
}

.set_description {
    white-space: wrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 3in;
    height: 2.95in;    
}

.set_image {
    width: 2in;
    height: 2in;
    object-fit: contain;
}


</style>

"""
    html += '</head><body><div class="container">'


    for a in sorted(set(('6175-1', '6605-1',
                '6621-1', '6641-1','6657-1','6688-1',
                '6697-1','6804-1','6805-1','6820-1',
                '6821-1','6823-1','6846-1','6849-1',
                '6861-1','6870-1','6875-1','6883-1',
                '6891-1','6901-1','6925-1','6926-1',
                '6929-1','6950-1','6972-1','6990-1',
                '8847-1','6086-1','6833-1',


'645-1','897-1','1480-1','1560-1',
'1596-1','1752-1','4005-1','4536-1',
#'6001-1',
'6008-1','6010-1','6020-1',
'6022-1','6027-1','6034-1','6036-1',
'6037-1','6038-1','6040-1','6044-1',
'6047-1','6059-1','6062-1','6075-1',
'6078-1','6082-1','6260-1','6270-1',
'6357-1','6385-1','6501-1','6594-1',
'6605-1','6621-1','6641-1','6657-1',
'6688-1','6697-1',

'005-2','10225-1','10266-1','10283-1',
'10327-1','10360-1','10497-1','1327-1',
'1560-1','1687-1','21309-1','21312-1',
'21313-1','21321-1','21329-1','21348-1',
'21358-1','2963-1','30343-1','30350-1',
'31066-1','31378-1','3804-1','3841-1',
'40018-1','40032-1','40236-1','40252-1',
'40335-1','40682-1','40706-1','40712-1',
'40758-1','40767-1','40775-1','40786-1',
'40890-1','40921-1','4094-1','41046-1',
'41307-1','41307-1','41373-1','41393-1',
'42006-1','42028-1','42032-1','42035-1',
'42036-1','42043-1','42054-1','42059-1',
'42061-1','42062-1','42073-1','42115-1',
'42158-1','42179-1','42182-1','4536-1',
'4537-1','4539-1','4551-1','4554-1',
'45544-1','45544-1','4561-1','45800-1',
'45801-1','45802-1','45806-1','4603-1',
'4610-1','5008897-1','5009806-1','60052-1',
'6010-1','60197-1','60198-1','60267-1',
'60333-1','60404-1','6044-1','6602-2',
'6631-1','6776-1','6803-1','6824-1',
'6901-1','6927-1','6950-1','6970-1',
'7110-1','7199-1','7412-1','7468-1',
'7469-1','7470-1','7471-1','7499-1',
'75105-1','75137-1','75138-1','75161-1',
'75172-1','75187-1','75194-1','75265-1',
'75290-1','75298-1','75810-1','7683-1',
'76908-1','79100-1','7931-1','7956-1',
'8014-1','8024-1','8055-1','8055-1',
'8087-1','8089-1','8412-1','8480-1',
'8510-1','8527-1','8547-1','860-1',
'8640-1','8660-1','8810-1','8847-1',
'8851-1','8855-1','8858-1','9641-1',
'9657-1','9664-1','9695-1','9696-1',
'9697-1','9698-1','9699-1','9764-1',
'9797-1',#'cty1098',
'10280-1','30668-1',
'7195-1','40515-1','31088-1','60160-1',
'60115-1','41128-1','920-2',

                )), key=lambda x: int(x.split('-')[0])):
        print(a)
        try:
            img = bs.get_image(a)
            p = bs.get_set_data(a)
        except Exception as e:
            print(f"Cannot retrieve data for {a}: {e}")
            continue

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        b64data = b64encode(buffer.getvalue()).decode('utf-8')
        idata = "data:image/png;base64," + b64data


        #print(p)
        html += '<div class="box">'
        html += f'<div><img class="set_image" src="{idata}"/></div>'        
        html += f'<div class="set_description">{p['Id']}: <b>{p['Name']}</b><br/>'
        html += f'<hr style="margin-top: 1px; margin-bottom: 1px;" />'
        html += f'{p["Theme"]}/{p.get("Subtheme")}, '
        html += f'{p.get("Year", "?")}<br/>'
        html += f'Parts: {p.get("Parts", "?")}, Minifigs: {p.get("Minifigs", "?")}<br/>'
        html += f'Price: {p.get("Retail")}, Designer: {p.get("Designer", "?")}<br/>'
        html += f'</div>'
        html += '</div>'

    html += "</div></body></html>"
    Path("/tmp/test.html").write_text(html)




if __name__ == "__main__":
    main()

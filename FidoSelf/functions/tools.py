from FidoSelf import client
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import random
import re
import json

async def async_searcher(url, post=False, head=False, headers=None, evaluate=None, object=False, re_json=False, re_content=False, *args, **kwargs,):
    async with ClientSession(headers=headers) as Cclient:
        method = Cclient.head if head else (Cclient.post if post else Cclient.get)
        data = await method(url, *args, **kwargs)
        if evaluate:
            return await evaluate(data)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if head or object:
            return data
        return await data.text()

async def get_google_images(query):
    search = await async_searcher("https://google.com/search", params={"q": query, "tbm": "isch"}, headers={"User-Agent": random.choice(Cclient.functions.HEADERS)})
    soup = BeautifulSoup(search, "lxml")
    google_images = []
    all_script_tags = soup.select("script")
    images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    images_data_fix = json.dumps(images_data)
    images_data_json = json.loads(images_data_fix)
    google_image_data = re.findall(r"\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}", images_data_json)
    google_images_thumbnails = ", ".join(re.findall(r"\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]",str(google_image_data))).split(", ")
    thumbnails = [bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in google_images_thumbnails]
    removed_google_images_thumbnails = re.sub(r"\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]", "", str(google_image_data))
    google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_google_images_thumbnails,)
    full_res_images = [bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in google_full_resolution_images]
    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select(".isv-r.PNCib.MSM1fd.BUooTd"), thumbnails, full_res_images), start=1):
        google_images.append(
            {
                "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                    "title"
                ],
                "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                    "href"
                ],
                "source": metadata.select_one(".fxgdke").text,
                "thumbnail": thumbnail,
                "original": original,
            }
        )
    random.shuffle(google_images)
    return google_images
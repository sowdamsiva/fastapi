from fastapi import FastAPI
import time
import requests
import os
import httpx
import asyncio

app =FastAPI()

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR,exist_ok=True)


@app.get("/blocking")
def download_images_blocking():
    start = time.time()
    response = requests.get("https://picsum.photos/v2/list?limit=10")
    response.raise_for_status
    images = response.json()

    for i,img in enumerate(images):
        img_url = img["download_url"]
        img_data = requests.get(img_url).content
        with open(f"{IMAGE_DIR}/blocking_img_{i}.jpg","wb") as f:
            f.write(img_data)

    end = time.time()
    return {
        "method":"blocking",
        "duration":round(end-start,2),
        "message":"Downloaded 10 images"
    }

@app.get("/non-blocking")
async def download_images_nonblocking():
    start = time.time()
    timeout = httpx.Timeout(30.0,connect=10.0)

    async with httpx.AsyncClient(timeout=timeout,follow_redirects=True) as client:
        response = await client.get("https://picsum.photos/v2/list?limit=10")
        response.raise_for_status
        images = response.json()

        async def download_images(img,i):
            try:
                img_url = img["download_url"]
                img_data = await client.get(img_url)
                with open(f"{IMAGE_DIR}/non_blocking_{i}.jpg","wb") as f:
                    f.write(img_data.content)
            except httpx.TimeoutException:
                print(f"time out while downloading the image")

        await asyncio.gather(*(download_images(img,i) for i,img in enumerate(images)))
        end = time.time()
        return {
        "method":"non-blocking",
        "duration":round(end-start,2),
        "message":"Downloaded 10 images"
    }



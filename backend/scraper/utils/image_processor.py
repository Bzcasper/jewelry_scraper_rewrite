from PIL import Image
import io
import aiohttp
import asyncio
import os
import uuid

class ImageProcessor:
    def __init__(self, storage_path='backend/data/images', max_size=1200, quality=85):
        self.storage_path = storage_path
        self.max_size = max_size
        self.quality = quality
        os.makedirs(self.storage_path, exist_ok=True)

    async def process_image(self, image_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image = Image.open(io.BytesIO(image_data))
                    image = self.resize_image(image)
                    image_path = self.save_image(image, image_url)
                    return image_path
        return None

    def resize_image(self, image):
        if max(image.size) > self.max_size:
            image.thumbnail((self.max_size, self.max_size))
        return image

    def save_image(self, image, image_url):
        filename = f"{uuid.uuid4()}.jpg"
        path = os.path.join(self.storage_path, filename)
        image.save(path, format='JPEG', quality=self.quality)
        return path

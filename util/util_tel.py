from pathlib import Path
from PIL import Image


async def instagram_story_background_white(image: Image.Image, result_image: str):
    base = Image.open("util/instagram_story_background_white.png")
    base.paste(image.resize((716, 716)), (230, 335))
    if Path(result_image).suffix == ".jpg":
        base.save(result_image, "JPEG")
    else:
        base.save(result_image)

    base.close()


async def instagram_story(image: Image.Image, result_image: str):
    base = Image.open("util/instagram_story.png")
    base.paste(image.resize((1080, 715)), (0, 0))
    if Path(result_image).suffix == ".jpg":
        base.save(result_image, "JPEG")
    else:
        base.save(result_image)

    base.close()


async def instagram_post_background_white(image: Image.Image, result_image: str):
    base = Image.open("util/instagram_post_background_white.png")
    base.paste(image.resize((607, 607)), (375, 113))
    if Path(result_image).suffix == ".jpg":
        base.save(result_image, "JPEG")
    else:
        base.save(result_image)

    base.close()


async def instagram_post(image: Image.Image, result_image: str):
    base = Image.open("util/instagram_post.png")
    base.paste(image.resize((478, 1080)), (0, 0))
    if Path(result_image).suffix == ".jpg":
        base.save(result_image, "JPEG")
    else:
        base.save(result_image)

    base.close()

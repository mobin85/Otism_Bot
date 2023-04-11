from PIL import Image


def instagram_story_background_white(image: Image.Image, result_image: str):
    base = Image.open("instagram_story_background_white.png")
    base.paste(image.resize((716, 716)), (230, 335))
    base.save(result_image)
    image.close()
    base.close()


def instagram_story(image: Image.Image, result_image: str):
    base = Image.open("instagram_story.png")
    base.paste(image.resize((1080, 715)), (0, 0))
    base.save(result_image)
    image.close()
    base.close()


def instagram_post_background_white(image: Image.Image, result_image: str):
    base = Image.open("instagram_post_background_white.png")
    base.paste(image.resize((607, 607)), (375, 113))
    base.save(result_image)
    image.close()
    base.close()


def instagram_post(image: Image.Image, result_image: str):
    base = Image.open("instagram_post.png")
    base.paste(image.resize((478, 1080)), (0, 0))
    base.save(result_image)
    image.close()
    base.close()

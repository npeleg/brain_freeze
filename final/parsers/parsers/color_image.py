import pathlib
from PIL import Image


def parse_color_image(context, snapshot):
    image = Image('RGB', (snapshot.color_image.width, snapshot.color_image.height))
    image.putdata(snapshot.color_image.pixels)
    path = pathlib.Path(context.directory / 'color_image.jpeg')
    image.save(path)


parse_color_image.fields = ['color_image']

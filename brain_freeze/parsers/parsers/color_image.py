import pathlib
import json
from PIL import Image as PIL


def parse(json_snapshot):
    """extracts and returns the color_image information from json_snapshot"""
    snapshot = json.loads(json_snapshot)
    src_path = snapshot['color_image']['file_path']
    dest_path = pathlib.Path(snapshot['color_image']['dir_path'] + '/color_image.jpg')
    with open(src_path, 'rb') as file:
        data = file.read()
    image = PIL.new('RGB', (2500, 2500))  # TODO change to variables
    image.putdata(data)
    image.save(dest_path)
    color_image = dict(user_id=snapshot['user_id'],
                       datetime=snapshot['datetime'],
                       result='color',
                       color_image='color_image.jpg')
    return json.dumps(color_image)


parse.name = 'color_image'

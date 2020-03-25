import matplotlib.pyplot as plt
import pathlib


# TODO make sure this works
def parse_depth_image(context, snapshot):
    plt.imshow(snapshot.depth_image.pixels, cmap=True)
    path = pathlib.Path(context.directory / 'depth_image.jpeg')
    plt.savefig(path)


parse_depth_image.fields = ['depth_image']

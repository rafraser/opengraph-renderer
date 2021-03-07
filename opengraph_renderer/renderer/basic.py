from PIL import Image
from parse import OpenGraphData


def render(opengraph):
    return Image.new("RGBA", (512, 512))

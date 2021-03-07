from PIL import Image
from parse import OpenGraphData


def render(opengraph: OpenGraphData) -> Image.Image:
    return Image.new("RGBA", (512, 512))

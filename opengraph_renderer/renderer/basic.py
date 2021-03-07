from PIL import Image
from opengraph_renderer.parse import OpenGraphData


def render(opengraph: OpenGraphData) -> Image.Image:
    return Image.new("RGBA", (512, 512))

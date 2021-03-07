from PIL import Image
from opengraph_renderer.renderer.basic import render as render_basic
from opengraph_renderer.parse import OpenGraphData

renderer_list = {
    "basic": render_basic,
}


def render(opengraph: OpenGraphData, renderer: str) -> Image.Image:
    """Renders parsed OpenGraphData into an image

    Args:
        opengraph (OpenGraphData): Parsed OpenGraphData from a page
        renderer (str): Which renderer to use. Must be in the renderer list

    Raises:
        ValueError: if an unknown renderer is specified

    Returns:
        Image: Rendered image
    """
    renderer_func = renderer_list.get(renderer)
    if renderer_func:
        return renderer_func(opengraph)
    else:
        raise ValueError("Unknown renderer")

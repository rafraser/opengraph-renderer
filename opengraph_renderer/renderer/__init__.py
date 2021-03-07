from renderer.basic import render as render_basic

renderer_list = {
    "basic": render_basic,
}


def render(content, renderer):
    renderer_func = renderer_list.get(renderer)
    if renderer_func:
        return renderer_func(content)
    else:
        raise ValueError("Unknown renderer")

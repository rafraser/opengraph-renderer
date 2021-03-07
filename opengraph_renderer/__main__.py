import argparse
import parse
import renderer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--renderer", default="basic")
    parser.add_argument("--out", default="output.png")
    args = parser.parse_args()

    opengraph = parse.opengraph_from_url(args.url)
    rendered_image = renderer.render(opengraph, args.renderer)
    rendered_image.save(args.out)

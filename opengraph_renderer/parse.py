from PIL import Image
from bs4 import BeautifulSoup
from typing import Optional, TypedDict
import requests


class OpenGraphData(TypedDict, total=False):
    title: str
    description: str
    image: Image.Image
    url: str
    color: str


def load_image_from_url(url):
    return Image.open(requests.get(url, stream=True).raw)


def opengraph_from_url(url):
    html = requests.get(url).content
    return opengraph_from_html(html, url)


def opengraph_from_html(html, url=None):
    soup = BeautifulSoup(html, features="html.parser")
    return {
        "title": _find_title(soup),
        "description": _find_description(soup),
        "image": _find_image(soup),
        "url": _find_url(soup, url),
        "color": _find_theme_color(soup)
    }

def _find_title(soup):
    # Check for <meta property="og:title">
    if og_tag := soup.find("meta", attrs={"property": "og:title"}):
        return og_tag.get("content")

    # Check for <title>
    if title_tag := soup.find("title"):
        return title_tag.text


def _find_description(soup):
    # Check for <meta property="og:description">
    if og_tag := soup.find("meta", attrs={"property": "og:description"}):
        return og_tag.get("content")

    # Check for <meta name="description">
    if desc_tag := soup.find("meta", attrs={"name": "description"}):
        return desc_tag.get("content")


def _find_image(soup):
    # Check for <meta property="og:image">
    og_tag = soup.find("meta", attrs={"property": "og:image"})
    if og_tag:
        try:
            return load_image_from_url(og_tag.get("content"))
        except:
            return None

def _find_url(soup, fallback=None):
    # Check for <meta property="og:url">
    if og_tag := soup.find("meta", attrs={"property": "og:url"}):
        return og_tag.get("content")

    # Check for <link rel="canonical">
    if link_tag := soup.find("link", attrs={"rel": "canonical"}):
        return link_tag.get("href")

    # Return fallback value
    return fallback

def _find_theme_color(soup):
    # Check for <meta name="theme-color">
    if color_tag := soup.find("meta", attrs={"name": "theme-color"}):
        return color_tag.get("content")

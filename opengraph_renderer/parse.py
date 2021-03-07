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


def load_image_from_url(url: str) -> Image.Image:
    """Stream an image from a URL into a Pillow image

    Args:
        url (str): URL to stream image from

    Returns:
        Image: Image loaded from URL
    """
    return Image.open(requests.get(url, stream=True).raw)


def opengraph_from_url(url: str) -> OpenGraphData:
    """Given a URL, parses any OpenGraph/meta tags in the page into a nice structure

    Args:
        url (str): URL to parse

    Returns:
        OpenGraphData: Parsed OpenGraph meta tags
    """
    html = requests.get(url).content
    return opengraph_from_html(html, url)


def opengraph_from_html(html: str, url: str = None) -> OpenGraphData:
    """Given raw HTML text, parses any OpenGraph/meta tags in the page into a nice structure

    Args:
        html (str): Raw HTML text
        url (str, optional): Fallback URL, if no canonical URL is on the page.

    Returns:
        OpenGraphData: Parsed OpenGraph meta tags
    """
    soup = BeautifulSoup(html, features="html.parser")
    return {
        "title": _find_title(soup),
        "description": _find_description(soup),
        "image": _find_image(soup),
        "url": _find_url(soup, url),
        "color": _find_theme_color(soup),
    }


def _find_title(soup: BeautifulSoup) -> str:
    # Check for <meta property="og:title">
    if og_tag := soup.find("meta", attrs={"property": "og:title"}):
        return og_tag.get("content")

    # Check for <title>
    if title_tag := soup.find("title"):
        return title_tag.text


def _find_description(soup: BeautifulSoup) -> str:
    # Check for <meta property="og:description">
    if og_tag := soup.find("meta", attrs={"property": "og:description"}):
        return og_tag.get("content")

    # Check for <meta name="description">
    if desc_tag := soup.find("meta", attrs={"name": "description"}):
        return desc_tag.get("content")


def _find_image(soup: BeautifulSoup) -> Image.Image:
    # Check for <meta property="og:image">
    og_tag = soup.find("meta", attrs={"property": "og:image"})
    if og_tag:
        try:
            return load_image_from_url(og_tag.get("content"))
        except:
            return None


def _find_url(soup: BeautifulSoup, fallback: str = None) -> str:
    # Check for <meta property="og:url">
    if og_tag := soup.find("meta", attrs={"property": "og:url"}):
        return og_tag.get("content")

    # Check for <link rel="canonical">
    if link_tag := soup.find("link", attrs={"rel": "canonical"}):
        return link_tag.get("href")

    # Return fallback value
    return fallback


def _find_theme_color(soup: BeautifulSoup) -> str:
    # Check for <meta name="theme-color">
    if color_tag := soup.find("meta", attrs={"name": "theme-color"}):
        return color_tag.get("content")

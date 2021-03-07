import unittest
import opengraph_renderer.parse as parse


class TestParse(unittest.TestCase):
    @staticmethod
    def parse(s):
        return parse.opengraph_from_html(s)

    def test_basic(self):
        test_case = """
        <meta property="og:title" content="Hello, World"/>
        <meta property="og:description" content="Description"/>
        """
        parsed = self.parse(test_case)
        self.assertEqual(parsed.get("title"), "Hello, World")
        self.assertEqual(parsed.get("description"), "Description")

    def test_fallbacks(self):
        test_case = """
        <title>Hello, World</title>
        <meta name="description" content="Description"/>
        """
        parsed = self.parse(test_case)
        self.assertEqual(parsed.get("title"), "Hello, World")
        self.assertEqual(parsed.get("description"), "Description")

    def test_tag_precedence(self):
        test_case = """
        <title>Tagged Title</title>
        <meta property="og:title" content="OG Title"/>
        """
        parsed = self.parse(test_case)
        self.assertEqual(parsed.get("title"), "OG Title")

    def test_opengraph_url(self):
        test_case = """
        <meta property="og:url" content="foo.bar"/>
        """
        parsed = self.parse(test_case)
        self.assertEqual(parsed.get("url"), "foo.bar")

    def test_canonical_url(self):
        test_case = """
        <link rel="canonical" href="foo.bar"/>
        """
        parsed = self.parse(test_case)
        self.assertEqual(parsed.get("url"), "foo.bar")

    def test_fallback_url(self):
        test_case = """
        <title>Nothing important here.</title>
        """
        parsed = parse.opengraph_from_html(test_case, url="foo.bar")
        self.assertEqual(parsed.get("url"), "foo.bar")

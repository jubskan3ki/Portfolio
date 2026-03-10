"""HTML compression middleware."""

import re
from typing import Any, cast

from django.http import HttpRequest, HttpResponse

WHITESPACE_RE = re.compile(r"\s{2,}")
NEWLINE_RE = re.compile(r"\n")
COMMENT_RE = re.compile(r"<!--(?!<!)[^\[>].*?-->", re.DOTALL)
TAG_SPACE_RE = re.compile(r">\s+<")


class CompressHTMLMiddleware:
    """Compress HTML responses by removing unnecessary whitespace."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return self.process_response(response)

    def process_response(self, response: HttpResponse) -> HttpResponse:
        """Compress HTML content."""
        content_type = response.get("Content-Type", "")
        if "text/html" not in content_type:
            return response

        if response.get("Content-Encoding"):
            return response

        if response.status_code != 200:
            return response

        if getattr(response, "no_html_compression", False):
            return response

        if not hasattr(response, "content") or not response.content:
            return response

        try:
            html_content = response.content.decode("utf-8")
            html_content = COMMENT_RE.sub("", html_content)
            html_content = WHITESPACE_RE.sub(" ", html_content)
            html_content = NEWLINE_RE.sub("", html_content)
            html_content = TAG_SPACE_RE.sub("><", html_content)
            html_content = html_content.strip()

            cast(Any, response).content = html_content.encode("utf-8")

            if response.has_header("Content-Length"):
                response["Content-Length"] = str(len(response.content))

        except (UnicodeDecodeError, UnicodeError, AttributeError):
            pass

        return response

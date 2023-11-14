"""
HTTP Basic Server
Contributors:
    :: H. Kamran [@hkamran80] (author)
License: MIT
"""

import http.server
import os
import socketserver

URL_MAPPINGS = {}


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    global URL_MAPPINGS

    def translate_path(self, path):
        # Map .html, .css, .js, and image files automatically
        if (
            path.endswith(".html")
            or path.endswith(".css")
            or path.endswith(".js")
            or path.endswith(".jpg")
            or path.endswith(".jpeg")
            or path.endswith(".png")
            or path.endswith(".gif")
        ):
            return super().translate_path(path)

        compile_url_mappings()
        if path in URL_MAPPINGS:
            return URL_MAPPINGS[path]

        # If the URL doesn't have an extension, try to serve .html first
        html_path = super().translate_path(path + ".html")
        if os.path.isfile(html_path):
            return html_path

        # If no .html file exists, serve the requested path with a .html extension
        return super().translate_path(path + ".html")


def compile_url_mappings(directory: str = os.getcwd()):
    global URL_MAPPINGS

    url_mappings = {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                base_path = os.path.join(root.replace(directory, ""), filename)
                url_mappings[base_path.replace("index.html", "")[:-1] or "/"] = (
                    f".{base_path}" if base_path.startswith("/") else f"./{base_path}"
                )

    URL_MAPPINGS = url_mappings


def serve(port: int) -> bool:
    # Create the server with the custom handler
    with socketserver.TCPServer(("", port), RequestHandler) as httpd:
        print(f"Serving at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            return False

    return False


if __name__ == "__main__":
    # Set the server port and directory
    port = os.getenv("PORT", 8080)

    serve_status = True
    while serve_status:
        try:
            serve_status = serve(port)
        except OSError as error:
            if error.errno == 98:  # Address already in use
                port += 1

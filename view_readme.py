#!/usr/bin/env python3
"""
README.md viewer with proper Markdown rendering and image support.
Opens a local web server to preview the README as it would appear on GitHub.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path
from urllib.parse import unquote

# Change to project root directory
project_root = Path(__file__).parent
os.chdir(project_root)

PORT = 8000

# GitHub-style CSS for Markdown rendering
GITHUB_CSS = """
<style>
body {
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
    background: #fff;
    color: #24292e;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}
h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
h3 { font-size: 1.25em; }
code {
    background-color: rgba(27,31,35,.05);
    border-radius: 3px;
    font-size: 85%;
    margin: 0;
    padding: .2em .4em;
    font-family: SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;
}
pre {
    background-color: #f6f8fa;
    border-radius: 3px;
    font-size: 85%;
    line-height: 1.45;
    overflow: auto;
    padding: 16px;
}
pre code {
    background-color: transparent;
    border: 0;
    display: inline;
    line-height: inherit;
    margin: 0;
    overflow: visible;
    padding: 0;
}
img {
    max-width: 100%;
    box-sizing: content-box;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 5px;
    margin: 10px 0;
}
table {
    border-spacing: 0;
    border-collapse: collapse;
    margin-top: 0;
    margin-bottom: 16px;
}
table th, table td {
    padding: 6px 13px;
    border: 1px solid #dfe2e5;
}
table tr { background-color: #fff; border-top: 1px solid #c6cbd1; }
table tr:nth-child(2n) { background-color: #f6f8fa; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: 0; border-top: 1px solid #eaecef; margin: 24px 0; }
blockquote {
    padding: 0 1em;
    color: #6a737d;
    border-left: .25em solid #dfe2e5;
    margin: 0 0 16px 0;
}
ul, ol { padding-left: 2em; margin-top: 0; margin-bottom: 16px; }
</style>
"""

class MarkdownHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Decode URL
        path = unquote(self.path)

        # Serve root or README.md as HTML
        if path == '/' or path == '/README.md':
            self.serve_markdown_as_html()
        else:
            # Serve other files (images, etc.) normally
            super().do_GET()

    def serve_markdown_as_html(self):
        """Convert README.md to HTML and serve it."""
        try:
            # Try to import markdown
            try:
                import markdown
                has_markdown = True
            except ImportError:
                has_markdown = False

            # Read README.md
            with open('README.md', 'r', encoding='utf-8') as f:
                md_content = f.read()

            if has_markdown:
                # Convert Markdown to HTML with extensions
                html_content = markdown.markdown(
                    md_content,
                    extensions=['fenced_code', 'tables', 'nl2br']
                )
            else:
                # Fallback: Simple conversion (just wrap in <pre> for basic display)
                html_content = f'<pre style="white-space: pre-wrap;">{md_content}</pre>'
                html_content += '<p style="color: red; font-weight: bold;">Note: Install markdown package for better rendering: pip install markdown</p>'

            # Wrap in HTML document
            full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyVarChart README</title>
    {GITHUB_CSS}
</head>
<body>
    {html_content}
</body>
</html>"""

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(full_html.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Error rendering README: {str(e)}")

def check_dependencies():
    """Check if markdown package is installed."""
    try:
        import markdown
        return True
    except ImportError:
        print("WARNING: 'markdown' package not found.")
        print("For better rendering, install it: pip install markdown")
        print("(Will use basic fallback rendering)\n")
        return False

def main():
    print(f"Starting README.md viewer...")
    print(f"Project root: {project_root}")
    print(f"Server will run at: http://localhost:{PORT}")
    print(f"\nServing files from: {os.getcwd()}")

    # Check if README.md exists
    if not os.path.exists('README.md'):
        print("ERROR: README.md not found in current directory!")
        sys.exit(1)

    # Check if examples folder exists
    if not os.path.exists('examples'):
        print("WARNING: examples/ folder not found!")
    else:
        # Count images
        example_images = list(Path('examples').glob('*.png'))
        print(f"Found {len(example_images)} example images in examples/")

    # Check for markdown package
    has_markdown = check_dependencies()

    print(f"\nOpen http://localhost:{PORT}/ in your browser")
    print(f"Images will be loaded from: examples/*.png")
    print(f"\nPress Ctrl+C to stop the server\n")

    # Start server
    with socketserver.TCPServer(("", PORT), MarkdownHTTPRequestHandler) as httpd:
        # Open browser automatically
        url = f"http://localhost:{PORT}/"
        print(f"Opening browser to {url}...")
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()

if __name__ == '__main__':
    main()


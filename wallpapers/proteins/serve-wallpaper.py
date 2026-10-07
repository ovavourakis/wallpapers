#!/usr/bin/env python3
"""Serve the wallpaper and relay the two required SAbDab2 endpoints locally."""
import argparse
import json
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen

UPSTREAM = 'https://sabdab.opig.stats.ox.ac.uk/api'

class WallpaperHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Local file-based Plash pages have the serialized origin "null".
        if self.headers.get('Origin') == 'null':
            self.send_header('Access-Control-Allow-Origin', 'null')
            self.send_header('Vary', 'Origin')
        super().end_headers()

    def do_OPTIONS(self):
        if self.path != '/sabdab-api/download/structures':
            self.send_error(404)
            return
        self.send_response(204)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        path = urlsplit(self.path)
        if path.path == '/sabdab-api/pdb':
            query = parse_qs(path.query)
            try:
                if set(query) - {'processing_status', 'antigen_type', 'limit', 'offset'}:
                    raise ValueError()
                if query.get('processing_status') != ['ACCEPTED'] or query.get('limit') != ['1']:
                    raise ValueError()
                if query.get('antigen_type', ['true']) != ['true']:
                    raise ValueError()
                if int(query.get('offset', ['-1'])[0]) < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                self.send_error(400, 'Invalid SAbDab query')
                return
            self.relay(Request(UPSTREAM + '/pdb?' + path.query))
        elif __import__('re').fullmatch(r'/sabdab-api/frontend/pdb/pdb_[a-zA-Z0-9]{8}', path.path):
            self.relay(Request(UPSTREAM + path.path.removeprefix('/sabdab-api')))
        elif path.path.startswith('/sabdab-api'):
            self.send_error(404)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/sabdab-api/download/structures':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 2048:
                raise ValueError()
            body = self.rfile.read(length)
            payload = json.loads(body)
            structures = payload['structures']
            if len(structures) != 1 or structures[0].get('full_structure') is not True:
                raise ValueError()
            if not re.fullmatch(r'pdb_[a-zA-Z0-9]{8}', structures[0].get('pdb_id', '')):
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            self.send_error(400, 'Expected one full SAbDab structure')
            return
        self.relay(Request(UPSTREAM + '/download/structures', data=body,
                           headers={'Content-Type': 'application/json', 'Accept': 'chemical/x-mmcif'}))

    def relay(self, request):
        try:
            with urlopen(request, timeout=25) as upstream:
                body = upstream.read()
                content_encoding = upstream.headers.get('Content-Encoding')
                self.send_response(upstream.status)
                self.send_header('Content-Type', upstream.headers.get('Content-Type', 'application/octet-stream'))
                # Keep gzip encoding: the browser decompresses the mmCIF response.
                if content_encoding:
                    self.send_header('Content-Encoding', content_encoding)
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
        except HTTPError as error:
            self.send_error(error.code, 'SAbDab request failed')
        except (URLError, TimeoutError, OSError, ValueError):
            self.send_error(502, 'SAbDab unavailable')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(WallpaperHandler, directory=str(root)))
    print(f'Wallpaper: http://127.0.0.1:{args.port}/index.html', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

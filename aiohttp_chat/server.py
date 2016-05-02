import logging

import sys
import argparse
import asyncio
import json

import coloredlogs
import aiohttp_themes
import aiohttp_debugtoolbar
import aiohttp
from aiohttp import web

from . import model, utils
from .themes.typewriter import TypewriterTheme

log = logging.getLogger(__name__)


async def client_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    remote_addr = utils.remote_address(request)

    clients = request.app['clients']
    clients[ws] = remote_addr

    try:
        async for msg in ws:
            if msg.tp == aiohttp.MsgType.binary:
                obj = json.loads(msg.data.decode('utf-8'))
                for other_ws in clients:
                    if other_ws != ws:
                        other_ws.send_bytes(msg.data)
            elif msg.tp == aiohttp.MsgType.closed:
                log.info("Connection closed.")
                break
            elif msg.tp == aiohttp.MsgType.error:
                log.info("User websocket error: %s", msg)
                break
            else:
                log.error("Unknown user message type: %s, ignoring.", msg.tp)
    finally:
        del clients[ws]
        log.info("Client connection closed: %s", remote_addr)

    return ws


@aiohttp_themes.template('index.html')
async def index_view(request):
    return {
        'request': request,
    }


def make_app(loop, dburl, debug=False):
    app = web.Application()
    app['clients'] = {}

    model.init(url=dburl)

    aiohttp_themes.setup(app,
                         themes=[TypewriterTheme],
                         debug=debug,
                         theme_strategy='typewriter',
                         compiled_asset_dir='/tmp/compiled')

    #if debug:
    #    aiohttp_debugtoolbar.setup(app)

    app.router.add_route('GET', '/', index_view)
    app.router.add_route('GET', '/client', client_handler)

    return app


def main(argv=sys.argv):
    p = argparse.ArgumentParser(description='Chat Server')

    p.add_argument('--port', default=8080)
    p.add_argument('--verbose', default='store_true')
    p.add_argument('dbfile')

    opts, args = p.parse_known_args(argv[1:])

    dburl = 'sqlite:///' + opts.dbfile

    coloredlogs.install(level='DEBUG' if opts.verbose else 'INFO')

    loop = asyncio.get_event_loop()
    app = make_app(loop, dburl=dburl, debug=True)
    web.run_app(app, port=opts.port)

import sys

from twisted.internet.endpoints import serverFromString
from twisted.internet import reactor
from twisted.python import log

from .relay import Relay, RelaySite
import click


@click.command()
@click.option('--listen',
              default='tcp:8001',
              help='The TCP port to listen on.')
@click.option('--url',
              default=None,
              help=('Where to find heatherr. For example '
                    'http://username:password@localhost:8000/relay/'))
@click.option('--verbose/--no-verbose',
              default=False,
              help='Turn on verbose log output.')
@click.option('--debug/--no-debug',
              default=False,
              help='Turn on Websocket debugging output.')
@click.option('--logfile',
              help='Where to log output to.',
              type=click.File('a'),
              default=sys.stdout)
def run(listen, url, verbose, debug, logfile):
    if not url:
        raise click.UsageError('--url is required.')
    log.startLogging(logfile)

    endpoint = serverFromString(reactor, str(listen))
    site = RelaySite(Relay(url, debug=debug, verbose=verbose).app.resource())
    site.verbose = verbose
    endpoint.listen(site)
    reactor.run()

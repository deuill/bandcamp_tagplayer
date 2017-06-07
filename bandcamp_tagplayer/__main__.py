#!/usr/bin/python3

"""
bandcamp_tagplayer
Creates mpd playlists from Bandcamp genre tags.

Config file at: ~/.config/bandcamp_tagplayer/config

Usage:
  bandcamp_tagplayer
  bandcamp_tagplayer <tag>
  bandcamp_tagplayer (-h | --help)
  bandcamp_tagplayer (--version)

Options:
  -t --tag                  Search tag
  -h --help                 Show this screen.
  -v --version              Show version.
"""

""" Code:
Gregory Parrish
    http://github.com/greggparrish
"""

import os
from docopt import docopt
from slugify import slugify

from tagplayer import Tagplayer


def main():
  arguments = docopt(__doc__, version='bandcamp_tagplayer 1.0')
  bct = Tagplayer()
  if arguments['<tag>']:
    tag = slugify(arguments['<tag>'])
    bct.check_tag(tag)
  else:
    bct.ask_for_tag()

if __name__ == '__main__':
    main()


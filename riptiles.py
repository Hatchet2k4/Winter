#!/usr/bin/env python

import ika


def rip_tiles(image, width, height, span, tilecount):
    """This is a simple function that takes any image that is formatted
    like a tileset and rips the tiles into a list which is then
    returned.

    image - image to rip from
    width/height - width and height of a single tile
    span - how many tiles per row
    tilecount - number of tiles to rip
    """
    tiles = []
    big_image = ika.Canvas(image)
    for i in range(tilecount):
        tile = ika.Canvas(width, height)
        big_image.Blit(tile, -1 - (i % span * (width + 1)),
                       -1 - (i / span * (height + 1)), ika.Opaque)
        tiles.append(ika.Image(tile))
    return tiles

def RipTiles(image, width, height, span=None, tilecount=None):
    """This is a simple function that takes any image that is formatted
    like a tileset and rips the tiles into a list which is then
    returned.

    image - image to rip from
    width/height - width and height of a single tile
    span - how many tiles per row
    tilecount - number of tiles to rip
    """
    tiles = []
    big_image = ika.Canvas(image)

    # do some figurin:) ~infey
    if span == None and tilecount == None:
        span = (big_image.width - 1) / (width + 1)
        tilecount = span * ((big_image.height - 1) / (height + 1))

    for i in range(tilecount):
        tile = ika.Canvas(width, height)
        big_image.Blit(tile, -1 - (i % span * (width + 1)),
                       -1 - (i / span * (height + 1)), ika.Opaque)
        tiles.append(ika.Image(tile))
    return tiles

from sources import tantan, tinder, happn

SOURCE_MAP = {
    'tantan': tantan.Tantan,
    'tinder': tinder.Tinder,
    'happn': happn.Happn,
}

PIXEL_MAP_SCALE = {
    720: 1,
    1280: 1,
}
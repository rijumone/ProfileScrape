from sources import tantan, tinder, happn, woo

SOURCE_MAP = {
    'tantan': tantan.Tantan,
    'tinder': tinder.Tinder,
    'happn': happn.Happn,
    'woo': woo.Woo,
}

PIXEL_MAP_SCALE = {
    720: 1,
    1280: 1,
}
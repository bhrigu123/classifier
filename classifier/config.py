"""Configure for classifier
"""

import os

import six.moves.configparser as configparser

CONFIG_PATH = os.path.expanduser('~/.classifier.cfg')
CONFIG = None

ELEMENT_DILIMETER = ','
KEY_VAL_DILIMETER = ':'

FORMATS = 'Formats'
DEFAULT_CONFIG = {
    FORMATS: {
        'Music': ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff', '.wav'],
        'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts'],
        'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd'],
        'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz', '.xz'],
        'Documents': ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsv', '.xlsx',
                      '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
        'Books': ['.mobi', '.epub', '.chm'],
        'DEBPackages': ['.deb'],
        'RPMPackages': ['.rpm']
    }
}


def _pair_string(pair):
    return "%s%s %s" % (pair[0].strip(), KEY_VAL_DILIMETER, pair[1].strip())


def _string_pair(s):
    k, v = s.split(KEY_VAL_DILIMETER)
    return k.strip(), v.strip()


def _set(parser, section, items):
    try:
        parser.add_section(section)
    except configparser.DuplicateSectionError:
        pass
    dilimeter = "%s " % ELEMENT_DILIMETER
    for key, val in items.items():
        if type(val) is list:
            val_str = dilimeter.join(list(map(lambda s: s.strip(), val)))
            parser.set(section, key, val_str)
        elif type(val) is dict:
            val_str = dilimeter.join(list(map(_pair_string, val.items())))
            parser.set(section, key, val_str)
        else:
            parser.set(section, key, val)


def _init_config(parser, config):
    for sec, values in config.items():
        _set(parser, sec, values)


def init_config(write_file=False):
    global CONFIG
    if CONFIG is None:
        CONFIG = configparser.SafeConfigParser()

    if os.path.exists(CONFIG_PATH):
        try:
            CONFIG.read(CONFIG_PATH)
        except configparser.ParsingError:
            _init_config(CONFIG, DEFAULT_CONFIG)
    else:
        _init_config(CONFIG, DEFAULT_CONFIG)
        if write_file:
            with open(CONFIG_PATH, 'w') as config_file:
                CONFIG.write(config_file)


def _get(parser, section, typ=None):
    conf = {}
    for key, val in parser.items(section):
        if typ is list:
            conf[key] = list(map(lambda s: s.strip(),
                                 val.split(ELEMENT_DILIMETER)))
        elif typ is dict:
            conf[key] = dict(_string_pair(e)
                             for e in val.split(ELEMENT_DILIMETER))
        else:
            conf[key] = val.strip()
    return conf


def get_formats():
    try:
        return _get(CONFIG, FORMATS, typ=list)
    except configparser.NoSectionError:
        return DEFAULT_CONFIG[FORMATS]

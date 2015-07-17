'''
config_helper.py

This file is meant as a wrapper for the config file and resources cache dictionary
    to be used with GameGen.py.
config_helper supports two config files: One main file, and one optional file to be
    found in the 'card set' folder. Any options in the optional config file will
    overwrite identical options in the main file. In this way, card sets can be
    configured to vary slightly from the main config without having to constantly
    update the main file.

When first started, GameGen should call LoadConfig to load the config files. Assets
    like fonts and images are not preloaded into the resources cache. Rather they
    are processed and loaded as needed.
From within a CardGen script, the specific function should be called to load
    a particular type from the resources cache. E.g. To load a font, the getfont()
    function should be called.
config_helper supports a hierarchy of default values in both the config file and
    resources cache. Every function to be called from the CardGen script should
    include both the card name and the card type. This way, config_helper will
    check the resources cache or config file in the following order of sections
    for the given option: Card name -> Card type -> Card Defaults
If the resource is not found in the cache (for some options), config_helper
    will attempt to load that resource from the config and add it to the cache.
'''

import os
import PIL_Helper as ph
from ConfigParser import SafeConfigParser, NoOptionError

config = None
resources_cache = None
DEFAULT_SECTION = "Card Defaults"
CARD_NAME_PREFIX = "Card."
CARD_TYPE_PREFIX = "Type."

pjoin = os.path.join

def LoadConfig(folder, card_set, filename):
    '''
    @param str folder: The game folder, e.g. TSSSF
    @param str card_set: The folder within the game folder that stores the
        given card set. e.g., Core Deck 1.1.5
    @param str filename: The name of the config files to be loaded. Both config
        files must have the same name.

    Loads a required config file from the game folder, passing it back to the main
        function. Can also load an optional config file in the card_set folder, and
        that config can overwrite anything in the first config. This is useful for
        making small tweaks to the config file that apply only to that card set.

    @return None: The config file and resources cache will be saved in this module.
        No other module should be handling these objects.
    '''
    global config, resources_cache
    # Init config object
    config = SafeConfigParser()
    # Load main config
    config.read(pjoin(folder, filename))
    # Load possible alternate config
    alt_config_path = pjoin(folder, card_set, filename)
    if os.path.exists(alt_config_path):
        config.read(alt_config_path)
    # Initialize the resources_cache
    resources_cache = {}

def get(option, section="Settings", val_type="str", default=None):
    '''
    @param str option: The option to pull the value for
    @param str section: The config section to pull from
    @param str val_type: The value type to try to cast the config option to.
        Accepted options: str (default), int, float, bool
    @param any default: If the given option isn't found, default is returned.

    Attempts to load the given option from the given section, casting it 
        to the given value type.
    If default is returned, it is not cast using the val_type, but will be
        returned exactly as it was passed in.

    @return str or None: None, or the value from the config
    '''
    if not config.has_option(section, option):
        if default:
            return default
        raise ConfigParseError("No config option {}/{}".format(section, option))
    if val_type == "str":
        return config.get(section, option)
    if val_type == "int":
        return config.getint(section, option)
    if val_type == "float":
        return config.getfloat(section, option)
    if val_type == "bool":
        return config.getboolean(section, option)
    raise ConfigParseError("Invalid val_type: {}\n".format(val_type)+
                           "The only valid options are: str, int, float, bool")

def getcolor(option, card_type=None, card_name=None):
    option = "color_"+option if option else "color"
    return _get_list_from_config(option, card_type, card_name)

def getanchor(option, card_type=None, card_name=None):
    option = "anchor_"+option if option else "anchor"
    anchor = _get_list_from_config(option, card_type, card_name)
    if not (isinstance(anchor, (list, tuple)) and len(anchor) == 2):
        raise AnchorParseError(
            "Not a valid anchor: {}|{}|{}".format(
                option, card_type, card_name
                )
            )
    return anchor

def getart(filename, folder=None):
    '''
    The art is not loaded into the cache because it's expected that the art is
    unique for each card. This means that 99% of the time, the art will not
    need to be cached, and when building a deck of 160+ cards, you don't
    want to cache 160+ card art images for no reason.
    '''
    if folder is None:
        folder = get("card art directory", DEFAULT_SECTION)
    return ph.LoadImage(pjoin(folder, filename))

def getframe(option, card_type=None, card_name=None):
    # Name of the option for the frame image
    option = "frame_"+option if option else "frame"
    return _find_and_load_image(option, card_type, card_name,
                                get("frames directory", DEFAULT_SECTION))

def getback(option, card_type=None, card_name=None):
    # Name of the option for the back image
    option = "back_"+option if option else "back"
    return _find_and_load_image(option, card_type, card_name,
                                get("frames directory", DEFAULT_SECTION))

def getsymbol(option, card_type=None, card_name=None):
    # Name of the option for the symbol image
    option = "symbol_"+option if option else "symbol"
    return _find_and_load_image(option, card_type, card_name,
                                get("symbols directory", DEFAULT_SECTION))

def getfont(option, card_type=None, card_name=None):
    '''
    Checks for a font object in the resources_cache dict. If it's not there,
    checks the config file and attempts to load the font into the
    resources_cache directory. 
    '''
    # Name of the option for the font object and filename
    font_option = "font_"+option
    fontfile_option = "fontfile_"+option
    # Check resources_cache for font object
    font = _get_resource(font_option, card_type, card_name)
    if font is None:
        # If not in resources_cache, check if the fontfile_ option exists in the
        # config.
        section = _find_option_in_config(fontfile_option,
                                        card_type, card_name)
        # If not, throw an error.
        if section is None:
            raise FontParseError("Font not found: {}|{}|{}".format(
                option, card_type, card_name
                ))
        # Attempt to load a new font object from the config
        font = _load_font(section, option,
                          get("fonts directory", DEFAULT_SECTION))
        # Add that new font object to the resources_cache object.
        _add_to_resources(section, font_option, font)
    return font

def _find_option_in_config(option, card_type=None, card_name=None):
    card_name = CARD_NAME_PREFIX+card_name
    card_type = CARD_TYPE_PREFIX+card_type
    if config.has_section(card_name) and config.has_option(card_name, option):
        return card_name
    if config.has_section(card_type) and config.has_option(card_type, option):
        return card_type
    if config.has_section(DEFAULT_SECTION) and config.has_option(DEFAULT_SECTION, option):
        return DEFAULT_SECTION
    return None

def _get_resource(option, card_type=None, card_name=None):
    '''
    @param str option: The option to pull the value for
    @param str card_type: If not None, will check this section for the given option.
    @param str card_name: If not None, will check this section for the given option
        before 'card_type'.

    Attempts to return the value for the given option from the resources_cache dict,
        first from a section matching card_name, then from a section matching
        card_type, then the Card Defaults section. If none of the sections
        (if they exist) have that option, then None is returned.
    All resources should be made the correct type as they're loaded during LoadConfig,
        so no checking of types is performed in this function.

    @return str or None: None, or the value from the config
    '''
    card_name = CARD_NAME_PREFIX+card_name
    card_type = CARD_TYPE_PREFIX+card_type
    if card_name in resources_cache and option in resources_cache[card_name]:
        section = card_name
    elif card_type in resources_cache and option in resources_cache[card_type]:
        section = card_type
    elif DEFAULT_SECTION in resources_cache and option in resources_cache[DEFAULT_SECTION]:
        section = DEFAULT_SECTION
    else:
        return None
    return resources_cache[section][option]

def _get_list_from_config(option, card_type=None, card_name=None):
    '''
    Attempts to retrieve a value from the config file, then convert it to a
    list of integers. If the conversion fails, it just returns the string value.
    
    The list must be separated by commas. Leading and trailing spaces around
    the items in the list are allowed. Any leading or trailing spaces or
    brackers ()[] will be stripped off the string before splitting around the
    commas.

    @return tuple
    '''
    section = _find_option_in_config(option, card_type, card_name)
    if section is None:
        raise ConfigParseError("Option not found in config: {}|{}|{}".format(
            option, card_type, card_name
            ))
    value_str = get(option, section)
    # Try to convert str to list
    try:
        return [int(item) for item in value_str.strip(' ()[]').split(',')]
    except ValueError:
        return value_str

def _find_and_load_image(option, card_type=None, card_name=None,
                         resource_directory=None):
    '''
    Checks for an image in the resources_cache dict. If it's not there,
    checks the config file and attempts to load the image into the
    resources_cache directory. 
    '''
    image = _get_resource(option, card_type, card_name)
    if image is None:
        section = _find_option_in_config(option,
                                         card_type, card_name)
        # If not, throw an error.
        if section is None:
            raise FrameParseError("Image not found: {}|{}|{}".format(
                option, card_type, card_name
                ))
        # Attempt to load a image from the config
        image = ph.LoadImage(pjoin(resource_directory,
                                   get(option, section)))
        # Add that new image to the resources_cache object.
        _add_to_resources(section, option, image)
    return image

def _load_font(section, fontname, fonts_directory):
    try:
        fontfile = get("fontfile_"+fontname, section)
    except NoOptionError:
        raise FontParseError("No config option {}/fontsize_{}".format(
            section, fontname
            ))
    fontpath = os.path.abspath(pjoin(fonts_directory, fontfile))
    # Make sure the fontpath exists
    if not os.path.exists(fontpath):
        raise FontParseError("{} does not exist".format(fontpath))
    # Make sure the fontsize is an int
    try:
        fontsize = get("fontsize_"+fontname, section, val_type="int")
    except NoOptionError:
        raise FontParseError("No config option {}/fontsize_{}".format(
            section, fontname
            ))
    except ValueError:
        raise FontParseError("{}/fontsize_{} is not an int: {}".format(
            section, fontname, config.get(section, "fontsize_"+fontname)
            ))
    # Create font object
    try:
        return ph.BuildFont(fontpath, fontsize)
    except Exception as e:
        raise FontParseError("Error when loading font: {}".format(e))

def _add_to_resources(section, option, value):
    # If the section (e.g. Pony) doesn't exist in resources_cache, create it.
    if section not in resources_cache:
        resources_cache[section] = {}
    resources_cache[section][option] = value

def print_config():
    if len(config.sections()) == 0:
        print ""
    for section in config.sections():
        print "{}: {}".format(section, config.items(section))

def print_resources():
    if resources_cache is None:
        print resources_cache
        return
    if len(resources_cache) == 0:
        print ""
    for section in resources_cache:
        print "{}: {}".format(section, resources_cache[section])

class ConfigParseError(Exception):
    pass

class FontParseError(ConfigParseError):
    pass

class FrameParseError(ConfigParseError):
    pass

class AnchorParseError(ConfigParseError):
    pass

if __name__ == "__main__":
    raise Exception("Not a main module.")

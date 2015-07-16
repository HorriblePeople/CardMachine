import os
import PIL_Helper as ph
from ConfigParser import SafeConfigParser, NoOptionError

config = None
resources = None
preload_assets = None

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

    Some config options are meant to have the assets preloaded.
    '''
    global config, resources
    # Init config object
    config = SafeConfigParser()
    # Load main config
    config.read(pjoin(folder, filename))
    # Load possible alternate config
    alt_config_path = pjoin(folder, card_set, filename)
    if os.path.exists(alt_config_path):
        config.read(alt_config_path)
    # Parse all necessary config options into ready-made objects
    # and store them in the resources object
    print __file__
    if get("preload assets", val_type="bool", default=True):
        resources = {}
        parse_fonts(folder)

def parse_fonts(folder):
    '''
    Parses every matching "fontfile_*" and "fontsize_*" pair in every config
    section, and adds a correspending "font_*" object to that section, which
    is the created font object.
    '''
    fonts_directory = get("fonts directory", "Card Defaults")
    if fonts_directory is None:
        raise FontParseError("No 'fonts_directory' found in config file.")
    fonts_directory = pjoin(folder, fonts_directory)
    # Go through every section in the config file, except for Defaults
    for section in config.sections():
        if section is not "Defaults":
            for option, value in config.items(section):
                # If we find a fontfile_* option, find its fontsize_* pair
                if option.startswith("fontfile_"):
                    print_resources()
                    # Pull name of the font object from config option
                    # Note: Not the font filename, but the name applied to it within
                    # the code. E.g. "Flavortext"
                    fontname = option[9:]
                    # If the section (e.g. Pony) doesn't exist in resources, create it.
                    if section not in resources:
                        resources[section] = {}
                    resources[section]["font_"+fontname] = loadfont(
                        section, fontname, fonts_directory
                        )

def get(option, section="Settings", val_type="str", default=None):
    '''
    @param str option: The option to pull the value for
    @param str section: The config section to pull from
    @param str val_type: The value type to try to cast the config option to.
        Accepted options: str (default), int, float, bool

    Convenience function for allowing 
    Attempts to return the value for the given option, first from a section
        matching card_name, then from a section matching card_type, then
        from the Defaults section. If none of the sections (if they exist)
        have that option, then None is returned.

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

def get_resource(option, card_type=None, card_name=None):
    '''
    @param str option: The option to pull the value for
    @param str card_type: If not None, will check this section for the given option.
    @param str card_name: If not None, will check this section for the given option
        before 'card_type'.

    Attempts to return the value for the given option from the resources dict, first
        from a section matching card_name, then from a section matching card_type,
        then the Card Defaults section. If none of the sections (if they exist)
        have that option, then None is returned.
    All resources should be made the correct type as they're loaded during LoadConfig,
        so no checking of types is performed in this function.

    @return str or None: None, or the value from the config
    '''
    if card_name in resources and option in resources[card_name]:
        section = card_name
    elif card_type in resources and option in resources[card_type]:
        section = card_type
    elif "Card Defaults" in resources and option in resources["Card Defaults"]:
        section = "Card Defaults"
    else:
        return None
    return resources[section][option]

def getfont(option, card_type=None, card_name=None):
    if not preload_assets:
        return loadfont(card_type, option.lower(), get("fonts directory", "Card Defaults"))
    font = get_resource("font_"+option.lower(), card_type, card_name)
    if font is None:
        raise FontParseError("Font not found: {}|{}|{}".format(
            option, card_type, card_name
            ))
    return font

def loadfont(section, fontname, fonts_directory):
    try:
        fontfile = get("fontfile_"+fontname, section)
    except NoOptionError:
        raise FontParseError("No config option {}/fontsize_{}".format(
            section, fontname
            ))
    fontpath = pjoin(fonts_directory, fontfile)
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
    

##def getimage(config, option, card_type=None, card_name=None):
##    image = get(config, option, card_type, card_name)
##    if image is None:
##        return Image.new('L', (1,1))
##    return value

def print_config():
    for section in config.sections():
        print config.items(section)

def print_resources():
    if resources is None:
        print resources
        return
    for section in resources:
        print section, resources[section]

class ConfigParseError(Exception):
    pass

class FontParseError(ConfigParseError):
    pass

if __name__ == "__main__":
    raise Exception("Not a main module.")

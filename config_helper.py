import os
import PIL_Helper as ph
from ConfigParser import SafeConfigParser, NoOptionError

config = None
resources_cache = None

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
    global config, resources_cache
    # Init config object
    config = SafeConfigParser()
    # Load main config
    config.read(pjoin(folder, filename))
    # Load possible alternate config
    alt_config_path = pjoin(folder, card_set, filename)
    if os.path.exists(alt_config_path):
        config.read(alt_config_path)
    # Parse all necessary config options into ready-made objects
    # and store them in the resources_cache object
    print __file__
    resources_cache = {}

def add_to_resources(section, option, value):
    # If the section (e.g. Pony) doesn't exist in resources_cache, create it.
    if section not in resources_cache:
        resources_cache[section] = {}
    resources_cache[section][option] = value

def find_option_in_config(option, card_type=None, card_name=None):
    if config.has_section(card_name) and config.has_option(card_name, option):
        return card_name
    if config.has_section(card_type) and config.has_option(card_type, option):
        return card_type
    if config.has_section("Card Defaults") and config.has_option("Card Defaults", option):
        return "Card Defaults"
    return None

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

    Attempts to return the value for the given option from the resources_cache dict,
        first from a section matching card_name, then from a section matching
        card_type, then the Card Defaults section. If none of the sections
        (if they exist) have that option, then None is returned.
    All resources should be made the correct type as they're loaded during LoadConfig,
        so no checking of types is performed in this function.

    @return str or None: None, or the value from the config
    '''
    if card_name in resources_cache and option in resources_cache[card_name]:
        section = card_name
    elif card_type in resources_cache and option in resources_cache[card_type]:
        section = card_type
    elif "Card Defaults" in resources_cache and option in resources_cache["Card Defaults"]:
        section = "Card Defaults"
    else:
        return None
    return resources_cache[section][option]

def getfont(option, card_type=None, card_name=None):
    '''
    Checks for a font object in the resources directory. If it's not there,
    checks the config file and attempts to load the font into the resources_cache
    directory. 
    '''
    # Name of the option for the font object
    option = "font_"+option.lower()
    # Check resources_cache for font object
    font = get_resource(option, card_type, card_name)
    if font is None:
        # If not in resources_cache, check if the fontfile_ option exists in the
        # config.
        section = find_option_in_config("fontfile_"+option.lower(),
                                        card_type, card_name)
        # If not, throw an error.
        if section is None:
            raise FontParseError("Font not found: {}|{}|{}".format(
                option, card_type, card_name
                ))
        # Attempt to load a new font object from the config
        font = loadfont(section, option, get("fonts directory", "Card Defaults"))
        # Add that new font object to the resources_cache object.
        add_to_resources(section, option, font)
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
    if resources_cache is None:
        print resources_cache
        return
    for section in resources_cache:
        print section, resources_cache[section]

class ConfigParseError(Exception):
    pass

class FontParseError(ConfigParseError):
    pass

if __name__ == "__main__":
    raise Exception("Not a main module.")

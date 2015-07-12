import os
import PIL_Helper as ph
import ConfigParser

config = None

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

    @return SafeConfigParser: The config object to be used for building a card
    '''
    global config
    config = ConfigParser.SafeConfigParser()
    # Load main config
    config.read(pjoin(folder, filename))
    # Load possible alternate config
    alt_config_path = pjoin(folder, card_set, filename)
    if os.path.exists(alt_config_path):
        config.read(alt_config_path)
    # Parse all necessary config options into ready-made objects
    # and store them in the config file
    print __file__
    parse_fonts(folder)

def parse_fonts(folder):
    '''
    Parses every matching "fontfile_*" and "fontsize_*" pair in every config
    section, and adds a correspending "font_*" object to that section, which
    is the created font object.
    '''
    fonts_directory = get("fonts_directory")
    if fonts_directory is None:
        raise FontParseError("No 'fonts_directory' found in config file.")
    # Go through every section in the config file, except for Defaults
    for section in config.sections():
        if not section == "Defaults":
            for option,value in config.items(section):
                # If we find a fontfile_* option, find its fontsize_* pair
                if option.startswith("fontfile_"):
                    fontname = option[9:]
                    if "fontsize_"+fontname not in config.options(section):
                        raise FontParseError(
                            "Found a font path without a matching font size: {}/{}".format(
                                section, option
                                )
                            )
                    # Make sure the fontsize is an int.
                    try:
                        fontsize = config.getint(section, "fontsize_"+fontname)
                    except ValueError:
                        raise FontParseError("{}/fontsize_{} is not an int: {}".format(
                            section, fontname, config.get(section, "fontsize_"+fontname)
                            ))
                    fontpath = pjoin(folder, fonts_directory, value)
                    # Make sure the fontpath exists
                    if not os.path.exists(fontpath):
                        raise FontParseError("{} does not exist".format(fontpath))
                    # Create font object
                    try:
                        font_object = ph.BuildFont(fontpath, fontsize)
                    except Exception as e:
                        raise FontParseError("Error when loading font: {}".format(e))
                    # Add newly created font object to the config file
                    config.set(section, "font_"+fontname, font_object)

def get(option, card_type=None, card_name=None):
    '''
    @param ConfigParser config: Config object to pull value from
    @param str option: The option to pull the value for
    @param str card_type: If not None, will check this section for the given option.
    @param str card_name: If not None, will check this section for the given option
        before 'card_type'.

    Attempts to return the value for the given option, first from a section
        matching card_name, then from a section matching card_type, then
        from the Defaults section. If none of the sections (if they exist)
        have that option, then None is returned.

    @return str or None: None, or the value from the config
    '''
    if card_name is not None and config.has_option(card_name, option):
        return config.get(card_name, option)
    if card_type is not None and config.has_option(card_type, option):
        return config.get(card_name, option)
    if config.has_option("Defaults", option):
        return config.get("Defaults", option)
    return None

def getfont(option, card_type=None, card_name=None):
    font = get("font_"+option, card_type, card_name)
    if font is None:
        raise FontParseError("Font not found: {}|{}|{}".format(
            option, card_type, card_name
            ))
    return font

##def getimage(config, option, card_type=None, card_name=None):
##    image = get(config, option, card_type, card_name)
##    if image is None:
##        return Image.new('L', (1,1))
##    return value

def print_config():
    for section in config.sections():
        print config.items(section)

class ConfigParseError(Exception):
    pass

class FontParseError(ConfigParseError):
    pass

if __name__ == "__main__":
    raise Exception("Not a main module.")

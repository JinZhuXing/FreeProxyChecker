import configparser


# config parser
def getConfig(filename, section, option):
    # create a parser
    parser = configparser.ConfigParser()
    # read config file
    parser.read(filename)
    # get section
    value = parser.get(section, option)
    # return value
    return value

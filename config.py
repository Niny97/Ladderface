import configparser


config = configparser.ConfigParser()
config["settings"] = {"test": "1"}
if "music" not in config["settings"]:
    config["settings"] = {"music": "on"}
if "sfx" not in config["settings"]:
    config["settings"] = {"sfx": "on"}

if not config.has_section("level1"):
    config["level1"] = {"1": "0", "2": "0", "3": "0"}
    config["level2"] = {"1": "0", "2": "0", "3": "0"}
    config["level3"] = {"1": "0", "2": "0", "3": "0"}

    config["names1"] = {"1": "0", "2": "0", "3": "0"}
    config["names2"] = {"1": "0", "2": "0", "3": "0"}
    config["names3"] = {"1": "0", "2": "0", "3": "0"}

def before_quit():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

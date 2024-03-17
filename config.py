import configparser


config = configparser.ConfigParser()
config["settings"] = {"test": "1"}

if "music" not in config["settings"]:
    config["settings"] = {"music": "on"}
if "sfx" not in config["settings"]:
    config["settings"] = {"sfx": "on"}

if not config.has_section("level1"):
    for i in range(1, 4):
        config["level{}".format(i)] = {"1": "0", "2": "0", "3": "0"}
        config["names{}".format(i)] = {"1": "0", "2": "0", "3": "0"}


def before_quit():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

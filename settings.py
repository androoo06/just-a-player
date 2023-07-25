from util import open_file, try_number

settings = {}

#### settings ####
def read_settings():
    f = open_file("data/settings.txt", "r")
    for line in f.read().splitlines():
        setting = line.split("=")
        settings[setting[0]] = try_number(setting[1])
    f.close()

def write_settings():
    f = open_file("data/settings.txt", "w")

    for setting in settings.keys():
        f.write(f"{setting}={str(settings[setting])}\n")

def change_setting(setting, value):
    final = try_number(value)
    settings[setting] = final
    #print("final val for", setting, "is", final)
    return final

### on import

read_settings()
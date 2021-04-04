import os
import configparser


CONFIGPATH = os.path.join(
    os.path.expanduser('~'),
    '.config/bandcamp_tagplayer/')

""" read or create config file """
conf = configparser.ConfigParser()


class Config:
    def __init__(self):
        self.build_dirs(CONFIGPATH)
        confvars = conf.read(os.path.join(CONFIGPATH, 'config'))
        if not confvars:
            self.create_config()
        cache_dir = self.conf_vars()['cache_dir']
        self.build_dirs(self.format_path(cache_dir))

    def conf_vars(self):
        conf_vars = {
            'cache_dir': self.format_path(conf['storage']['cache']),
            'mpd_host': conf['mpd']['host'],
            'mpd_port': conf['mpd']['port'],
            'mpd_password': conf['mpd']['password'] if conf.has_option('mpd', 'password') else '',
            'banned_genres': conf['songs']['ban_list'],
            'music_dir': self.format_path(conf['mpd']['music_dir'])
        }
        return conf_vars

    def create_config(self):
        """ Create config file """
        print("No config file found at ~/.config/bandcamp_tagplayer, using default settings. Creating file with defaults.")
        path = self.format_path(os.path.join(CONFIGPATH, 'config'))
        conf.add_section("storage")
        conf.set("storage", "cache", "~/.config/bandcamp_tagplayer/bct_cache")
        conf.add_section("mpd")
        conf.set("mpd", "host", "localhost")
        conf.set("mpd", "music_dir", "~/Music")
        conf.set("mpd", "password", "")
        conf.set("mpd", "port", "6600")
        conf.add_section("songs")
        conf.set("songs", "ban_list", "")
        with open(path, "w") as config_file:
            conf.write(config_file)

    def build_dirs(self, path):
        """ Create bandcamp_tagplayer dir and cache dir in .config """
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def format_path(self, path):
        if '~' in path:
            path = os.path.expanduser(path)
        else:
            path = path
        return path

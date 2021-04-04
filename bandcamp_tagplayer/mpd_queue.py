from blessed import Terminal
from time import sleep
from mpd import MPDClient

from .config import Config
from .utils import Utils

c = Config().conf_vars()


class MPDConn:
    def __init__(self, host, path):
        self.host = c['mpd_host']
        self.port = c['mpd_port']
        self.client = None

    def __enter__(self):
        self.client = MPDClient()
        self.client.connect(c['mpd_host'], c['mpd_port'])
        if c['mpd_password']:
            self.client.password(c['mpd_password'])
        # 0 is random off, 1 is on
        # self.client.random(0)
        return self.client

    def __exit__(self, exc_class, exc, traceback):
        self.client.close()
        self.client.disconnect()


class MPDQueue:
    def add_song(self, song):
        with MPDConn(c['mpd_host'], c['mpd_port']) as m:
            self.update_mpd()
            sleep(5)
            try:
                m.add(song)
            except:
                try:
                    sleep(2)
                    m.add(song)
                except:
                    pass

    def watch_playlist(self, tags=None, user=None):
        '''
        Check playlist every 2 seconds, if under 4 tracks, get more
        '''
        term = Terminal()
        print(term.clear)
        with MPDConn(c['mpd_host'], c['mpd_port']) as m:
            change = None
            curr_song = None
            while True:
                songs_left = self._songs_left(m)
                if songs_left <= 3 or change:
                    print(term.clear)
                    break
                else:
                    if m.status()['state'] != 'play':
                        curr_song = 'paused'
                    else:
                        song_check = m.currentsong()['file']
                        if song_check != curr_song:
                            curr_song = song_check
                            print(term.clear)
                    self._write_status(m=m, songs_left=songs_left, tags=tags, user=user)
                    sleep(2)
                change = Utils().options_menu(curr_song, change)
        return change

    def update_mpd(self):
        '''
          Update mpd so it knows of new tracks in bct cache
        '''
        rel_path = c['cache_dir'].split('/')[-1]
        with MPDConn(c['mpd_host'], c['mpd_port']) as m:
            m.update(rel_path)

    def _songs_left(self, m):
        '''
          Get the number of songs remaining in the playlist/queue regardless
          of mpd consume mode or random status.
        '''
        consume = m.status().get('consume')

        if consume == '1':
            return len(m.playlist())
        else:
            cs = m.currentsong()
            if 'pos' in cs:
                return len(m.playlistinfo(cs['pos'] + ':'))
            else:
                return len(m.playlist())

    def _write_status(self, m, songs_left, tags=None, user=None):
        '''
          Write current song (if playing), # in playlist, current search tag
          and menu to term
        '''
        cs = m.currentsong()
        pl = len(m.playlist())
        if cs != {}:
            genre = cs.get('genre', '')
            title = cs.get('title', '')
            artist = cs.get('artist', '')
        term = Terminal()
        with term.hidden_cursor():
            with term.location(0, 0):
                if tags:
                    print(f"Search tag(s): {(', ').join(tags)}")
                if user:
                    print(f"User collection: {user}")
                print(f"{pl} tracks in current playlist")
                if cs != {}:
                    print(f"\n# Current song \nartist:\t{artist}\ntitle:\t{title}\ntags:\t{genre}")
                print("\nchange [t]ags, change [u]sername, [w]ebsite, [b]an song, [B]an artist, [q]uit")

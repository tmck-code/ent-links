import os
import sys

from ent_links import tvdb, sonarr


if __name__ == '__main__':
    show_ids = sonarr.SonarrApi(os.getenv('SONARR_API_KEY')).list_shows()
    client = tvdb.TVDBApi(os.getenv('TVDB_API_KEY'))
    for n, i in enumerate(show_ids.all_tvdb_ids()):
        print(i, n)
        ac = client.get_series_actors(n)
        print(ac)

os.

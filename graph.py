#!/usr/bin/env python3
'Graphs relationships and commonalities between entertainment'

import os
import sys

from ent_links import tvdb, sonarr
# For now, generate graph for all TV

from ent_links import log
LOG = log.getLogger('graph')

if __name__ == '__main__':
    show_ids = sonarr.SonarrApi(os.getenv('SONARR_API_KEY')).list_shows()
    client = tvdb.TVDBApi(os.getenv('TVDB_API_KEY'))
    LOG.info(f'Connected to sonarr and TVDB')
    all_ids = show_ids.all_tvdb_ids()
    LOG.info(f'Found {len(all_ids)} TV ids')
    for i, n in enumerate(show_ids.all_tvdb_ids()):
        LOG.info(f'{i}: Getting series actors for {n}')
        ac = client.get_series_actors(n)
        LOG.info(ac)



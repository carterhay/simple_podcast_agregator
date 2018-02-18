#!/user/bin/python3

import sys
import urllib
import feedparser
import yaml
import time
from glob import glob


def get_config(directory):
    with open(directory + '/.config', 'r') as f:
        return yaml.load(f)


# Config is a map. This should run in O(n) where n is number of manditory_options.
def is_valid(config):
    manditory_options = ['rss_url', 'download_amount']
    for option in manditory_options:
        if option not in config:
            return False
    return True


def get_audio_link(links):
    for link in links:
        if 'audio' in link['type'] or 'video' in link['type']:
            return link['href']


def download_audio(url, path):
    # urllib.request.urlretrieve is legacy. Consider replacing this bit
    urllib.request.urlretrieve(url, path)


def get_time_code(t):
    t = time.struct_time(t)
    return str(t.tm_year) + '_' + str(t.tm_mon) + '_' + str(t.tm_mday)


def main():
    if len(sys.argv) > 1:
        subdirs = ['./' + sys.argv[1] + '/']
    else:
        subdirs = glob("./*/")

    for directory in subdirs:
        try:
            config = get_config(directory)
        except FileNotFoundError:
            print('"' + directory + '.config" not found. Skipping', file=sys.stderr)
            continue

        if not is_valid(config):
            print('Error in file "' + directory + '.config". Skipping.', file=sys.stderr)
            continue

        feed = feedparser.parse(config['rss_url'])
        if feed['bozo']:
            print('Malformed XML in rss file. Skipping.', file=sys.stderr)
            continue

        download_amount = int(config['download_amount'])

        files = glob(directory + '/[!.]*')
        if len(files):
            for entry in feed['entries']:
                time_code = get_time_code(entry['published_parsed'])
                file_name = directory + time_code + ' ' + entry['title']
                if file_name in files:
                    break
                else:
                    download_audio(get_audio_link(entry['links'], file_name))
                
        else:
            # Download only the download_amount if download_amount is not 0, else download all entries.
            # List is iterated in reverse order in order to allow for easy resume if download is interrupted.
            for entry in (feed['entries'][:download_amount] if download_amount else feed['entries'])[::-1]:
                time_code = get_time_code(entry['published_parsed'])
                print('Downloading: ' + entry['title'])
                download_audio(get_audio_link(entry['links']), directory + time_code + ' ' + entry['title'])


if __name__ == "__main__":
    main()

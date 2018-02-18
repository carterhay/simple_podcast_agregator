# simple_podcast_agregator
Just a simple podcast agregator script for my personal use.

## Setup

reader.py requires the following libraries:
- feedparser

Both the python script, and all podcast directories were designed to live inside of another directory.
A directory structure similar to the following is assumed.

- [Podcasts]
    - reader.py
    - [Title Of Podcast]
        - .config
        - [Podcast audio / video files]

Follow the following steps to get started using:

- Create a Podcast folder
- Create a .config file inside the newly created Podcast folder, following the format in .config_example


## Running

- Run reader.py with no arguments for it to parse every subdir for a podcast **.config** directory
- Run reader.py [Directory] for reader to only parse and update the provided subdir.


## Notes

- reader.py must be run with python3
- This has only been tested to work under linux, and with a select number of podcast RSS feeds

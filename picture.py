from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os

DOWNLOAD_DIR = "downloaded"

def create_jpgfile(video_id, image):
    """Create a video_id.jpg file in DOWNLOAD_DIR/ directory
    Args:
        video_id (str): Youtube video id
        image (bytes): video image extracted from urlopen
    """
    file = open("./%s/%s.jpg" % (DOWNLOAD_DIR, video_id), "wb")
    file.write(image)
    file.close()

def extract_image(video_id):
    """Download video image from youtube
    Args:
        video_id (str): Youtube video id
    Example:
        extract_image("AY-aG_Ki-r0")
    Returns:
        bytes formatted image
    """
    try:
        return urlopen("https://img.youtube.com/vi/%s/maxresdefault.jpg" % video_id).read()
    except HTTPError:
        return urlopen("https://img.youtube.com/vi/%s/hqdefault.jpg" % video_id).read()

def extract_id(yt_url):
    """RegExp covering all youtube video urls
    Args:
        yt_url (str): A youtube video url
    Returns:
        (str): A youtube video id
    Example:
        extract_id("www.youtube.com/v/MkTD2Y4XcM")
        extract_id("www.youtube.com?v=MkTD2Y4XcM")
        extract_id("http://www.youtube.com/watch?v=MkTD2Y4XcM&feature=youtu.be")
        extract_id("http://www.youtube.com/watch?v=MkTD2Y4XcM")
        extract_id("youtu.be/MkTD2Y4XcM")
        extract_id("http://www.youtube.com/watch?feature=player_detailpage&v=MkTD2Y4XcM#t=31s")
    """
    m = re.search(r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", yt_url)
    if m:
        return m.group(4)
    return False

def fetch_channel_videos(channel_url):
    """Fetch all youtube videos urls the channel has uploaded
    Args:
        channel_url (str): A youtube channel url
    Returns:
        A list of (str) url
    Example:
        fetch_channel_videos("www.youtube.com/channel/UCPRLhjrtiV8t2GZYmJn79ag")
        fetch_channel_videos("www.youtube.com/channel/UCPRLhjrtiV8t2GZYmJn79ag/videos")
    """
    channel_url = "https://www.youtube.com/channel/%s/videos" % channel_url.split('/')[4]
    channel_html = urlopen(channel_url).read()
    soup = BeautifulSoup(channel_html, 'html.parser')
    urls = []

    tiles = soup.find_all('a', { "class" : "yt-uix-tile-link" } )
    for tile in tiles:
        if 'href' in tile.attrs:
            urls.append(tile['href'])
    return urls

def parse_input():
    """Fetch all youtube videos urls in user-input string and extract video id with RegExp
    If the user inputs a channel url, fetch all urls from the channel
    Returns:
        A list of (str) video ids
    """
    urls_input = input("Entrer le lien d'une chaine youtube ou des liens youtube séparés par une virgule (,) : \n").split(',')
    first_url = urls_input[0]

    if first_url.split('/')[3] == 'channel':
        urls = fetch_channel_videos(first_url)
    else:
        urls = urls_input
    return map(extract_id, urls)



def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    video_ids = parse_input()

    for video_id in video_ids:
        image = extract_image(video_id)
        create_jpgfile(video_id, image)
        print("%s done" % video_id)
    input("Fin.")

if __name__ == '__main__':
    main()

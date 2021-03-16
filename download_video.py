# python3.8
import argparse


def get_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    from urllib.parse import urlparse, parse_qs
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


def create_folder():
    from pathlib import Path
    import os
    path = Path('./videos')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def download_video(url):
    video_id = get_video_id(url)
    if video_id is None:
        return "Nothing to download"
    from pytube import YouTube
    #Get the unique video types
    video_types = set([
        streamquery.mime_type.replace("video/", "")
        for streamquery in YouTube(url).streams.filter(only_video=True)
    ])
    file_extension = input(f"Select format type {video_types}: ")
    YouTube(url).streams.filter(subtype=file_extension).first().download(
        output_path=create_folder(), filename=(video_id))
    return f"Downloaded video {video_id}.{file_extension}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '--url', help='Youtube video URL')
    args = parser.parse_args()
    print(f"The entered URL: {args.url}")
    print(download_video(args.url))


if __name__ == '__main__':
    main()
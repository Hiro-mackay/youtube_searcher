# -*- coding: utf-8 -*-

"""
from search import search
    name, id = search(keyword)

search()
    第一戻り値:video_name
    第二戻り値:video_id
    return type list
"""


from apiclient.discovery import build
from apiclient.errors import HttpError
from .youtube_data_model import YouTubeData
from functools import reduce
from copy import copy


DEVELOPER_KEY = "copy your youtube api code"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search_or(target_string, search_keyword):
    search_words = ["ベース", "bass", "ドラム", "drum"]
    result_list = [1 if i in target_string else 0 for i in search_words]
    # result_list.append(0 if search_keyword in target_string else 1)
    result = reduce(lambda x, y: x+y, result_list)
    return True if result == 0 else False


def keyword_search_reaponse(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    return youtube.search().list(
        q=options+" ギター",
        part="id,snippet",
        maxResults=50
    ).execute()


def id_search_reaponse(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    return youtube.search().list(
        part="id,snippet",
        relatedToVideoId=options,
        type="video",
        maxResults=25
    ).execute()


def youtube_api_request(options, serach_keyword):
    if serach_keyword == "keyword":
        saerch_response = keyword_search_reaponse(options)
    elif serach_keyword == "ID":
        saerch_response = id_search_reaponse(options)

    videos = []

    for saerch_result in saerch_response.get("items", []):
        if saerch_result["id"]["kind"] == "youtube#video":

            videos.append(
                {"video_id": saerch_result["id"]["videoId"],
                 "video_name": saerch_result["snippet"]["title"]})

    temp_videos_list = copy(videos)
    for video in temp_videos_list:
        if search_or(video["video_name"].lower(), options) is False:
            videos.remove(video)
    return videos


def youtube_search(keyword, search_keyword):
    try:

        return youtube_api_request(keyword, search_keyword)
    except HttpError as e:
        print("An HTTP error %d occurrede::\n%s" % (e.resp.status, e.content))

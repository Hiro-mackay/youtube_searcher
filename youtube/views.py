from django.shortcuts import render
from django.views import generic
from .youtube_search import youtube_search
from copy import copy

# Create your views here.
global_videos_list = []


def top_search(request):
    return render(request, "youtube/search.html")


def index(request):
    keyword = request.GET.get("keyword")
    global global_videos_list
    global_videos_list = youtube_search(keyword,"keyword")
    # global_search_list = search(keyword)
    # return render(request, "youtube/search_list.html", {'videos': global_search_list})

    return render(request, "youtube/search_list.html", {'videos': global_videos_list})


def detaile(request, video_id):
    video_url = "https://www.youtube.com/embed/" + video_id
    videos_list = copy(global_videos_list)
    for video in videos_list:
        if video["video_id"] == video_id:
            videos_list.remove(video)
            break
    return render(request, "youtube/detaile.html",  {"video_url": video_url, "videos":videos_list})

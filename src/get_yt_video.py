from youtubesearchpython import VideosSearch


def get_yt_video_link(query, limit=3):
    """
    Search YouTube videos based on user query.
    Returns titles and links.
    """

    try:
        videos_search = VideosSearch(query=query, limit=limit)
        result = videos_search.result()

        video_titles = []
        video_links = []

        for video in result.get('result', []):
            video_titles.append(video.get('title'))
            video_links.append(video.get('link'))

        return video_titles, video_links

    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return [], []
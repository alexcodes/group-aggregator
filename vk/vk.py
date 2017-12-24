import time
import logging

import requests

import envutil
from aggregator.group import Group
from aggregator.post import Post

ACCESS_TOKEN = envutil.get_access_token()
TARGET_GROUP = envutil.get_target_group()
MAX_REQUEST_PER_SECOND = 3
REQUEST_TIMESTAMPS = []  # newest -> oldest


def get_posts(group, count=100, offset=0):
    url = 'https://api.vk.com/method/wall.get?owner_id=-{}&count={}&offset={}&access_token={}'
    url = url.format(group.id, count, offset, ACCESS_TOKEN)

    response = execute_request(url)
    response_json = response.json()
    posts = response_json["response"]

    # filter invalid items
    posts = [post for post in posts if type(post) is not int]

    # filter ads
    posts = [post for post in posts if post["marked_as_ads"] == 0]

    posts = [Post(item["id"], item["date"], item["likes"]["count"]) for item in posts]
    return posts


def get_groups(group_ids):
    if not group_ids:
        return []

    url = 'https://api.vk.com/method/groups.getById?group_ids={}'
    url = url.format(','.join(group_ids))

    response = execute_request(url)
    response_json = response.json()

    groups = response_json["response"]
    groups = [Group(item["gid"], item["name"], item["screen_name"]) for item in groups]
    return groups


def repost(from_group, post):
    url = 'https://api.vk.com/method/wall.repost?object=wall-{}-{}&group_id={}'
    url = url.format(from_group.id, post.id, TARGET_GROUP)

    response = execute_request(url)
    logging.debug(response.text)


############################################################################################


def ensure_request_limit():
    if len(REQUEST_TIMESTAMPS) < MAX_REQUEST_PER_SECOND:
        return

    oldest = REQUEST_TIMESTAMPS[-1]
    while (time.time() - oldest) < 1.0:
        time.sleep(0.1)


def register_request():
    REQUEST_TIMESTAMPS.insert(0, time.time())
    if len(REQUEST_TIMESTAMPS) > MAX_REQUEST_PER_SECOND:
        del REQUEST_TIMESTAMPS[-1]


def execute_request(url):
    ensure_request_limit()
    response = requests.get(url, verify=False)
    register_request()
    return response

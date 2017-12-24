import logging
import time

import envutil
from aggregator.analyzer import get_threshold
from vk import vk

GROUP_LIST = vk.get_groups(envutil.get_group_list())
HOURS_WAIT = envutil.get_hours_wait()
LAST_TIMESTAMPS = {}

for item in GROUP_LIST:
    LAST_TIMESTAMPS[item.id] = int(time.time()) - HOURS_WAIT * 60 * 60


def execute():
    logging.info("=" * 20)
    for group in GROUP_LIST:
        try:
            process_group(group)
        except Exception as e:
            logging.error(e)


def process_group(group):
    logging.info("Process group %s", group.name)
    posts = fetch_stable_posts(group)
    logging.debug("Fetched %s posts", str(len(posts)))

    like_array = [post.likes for post in posts]
    like_threshold = get_threshold(like_array)
    logging.debug("Threshold: %s", str(like_threshold))
    filtered_posts = [post for post in posts if post.likes > like_threshold]

    last_timestamp = LAST_TIMESTAMPS[group.id]
    if not last_timestamp:
        raise RuntimeError("Cannot find last_timestamp: id" + str(group.id))

    actual_posts = [post for post in filtered_posts if post.date > last_timestamp]
    if actual_posts:
        update_last_timestamp(group, actual_posts)
        for post in actual_posts:
            logging.info("Repost %s", post.id)
            vk.repost(group, post)


def update_last_timestamp(group, posts):
    last_timestamp = max([post.date for post in posts])
    LAST_TIMESTAMPS[group.id] = last_timestamp


def fetch_stable_posts(group):
    all_posts = vk.get_posts(group)

    now = int(time.time())
    filtered_posts = [post for post in all_posts if post.date < now - (HOURS_WAIT * 60 * 60)]
    return filtered_posts

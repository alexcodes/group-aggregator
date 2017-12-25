import os


def get_update_frequency_sec():
    env = os.getenv("VK_UPDATE_FREQUENCY_SEC", 60)
    check_not_null(env, "VK update frequency not defined")
    return int(env)


def get_access_token():
    env = os.getenv("VK_ACCESSTOKEN")
    check_not_null(env, "VK access token not defined")
    return env


def get_service_key():
    env = os.getenv("VK_SERVICEKEY")
    check_not_null(env, "VK service key not defined")
    return env


def get_group_list():
    env = os.getenv("VK_GROUPS")
    check_not_null(env, "VK group list not defined")
    return get_comma_separated_list(env)


def get_target_group():
    env = os.getenv("VK_TARGET_GROUP")
    check_not_null(env, "VK target group not defined")
    return env


def get_hours_wait():
    env = os.getenv("VK_HOURS_WAIT", 10)
    return int(env)


def check_not_null(env, error_message):
    if not env:
        raise RuntimeError(error_message)


def get_comma_separated_list(line):
    arr = line.strip().split(",")
    if not arr:
        raise RuntimeError("Cannot parse comma separated list: " + str(line))
    return arr

import logging

import sched
import time
import urllib3

from aggregator import searcher
import envutil


def init_logging():
    # configure project logging
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)-7s - %(message)s', level=logging.INFO)
    logging.info("Start VK_GROUP_AGGREGATOR")

    # configure libraries logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    init_logging()

    scheduler = sched.scheduler(time.time, time.sleep)
    priority = 1
    delay = envutil.get_update_frequency_sec()

    def repeat():
        searcher.execute()
        scheduler.enter(delay, priority, repeat)

    try:
        scheduler.enter(0, priority, repeat)
        scheduler.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()

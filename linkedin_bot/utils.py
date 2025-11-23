import re
import time
import random

def human_delay(a=1, b=3):
    time.sleep(random.uniform(a, b))


def parse_days_ago(text):
    text = text.lower()

    if "just now" in text or "hour" in text:
        return 0

    # Match numbers like "3 days ago" or "1 week ago"
    match = re.search(r"(\d+)", text)
    if not match:
        return 999  # Unknown → skip

    num = int(match.group(1))

    if "day" in text:
        return num
    if "week" in text:
        return num * 7
    if "month" in text:
        return num * 30

    return 999
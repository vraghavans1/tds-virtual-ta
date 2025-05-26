import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = f"{BASE_URL}/c/courses/tools-in-data-science/56.json"
POSTS = []

def scrape_all():
    res = requests.get(CATEGORY_URL).json()
    topic_ids = [t["id"] for t in res["topic_list"]["topics"]]

    for tid in tqdm(topic_ids):
        post_url = f"{BASE_URL}/t/{tid}.json"
        try:
            post = requests.get(post_url).json()
            POSTS.append({
                "title": post.get("title", ""),
                "body": post["post_stream"]["posts"][0]["cooked"],
                "url": BASE_URL + post["slug"]
            })
        except:
            continue

    with open("data/discourse.json", "w") as f:
        json.dump(POSTS, f, indent=2)

if __name__ == "__main__":
    scrape_all()


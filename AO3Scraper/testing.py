import requests
from bs4 import BeautifulSoup

url = "https://archiveofourown.org/tags/Sherlock%20(TV)/works?page=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}
res = requests.get(url, headers=headers)
print("Status code:", res.status_code)
soup = BeautifulSoup(res.text, "lxml")
works = soup.select("li.work.blurb.group")
print("Number of works found:", len(works))

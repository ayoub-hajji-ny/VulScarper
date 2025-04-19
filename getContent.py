import requests
from bs4 import BeautifulSoup

url = "https://ubuntu.com/security/notices"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    with open('html.txt', 'a') as f:
        f.write(soup.prettify())
        f.write('exit')
else:
    print(f"Failed to fetch page: {response.status_code}")

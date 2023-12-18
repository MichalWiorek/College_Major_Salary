from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"

response = requests.get(url=url)
response.raise_for_status()
site_text = response.text
soup = BeautifulSoup(site_text, "html.parser")

paginator = soup.select(selector="div.pagination.csr-gridpage__pagination a")
total_pages = int(paginator[-2].text)


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


table = soup.select(selector="table.data-table tbody tr")
headers = [element.select_one(selector="span.data-table__title").text[:-1] for element in table[0]]

all_values = []
for i in range(1, total_pages+1):
    response = requests.get(url=url+f"/page/{i}")
    response.raise_for_status()
    site_text = response.text
    soup = BeautifulSoup(site_text, "html.parser")
    table = soup.select(selector="table.data-table tbody tr")
    for row in table:
        values = []
        for element in row:
            value = element.select_one(selector="span.data-table__value")
            if value.text.strip("$") != value.text:
                values.append(int(value.text.strip("$").replace(",", "")))
            else:
                values.append(value.text)
        all_values.append(values)
        # print(values)

df = pd.DataFrame(data=all_values, columns=headers)
clean_df = df.dropna()
# print(clean_df.info())

import unittest
import bs4
import pandas as pd
import requests

class TestMyProgram(unittest.TestCase):
    def test_showbtn(self):
        url = "https://radioaktywnosc-pomiary.umcs.lublin.pl/wykresy_front/wykresy_podstawowe/wykresy.php"
        page = requests.get(url)

        soup = bs4.BeautifulSoup(page.content, "lxml")

        results = soup.find("h4")
        contamination = soup.find("div", class_="success-msg")
        table = soup.find("div", class_="tableMoc")

        historical_results = results.text
        historical_constamination = contamination.text
        historical_table = pd.read_html(str(table))
        historical_table = historical_table[0]
        print(historical_results)
        print(historical_constamination)
        print(historical_table)


if __name__ == '__main__':
    unittest.main()

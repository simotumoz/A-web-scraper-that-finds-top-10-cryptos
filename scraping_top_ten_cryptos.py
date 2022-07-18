from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
from datetime import datetime

url = 'https://coinmarketcap.com/'


def run_scraping():
    result = requests.get(url).text
    doc = BeautifulSoup(result, 'html.parser')

    tbody = doc.tbody
    trs = tbody.contents

    prices = {}

    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        fixed_name = name.p.string
        fixed_price = price.a.string

        prices[fixed_name] = fixed_price

    print(prices)
    return prices


def print_on_pdf(prices: dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=20)
    pdf.cell(200, 10, txt="Top Ten Cryptocurrencies", ln=1, align='C')
    pdf.set_font('Arial', size=14)
    pdf.cell(200, 10, txt=" ", ln=1, align='C')
    for p, n in prices.items():
        text = "> " + str(p) + " : " + str(n)
        pdf.cell(200, 10, txt=text, ln=1, align='C')

    pdf.cell(200, 10, txt=" ", ln=1, align='C')
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    pdf_footer = "Data taken from " + str(url) + " at " + str(t)
    pdf.cell(200, 10, txt=pdf_footer, ln=1, align='C')
    pdf.output('top_ten_cryptocurrencies.pdf')


print_on_pdf(run_scraping())

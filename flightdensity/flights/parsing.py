from bs4 import BeautifulSoup
import time
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from flights.models import Flights, Companies


def delete_spaces(s: str):
    return " ".join(s.split())


def save_tolmachovo_tables(destination="saved pages", name='page'):
    urltosave = 'https://tolmachevo.ru/passengers/information/timetable'
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # linux only
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(urltosave)
    element = WebDriverWait(driver, timeout=20, poll_frequency=1) \
        .until(lambda d: d.find_element(By.XPATH,
                                        "/html/body/div[3]/div[3]/section/div/div/section/header/div[2]/span[3]"))
    with open(destination + "/" + name + ".html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    element.click()

    time.sleep(1)  # ПЕРЕДЕЛАТЬ ПОЗЖЕ НА АСИНХРОНКУ

    with open(destination + "/" + name + "_tomorrow.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    driver.quit()


def write_in_db(fnumber: str, shtime: str, shdate: str, etatime: str, etadate: str,
                airport: str, isdep: bool, ftype: str, company: str):
    shdate = dt.date(dt.date.today().year, month=int(shdate.split(".", 1)[1]), day=int(shdate.split(".", 1)[0]))
    shtime = dt.time(int(shtime.split(":", 1)[0]), int(shtime.split(":", 1)[1]))

    etadate = dt.date(dt.date.today().year, month=int(etadate.split(".", 1)[1]), day=int(etadate.split(".", 1)[0]))
    etatime = dt.time(int(etatime.split(":", 1)[0]), int(etatime.split(":", 1)[1]))

    exist_flight, is_created = Flights.objects.update_or_create(
        number=fnumber, sh_time=shtime, sh_date=shdate,
        defaults={'number': fnumber,
                  'sh_time': shtime,
                  'sh_date': shdate,
                  'eta_time': etatime,
                  'eta_date': etadate,
                  'airport_iata': airport,
                  'is_depart': isdep,
                  'plane_type': ftype,
                  'company': company}
    )
    if not is_created:
        Companies.objects.get_or_create(name=company)

def parse_saved_tolmachovo_html(target="saved pages/page.html"):
    html_file = open(target, "r")
    index = html_file.read()
    parse = BeautifulSoup(index, 'lxml')

    for flight in parse.find_all('article', class_='flight-item'):
        is_dep = False
        number, s_time, s_date, e_time, e_date, airtype, company = ['' for _ in range(7)]
        flightdata = [i.text.lower() for i in list(flight.find_all("li"))]
        for item in flightdata:
            itemtitle, itemdata = item.split(":", 1)
            if "расчетное время" in itemtitle:
                e_time, e_date = itemdata.split(",", 1)
                e_time = delete_spaces(e_time)
                e_date = delete_spaces(e_date)
            elif "посадка" in itemtitle:
                is_dep = True
            elif "тип ВС" in itemtitle:
                airtype = delete_spaces(itemdata)
            elif "по расписанию" in itemtitle:
                s_time, s_date = itemdata.split(",", 1)
                s_time = delete_spaces(s_time)
                s_date = delete_spaces(s_date)
            elif "номер рейса" in itemtitle:
                number = delete_spaces(itemdata)
            elif "компания" in itemtitle:
                company = delete_spaces(itemdata)
        write_in_db(fnumber=number, shtime=s_time, shdate=s_date, etatime=e_time, etadate=e_date, airport='obv',
                    isdep=is_dep, ftype=airtype, company=company)

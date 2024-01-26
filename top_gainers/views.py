import time
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import requests

from .models import Company, CompanyDetail

URL = 'https://nepalstock.com/'

def index(request):
    companies_per_page = 10
    companies_list = Company.objects.all()
    paginator = Paginator(companies_list, companies_per_page)
    page = request.GET.get('page')

    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page
        companies = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page
        companies = paginator.page(paginator.num_pages)

    context = {
        "companies": companies,
        "last_updated_date": companies_list.last().added if companies_list.last() else None
    }
    return render(request, 'top_gainers/index.html', context=context)

def refresh_data(request):
    Company.objects.all().delete()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    
    try:
        with webdriver.Edge() as driver:
            driver.get(URL)

            view_more_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tab__viewmore"))
            )
            view_more_btn.click()
            while True:
                # Switch to the modal context
                modal = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-content"]'))
                )

                table = modal.find_element(By.XPATH, '//table[@class="table table__lg table-striped"]')
                table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

                tbody = table_soup.find('tbody')
                rows = tbody.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    
                    # Check if the record exists in the database
                    try:
                        company = Company.objects.get(symbol=columns[0].get_text(strip=True))
                    except Company.DoesNotExist:
                        # If the record doesn't exist, create a new record
                        company = Company.objects.create(
                            symbol=columns[0].get_text(strip=True),
                            LTP=columns[1].get_text(strip=True),
                            pt_change=columns[2].get_text(strip=True),
                            percentage_change=columns[3].get_text(strip=True),
                        )

                # Click the "Next" button to go to the next page
                next_button = modal.find_element(By.XPATH, '//a[@aria-label="Next page"]')
                next_button.click()

                # Add a delay after clicking the "Next" button
                # time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    return redirect('index')


def get_stock_detail(request):
    url = "https://nepalstock.com/company/detail/2807"
    
    # initializing web driver 
    driver = webdriver.Edge()
    driver.get(url)

    # getting the container that contains company's name and other data
    container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "company"))
    )

    # getting the table that contains company's share details
    table = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'table'))
                )
    
    # parsing table and company detail container with beatiful soup to access their children elements
    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
    company_detail_container_soup = BeautifulSoup(container.get_attribute('outerHTML'), 'html.parser')

    # initializing a empty dictonary to store company data
    data_dict = {}
    company_name = company_detail_container_soup.find('h1').get_text(strip=True)        # company name
    data_dict['company_name'] = company_name
    company_meta = company_detail_container_soup.findAll('li')[1:]                      # company details
    data_dict['company_meta'] = []
    for li in company_meta:
        meta = li.find('strong').get_text(strip=True)
        data_dict['company_meta'].append(meta)

    tbody = table_soup.find('tbody')
    rows = tbody.find_all('tr')[1:-1]
    for row in rows:
        th_text = row.find('th').get_text(strip=True).lower().replace(" ", "_")
        td_text = row.find('td').get_text(strip=True)
        data_dict[th_text] = td_text
    print(data_dict)
    # saving to database or updating fields if already exists
    try:
        company_detail = CompanyDetail.objects.get(name__iexact=data_dict['company_name'])
    except CompanyDetail.DoesNotExist:
        company_detail = CompanyDetail()
        company_detail.name = data_dict['company_name']
        company_detail.email = data_dict['company_meta'][0]
        company_detail.sector = data_dict['company_meta'][1]
        company_detail.permitted_to_trade = data_dict['company_meta'][2]
        company_detail.status = data_dict['company_meta'][3]
        company_detail.instrument_type = data_dict['instrument_type']
        company_detail.listing_date = data_dict['listing_date']
        company_detail.last_traded_price = data_dict['last_traded_price']
        company_detail.total_traded_quantity = data_dict['total_traded_quantity']
        company_detail.total_trades = data_dict['total_trades']
        company_detail.previous_day_close_price = data_dict['previous_day_close_price']
        company_detail.high_low_price = data_dict['high_price_/_low_price']
        company_detail.week_high_low = data_dict['52_week_high_/_52_week_low']
        company_detail.open_price = data_dict['open_price']
        company_detail.close_price = data_dict['close_price*']
        company_detail.total_paid_up_value = data_dict['total_paid_up_value']
        company_detail.market_capitalization = data_dict['market_capitalization']
        company_detail.table_listed_shares = data_dict['total_listed_shares']
        company_detail.save()
    else:
        company_detail.name = data_dict['company_name']
        company_detail.email = data_dict['company_meta'][0]
        company_detail.sector = data_dict['company_meta'][1]
        company_detail.permitted_to_trade = data_dict['company_meta'][2]
        company_detail.status = data_dict['company_meta'][3]
        company_detail.instrument_type = data_dict['instrument_type']
        company_detail.listing_date = data_dict['listing_date']
        company_detail.last_traded_price = data_dict['last_traded_price']
        company_detail.total_traded_quantity = data_dict['total_traded_quantity']
        company_detail.total_trades = data_dict['total_trades']
        company_detail.previous_day_close_price = data_dict['previous_day_close_price']
        company_detail.high_low_price = data_dict['high_price_/_low_price']
        company_detail.week_high_low = data_dict['52_week_high_/_52_week_low']
        company_detail.open_price = data_dict['open_price']
        company_detail.close_price = data_dict['close_price*']
        company_detail.total_paid_up_value = data_dict['total_paid_up_value']
        company_detail.market_capitalization = data_dict['market_capitalization']
        company_detail.table_listed_shares = data_dict['total_listed_shares']
        company_detail.save()
    
    return render(request, 'top_gainers/detail.html', context={'company': company_detail})

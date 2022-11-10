from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

START_ID = 'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate1_txtDatePicker'
END_ID =   'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate2_txtDatePicker'
BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_btSearch'
START_DATE = '1/1/2018'
END_DATE = '29/8/2022'

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.headless = True
# create a web driver
driver = webdriver.Chrome(options=options)

# retrieve tickers name
with open('ticker_name.txt', 'r') as f:
    tickers = [s.strip('\n') for s in f.readlines()]

unsuccess = []

for ticker in tickers:
    content = []
    allow_write = True
    URL = f'https://s.cafef.vn/Lich-su-giao-dich-{ticker}-1.chn'
    filename = f'./data/{ticker}.csv'
    
    # check if already scraped
    if os.path.exists(filename):
        print(f'already scraped {ticker}')
        continue
    
    try:
        # open the page
        driver.get(URL)
    except:
        print(f'some problem happened to {ticker}')
        unsuccess.append(ticker)
        continue
    
    # select the start + end dates
    start = driver.find_element(By.ID, START_ID)
    end = driver.find_element(By.ID, END_ID)
    btn = driver.find_element(By.ID, BTN_ID)

    start.send_keys(START_DATE)
    end.send_keys(END_DATE)
    btn.click()
    
    # loop over the pages
    while True:
        # avoid staleness exception
        try:
            try:
                WebDriverWait(driver, 5).until(EC.staleness_of(driver.find_element(By.ID, 'GirdTable2')))
            except:
                WebDriverWait(driver, 5).until(EC.staleness_of(driver.find_element(By.ID, 'GirdTable')))
        except:
            print('unexpected table ID in selenium')
            allow_write = False
            unsuccess.append(ticker)
            break
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        try:        
            try:
                table_tag = soup.find('table', {'id' : 'GirdTable2'})
            except:
                table_tag = soup.find('table', {'id' : 'GirdTable'}) 
        except:
            print('unexpected table ID in bs4')
            allow_write = False
            unsuccess.append(ticker)
            break
        
        try:
            row_tags = table_tag.find('tbody').find_all('tr')
            for row_tag in row_tags[2:]:
                data_tags = row_tag.find_all('td')
                row = [data_tag.text.replace(',', '').replace('\xa0', '') for data_tag in data_tags[:-3]]
                
                # remove the unwanted elements
                row = row[:3] + row[5:]
                # convert the string to float
                data = ','.join(row)
                
                # store data
                content.append(data)
        except:
            print(f'some problem happened to {ticker}')
            unsuccess.append(ticker)
            allow_write = False
            break
            
        # press the next button
        try:
            next_page_button = driver.find_element(By.CLASS_NAME, 'CafeF_Paging').find_element(By.LINK_TEXT, '>')
            next_page_button.click()
        except:
            break
    
    
    # write data to csv file
    if not allow_write:
        continue
    
    # debug msg
    print(f'done scraping {ticker} data >>>>>')
    
    with open(filename, 'w') as f: 
        for line in content:
            f.write(line + '\n')

print('cannot open these stocks:', unsuccess)
driver.quit()



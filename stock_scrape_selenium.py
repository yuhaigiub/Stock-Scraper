from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

START_ID = 'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate1_txtDatePicker'
END_ID =   'ctl00_ContentPlaceHolder1_ctl03_dpkTradeDate2_txtDatePicker'
BTN_ID = 'ctl00_ContentPlaceHolder1_ctl03_btSearch'
START_DATE = '01/01/2018'
END_DATE = '29/8/2022'

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.headless = True
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
    
    # open the page
    driver.get(URL)
    
    # select the start + end dates
    start = driver.find_element(By.ID, START_ID)
    end = driver.find_element(By.ID, END_ID)
    btn = driver.find_element(By.ID, BTN_ID)

    start.send_keys(START_DATE)
    end.send_keys(END_DATE)
    btn.click()
    
    while True:
        try:
            try: 
                WebDriverWait(driver, 30).until(EC.staleness_of(driver.find_element(By.ID, 'GirdTable2')))
                table_tag = driver.find_element(By.ID, 'GirdTable2')
            except:
                print(f'No GirdTable2 in {ticker}')
                allow_write = False
                unsuccess.append(ticker)
                break
            tr_tags = table_tag.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for tr_tag in tr_tags[2:]:
                td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
                row = [td_tag.text.replace(',', '').replace('\xa0', '') for td_tag in td_tags]
                
                # remove the unwanted elements
                row = row[:3] + row[6:]
                row.pop(-4)
                
                # convert the string to float
                data = ','.join(row)
                
                # store data
                content.append(data)
        except:
            print(f'Unkwon error in {ticker}')
            allow_write = False
            unsuccess.append(ticker)
            break
            
        # press the next button
        try:
            next_page_button = driver.find_element(By.CLASS_NAME, 'CafeF_Paging').find_element(By.LINK_TEXT, '>')
            next_page_button.click()
            # print(f'{ticker} swap page')
        except:
            break
            
    if not allow_write:
        continue
    print(f'done scraping {ticker} data >>>>>')
    with open(filename, 'w') as f:
        for line in content:
            f.write(line + '\n')

print('cannot open these stocks:', unsuccess)
driver.quit()
#imports
from selenium import webdriver
from bs4 import BeautifulSoup
import pyautogui 
import numpy as np
import pandas as pd
import time
import random
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#building lists
address_list = []
city_list = []
link_list = []
price_list = []
dom_list = []
comp_list = []
ratio_list = []
school_list = []

#selenium setup
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
# ua = UserAgent()
# userAgent = ua.random
# options.add_argument(f"user-agent={userAgent}")
driver = webdriver.Chrome(options=options)

print('beginning scrape')
today = time.strftime('%d-%m-%Y')
site_login = "https://siteloginplaceholder.com/"
driver.get(site_login)

login = driver.find_element_by_xpath("//input[@name='username']").send_keys('email')
password = driver.find_element_by_xpath("//input[@type='password']").send_keys('password')
submit = driver.find_element_by_xpath("//button[@type='submit']").click()

try:
    check_for_proceed = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='Proceed']"))
    )
        
    proceed = driver.find_element_by_xpath("//div[text()='Proceed']").click()
except:
    pass

element_1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='react-autosuggest__container']"))
    )

#prompt to enter city/zip code to search
LOCATION = pyautogui.prompt('Enter a City or Zip Code to scrape')

search = driver.find_element_by_xpath("//input").send_keys(LOCATION)

wait_to_enter = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "react-autowhatever-1--item-0"))
    )

#enter search results page
enter = driver.find_element_by_id('react-autowhatever-1--item-0').click()

#filter by MLS
MLS_button = "//button[@title='MLS']"
wait_to_click = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, MLS_button))
    )

filter_by_MLS = driver.find_element_by_xpath(MLS_button).click()
filter_by_MLS

#filter out rentals and only see residential props
filter_xpath = "//div[text()='Filter']"
filter_button = driver.find_element_by_xpath(filter_xpath).click()
minimum_listing_price = 15000

click_MLS_status_xpath = "//span[contains(text(),'MLS Status')]"
click_MLS = driver.find_element_by_xpath(click_MLS_status_xpath).click()
minimum_input = driver.find_element_by_name('mlsListingAmountMin').send_keys(minimum_listing_price)

MLS_status_option_xpath = "//div[text() = 'MLS Status']/following-sibling::div"
click_MLS_status_option_xpath = driver.find_element_by_xpath(MLS_status_option_xpath).click()
active_listings_xpath = "//span[text() = 'Active']"
click_active = driver.find_element_by_xpath(active_listings_xpath).click()
# if Ohad wants to use the failed listings as well
# failed_listings_xpath = "//span[contains(text(), 'Fail']"
# click_failed_listings = driver.find_element_by_xpath(failed_listings_xpath).click()

prop_characteristics_xpath = "//span[contains(text(),'Characteristics')]"
click_prop_characteristics = driver.find_element_by_xpath(prop_characteristics_xpath).click()
prop_classification_input_xpath = "//div[text()='All Classifications']"
click_prop_classification_input = driver.find_element_by_xpath(prop_classification_input_xpath).click()
residential_xpath = prop_classification_input_xpath + "/parent::div/preceding-sibling::div[1]/descendant::span[text()='Residential']"
click_residential = driver.find_element_by_xpath(residential_xpath).click()

filter_button = driver.find_element_by_xpath(filter_xpath).click()

#check for listings
try: 
    unique_properties_xpath = "//div[text()='Unique Properties']"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, unique_properties_xpath))
    )
except:
    driver.quit()
    sys.exit("No Listings for this area")

properties = driver.find_element_by_xpath(unique_properties_xpath).text
number_of_properties = int(properties.split()[2].replace('(','').replace(')',''))
print(number_of_properties)

if number_of_properties < 51:
    number_of_pages = 1
else:
    pages_xpath = "//span[contains(text(),'Page')]/following-sibling::span[1]"
    wait_for_pages = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, pages_xpath))
        )

    pages = driver.find_element_by_xpath(pages_xpath).text
    number_of_pages = [int(s) for s in pages.split() if s.isdigit()][0]

for page in range(number_of_pages):
# for page in range(1):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, unique_properties_xpath))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings_xpath = unique_properties_xpath + "/parent::div/parent::div/following-sibling::div[1]/child::div[1]/child::div"
    listings = driver.find_elements_by_xpath(listings_xpath)

    number_of_listings = len(listings)

    cities_xpath = listings_xpath + "/child::div[3]/child::div[1]/child::div[1]/child::div[1]"
    cities =  driver.find_elements_by_xpath(cities_xpath)

    addresses_xpath = cities_xpath + '/preceding-sibling::a[1]'
    addresses = driver.find_elements_by_xpath(addresses_xpath)

    for listing in range(number_of_listings):
    # for listing in range(5):
        # print(listing)
        # print(page)
        print(page*50 + listing + 1)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # listings = soup.find_all("div", class_='_2MmYY__root')

        address = addresses[listing]
        address_text = address.text
    
        house_link = address.get_attribute('href')
        
        city = cities[listing].text

        # Open a new window
        driver.execute_script("window.open('');")
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[1])

        driver.get(house_link)

        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(2)
        )

        MLS_xpath = "//div[contains(text(),'MLS') and contains(text(), 'Details')]"

        try:
            wait_for_listing_page = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, MLS_xpath))
            )
            #go to MLS page once ready
            MLS_details_class = driver.find_element_by_xpath(MLS_xpath).click()

        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(1)
            )
            continue

        try:
            MLS_page_content = "//div[contains(text(),'Description')]"

            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, MLS_page_content))
            )

        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(1)
            )
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        listing_price_text_xpath = "//div[contains(text(),'List') and contains(text(), 'Price')]/following-sibling::div[1]"
        listing_price = driver.find_element_by_xpath(listing_price_text_xpath).text

        days_on_market_text_xpath = listing_price_text_xpath + "/parent::div/parent::div/parent::div/descendant::div[contains(text(),'Days') and contains(text(), 'Market')]/following-sibling::div[1]"
        days_on_market = driver.find_element_by_xpath(days_on_market_text_xpath).text
        days_on_market_int = int(days_on_market.replace(',', ''))

        #check if MLS listing is over a year old. CURRENTLY TESTING ON 118! change to 365
        if days_on_market_int > 365:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(1)
            )
            continue

        time.sleep(random.randint(2,6))
        
        #go to comps page and wait for content
        comps_xpath = "//*[contains(text(),'Comparables & Nearby Listings')]"
        comps_button = driver.find_element_by_xpath(comps_xpath).click()

        comps_page_content = "//div[contains(text(), 'Comparable Properties')]"
        element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, comps_page_content))
        )

        #find current property type
        prop_type_xpath = "//div[text()='Property Type'][1]/following-sibling::div[1]"
        prop_type = driver.find_element_by_xpath(prop_type_xpath).text

        #identify tab we need to click
        filter_by_type_button = "//label[text()='Public Record Sale Situation']/parent::div/following-sibling::div[1]/child::div[1]/child::div[1]"
        
        wait_for_filter_button = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, filter_by_type_button))
        )

        click_filter = driver.find_element_by_xpath(filter_by_type_button).click()
        time.sleep(1)

        single_family = filter_by_type_button + "/child::div[1]/child::div[2]/child::div[1]/child::div[1]"
        condo_town = filter_by_type_button + "/child::div[1]/child::div[2]/child::div[1]/child::div[2]"
        multi_small = filter_by_type_button + "/child::div[1]/child::div[2]/child::div[1]/child::div[3]"
        multi_big = filter_by_type_button + "/child::div[1]/child::div[2]/child::div[1]/child::div[4]"
        #if else statement for each type (return clicking the correct property type)
        if prop_type == 'Single Family Residential':
            click_single = driver.find_element_by_xpath(single_family).click()
            time.sleep(2)
        elif 'Duplex' or 'Triplex' in prop_type:
            click_multi_small = driver.find_element_by_xpath(multi_small).click()
            time.sleep(2)
        elif 'Apartments' in prop_type:
            click_multi_big = driver.find_element_by_xpath(multi_big).click()
            time.sleep(2)
        elif 'Townhouse' or 'Condo' in prop_type:
            click_condo = driver.find_element_by_xpath(condo_town).click()
            time.sleep(2)
        else:
            pass

        #reparse comps page
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #restrict comps to within 20% of square footage
        # sqft_xpath = "//div[@class='R-NbA__label' and contains(text(),'SqFt')]/following-sibling::div[1]"
        # listing_sqft = driver.find_element_by_xpath(sqft_xpath).text.replace(',', '')
        # listing_sqft = float(listing_sqft)

        # lower_limit = str(int(listing_sqft * 0.8))
        # upper_limit = str(int(listing_sqft * 1.2))
        # print(lower_limit)
        # print(upper_limit)
        # min_square_feet = driver.find_element_by_name('squareFeetMin').clear()
        # min_square_feet = driver.find_element_by_name('squareFeetMin').send_keys(lower_limit)
        # max_square_feet = driver.find_element_by_name('squareFeetMax').clear()
        # max_square_feet = driver.find_element_by_name('squareFeetMax').send_keys(upper_limit)
        
        try: 
            comp_price_xpath = "//div[text()='Comparable Properties']/following-sibling::div[1]"
            wait_for_calc = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, comp_price_xpath))
            )
            comp_price = driver.find_element_by_xpath(comp_price_xpath).text
        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(1)
            )
            continue

        partitioned_string = comp_price.split(',')
        before_first_comma = partitioned_string[0]
        after_first_comma_before_second = partitioned_string[1]
        just_price = before_first_comma[18:]
        average_comp_price = before_first_comma[17:] + ',' + after_first_comma_before_second
        #just_price is used for calculating difference. avg_comp_price is used to display neatly in CSV

        #ratio calculation price over comp. If its 85% or less it is a 15% discount. 115% or more is a 15% markup
        comp = just_price + after_first_comma_before_second
        price_without_dollar = listing_price[1:].replace(',','')
        percentage = float(price_without_dollar) / float(comp)

        #only add listing if it's a deal. Could produce very very few results
        if percentage > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(1)
            )
            continue

        #check if prop was saved, and then save property if it's usable
        save_property_xpath = "//div[contains(text(), 'Save')]/parent::button"
        save_property_disabled_q = driver.find_element_by_xpath(save_property_xpath).get_property('disabled')

        if save_property_disabled_q == False:
            save_property = driver.find_element_by_xpath(save_property_xpath).click()
        else:
            pass

        try:
            # Open a new window
            driver.execute_script("window.open('');")
            # Switch to the new window
            driver.switch_to.window(driver.window_handles[2])

            #go to trulia and bs4 parse or selenium i forgot
            driver.get("https://www.greatschools.org/")

            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(3)
            )

            greatschools_search_bar = "//div[@class='search-box']/descendant::input"

            wait_for_greatschools =  WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, greatschools_search_bar))
            )

            time.sleep(1)

            #search GS with the address and city
            search_GS = driver.find_element_by_xpath(greatschools_search_bar).send_keys(address_text + ' ' + city)
            time.sleep(2)
            wait_for_suggestions = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'search-results-list'))
            )
            submit_GS = driver.find_element_by_xpath("//button[@type = 'submit']").click()

            try:
                wait_for_gs_listing = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, 'search-page'))
                )
                #move rest of GS code inside this try block

                school_tags = driver.find_elements_by_css_selector("div[class^='circle-rating']")
                school_ratings = []
                num_schools = len(school_tags)

                #if 3 or more grab 3, elseif over 0, grab range, else break
                
                #if 3 or more grab 3, elseif over 0, grab range, else break
                if num_schools > 2:
                    for tag in range(3):
                        school_rating = int(school_tags[tag].text[:1])
                        school_ratings.append(school_rating)
                elif num_schools > 0:
                    for tag in range(num_schools):
                        school_rating = int(school_tags[tag].text[:1])
                        school_ratings.append(school_rating)
                else:
                    pass

                if num_schools > 0:
                    avg_school_rating = np.mean(school_ratings)
                    avg_school_rating = round(avg_school_rating, 2)
                    clear_list = school_ratings.clear()
                else:
                    avg_school_rating = 'None Found'

                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 10).until(
                    EC.number_of_windows_to_be(2)
                )

            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 10).until(
                    EC.number_of_windows_to_be(2)
                )
                continue
        except:
            avg_school_rating = 'None Found'

        # percentage = (percentage - 1) * 100
        percentage = (percentage - 1)
        new_percentage = format(percentage, "%")

        print(address_text)
        print(city)
        print(house_link)
        print(listing_price)
        print(days_on_market)
        print(average_comp_price)
        print(new_percentage)
        print(avg_school_rating)

        address_list.append(address_text)
        city_list.append(city)
        link_list.append(house_link)
        price_list.append(listing_price)
        dom_list.append(days_on_market)
        comp_list.append(average_comp_price)
        ratio_list.append(percentage)
        school_list.append(avg_school_rating)

        school_ratings.clear()

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(1)
        )
    
    #go to the next page
    if number_of_pages == 1:
        break
    else:
        next_page_xpath = "//span[text()='Next']/parent::button"
        next_page_disabled_q = driver.find_element_by_xpath(next_page_xpath).get_property('disabled')

        #if button is ENABLED, click. if disabled, break and start CSV
        if next_page_disabled_q == False:
            next_page = driver.find_element_by_xpath(next_page_xpath).click()
        else:
            break

#pandas dataframe
df = pd.DataFrame({
'Address': address_list,
'City': city_list,
'Listing_price': price_list,
'Days_on_market': dom_list,
'Avg_comparable_price': comp_list,
'Percentage_of_comp': ratio_list,
'School_Rating': school_list,
'link': link_list,
})

df_sorted = df.sort_values(by = ['Percentage_of_comp'])

df_sorted['Percentage_of_comp'] = df_sorted['Percentage_of_comp'].astype(float).map("{:.2%}".format)

# df_sorted = df_sorted.style.format({'Percentage_of_comp': "{:.2%}"})

#add dataframe to csv file named '[location].csv'
path='C:\\myscraperpath'

df_sorted.to_csv(path + LOCATION + ' ' + today + '.csv', index = False)    

driver.quit()
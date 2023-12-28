from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()
driver.maximize_window()

from_date = "2024-01-27"  # YEAR-MONTH-DAY
to_date = "2024-02-03"  # YEAR-MONTH-DAY
from_airport = "MAN" #### AIRPORT CODE (MAN = MANCHESTER, LHE = LAHORE, AND SO FORTH)
to_airport = "LHE"  # SAME AS ABOVE

url = f"https://www.kayak.co.uk/flights/{from_airport}-{to_airport}/{from_date}/{to_date}?sort=bestflight_a"

driver.get(url)
sleep(5)

cookie_wala = driver.find_element(By.XPATH, '//*[@id="portal-container"]/div/div[2]/div/div/div[2]/div/div[1]/button/div/div')
cookie_wala.click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
flight_elements = soup.find_all('div', class_='nrc6')


flight_data = []

# Loop through each flight element and extract the desired information
for element in flight_elements:
    price = element.find('div', class_='f8F1-price-text').text.strip()
    time_info = element.find('div', class_='vmXl-mod-variant-large').text.strip()
    flight_time_elements = element.find_all('div', class_='vmXl-mod-variant-large')

    # Check if there are at least 2 elements (outbound and return times)
    if len(flight_time_elements) >= 2:
        outbound_time = flight_time_elements[0].text.strip()
        return_time = flight_time_elements[1].text.strip()

        # Find flight times including duration
        flight_times = element.find('div', class_='xdW8 xdW8-mod-full-airport').text.strip()

    # Check if the 'JWEO-stops-text' element exists
    stops_elem = element.find('span', class_='JWEO-stops-text')
    stops = stops_elem.text.strip() if stops_elem else 'No stops'  # Set a default value if the element is not found

    # Append the flight data to the list
    flight_data.append({
        'Price': price,
        'Time There': time_info,
        'Outbound Time': outbound_time,
        'Return Time': return_time,
        'Stops': stops,
        'Flight Time': flight_times
    })

driver.quit()

# Sort the flight_data list by price
sorted_flight_data = sorted(flight_data, key=lambda flight: float(flight['Price'].strip('£').replace(',', '')))

df = pd.DataFrame(sorted_flight_data)
csv_file_name = 'sorted_flights.csv'
df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')


# Print the sorted flight data
for flight in sorted_flight_data:
    print(flight)






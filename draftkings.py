from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up the WebDriver for Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the webpage
    driver.get("https://sportsbook.draftkings.com/leagues/basketball/ncaab")

    # Wait for the dynamic content to load
    time.sleep(5)  # Adjust this based on your network speed and page response time

    # Extract the HTML content after JavaScript execution
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty dictionary to store the data
    games_odds = {}

    # Find all elements within 'tbody' with class 'sportsbook-table__body'
    data = soup.find_all("tbody", class_="sportsbook-table__body")
    for tbody in data:
        rows = tbody.find_all("tr")
        for row in rows:
            # Find the team name and odds within each row
            team_name = row.find("div", class_="event-cell__name-text")
            odds = row.find("span", class_="sportsbook-odds american default-color")

            if team_name or odds:
                # Strip the text and store in the dictionary
                games_odds[team_name.text.strip()] = odds.text.strip()
                print("YESSSS", team_name.text.strip(), odds.text.strip())
                
finally:
    # Close the browser window
    driver.quit()

# Print the dictionary
print(games_odds)

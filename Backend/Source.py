from dotenv import load_dotenv
from SaveCSV import append_data
from Scrapper import LinkedInScraper
import os

# Clear the console
os.system('clear')

# Load environment variables
load_dotenv()
username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")
# profile_url = os.getenv("LINKEDIN_PROFILE_URL")

Data = []
profile_links = []
profile_url = ['https://www.linkedin.com/company/google']
# Initialize the scraper with credentials
scraper = LinkedInScraper(username, password)

# Log in to LinkedIn and wait for successful login (feed page)
scraper.login()

for url in profile_url:

    # Navigate to the profile page
    scraper.navigate_to_profile(url)

    # Get all profile URLs
    profile_data = scraper.get_profiles()

    # Scrape posts from the profile page
    post_data = scraper.scrape_posts()

    # Append the post data to the main data list
    Data.extend(post_data)
    profile_url.extend(profile_data)
    profile_links.extend(profile_data)

    append_data(post_data)

# Close the browser when done
scraper.close()

# Display extracted post data
for i in range(0, len(profile_links)):
    print(i+1, profile_links[i], end="\n\n")

for i in range(0,len(Data)):
    print(i+1,Data[i], end="\n\n")

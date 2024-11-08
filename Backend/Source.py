from dotenv import load_dotenv
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
profile_url = ['https://www.linkedin.com/company/google','https://www.linkedin.com/showcase/google-cloud/posts/?feedView=all']
# Initialize the scraper with credentials
scraper = LinkedInScraper(username, password)

# Log in to LinkedIn and wait for successful login (feed page)
scraper.login()

for url in profile_url:
    # Navigate to the profile page
    scraper.navigate_to_profile(url)

    # Scrape posts from the profile page
    post_data = scraper.scrape_posts()

    # Append the post data to the main data list
    Data.extend(post_data)

# Close the browser when done
scraper.close()

# Display extracted post data
for i in range(0,len(Data)):
    print(i+1,Data[i], end="\n\n")
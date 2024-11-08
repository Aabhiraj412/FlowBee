from dotenv import load_dotenv
from SaveCSV import append_data
from Scrapper import LinkedInScraper
import os
import time
import redis

# Clear the console
os.system('clear')

# Load environment variables
load_dotenv()
username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define Redis keys for the queues
PROFILE_URL_QUEUE = "profile_url_queue"

# Clearing the Redis queue
redis_client.delete(PROFILE_URL_QUEUE)

# Initialize the scraper with credentials
Data = []
visited = []
profile_url = "https://www.linkedin.com/company/google"
redis_client.rpush(PROFILE_URL_QUEUE, profile_url)

# Initialize the scraper with credentials
scraper = LinkedInScraper(username, password)

# Log in to LinkedIn and wait for successful login (feed page)
scraper.login()

# Function to process profile URLs from the Redis queue
def process_profiles():
    while True:

        # Pop a profile URL from the start of the Redis queue
        url = redis_client.lpop(PROFILE_URL_QUEUE)
        
        if url is None:
            print("No more URLs in the queue, waiting for new entries...")
            time.sleep(2)  # Wait before trying again if queue is empty
            continue

        url = url.decode("utf-8")  # Convert from bytes to string if needed
        
        if url in visited:
            continue

        print(f"Processing URL: {url}")
        
        visited.append(url)

        # Navigate to the profile page
        scraper.navigate_to_profile(url)

        # Get all profile URLs and add them to the queue
        profile_data = scraper.get_profiles()
        for new_url in profile_data:
            if new_url not in visited:
                redis_client.rpush(PROFILE_URL_QUEUE, new_url)

        # Scrape posts from the profile page
        post_data = scraper.scrape_posts()
        
        append_data(post_data)  # Custom function as per your existing code

process_profiles()  # Start processing URLs from the Redis queue

# Close the browser when done
scraper.close()
from dotenv import load_dotenv
from threading import Thread
from SaveCSV import append_data, temp_data
from Scrapper import LinkedInScraper
from DB import connectDB
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
profile_url = os.getenv("PROFILE_URL")
redis_client.rpush(PROFILE_URL_QUEUE, profile_url)

class WorkingInstance:

    redis_client = redis_client
    visited = visited

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.scraper = LinkedInScraper(username, password)  # Initialize LinkedIn scraper
        
    # Log in to LinkedIn and wait for successful login (feed page)
    def login(self):
        self.scraper.login()


    # Function to process profile URLs from the Redis queue
    def process_profiles(self):
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
            
            self.visited.append(url)

            # Navigate to the profile page
            self.scraper.navigate_to_profile(url)

            # Get all profile URLs and add them to the queue
            profile_data = self.scraper.get_profiles()
            for new_url in profile_data:
                if new_url not in visited:
                    redis_client.rpush(PROFILE_URL_QUEUE, new_url)

            # Scrape posts from the profile page
            post_data = self.scraper.scrape_posts(url)
            
            append_data(post_data)  # Custom function as per your existing code
            temp_data(post_data)

    # Close the browser when done
    def close(self):
        self.scraper.close()

    def run(self):
        self.login()
        self.process_profiles()
        self.close()


# Main function to start the scraping process
if __name__ == "__main__":
    
    # Create multiple instances of WorkingInstance
    # Run each scraper instance in parallel (you can use threading, multiprocessing, etc.)
    # Here we are using separate threads for concurrent execution.
    # Start the scraping process concurrently

    scraper1 = WorkingInstance(username, password)
    thread1 = Thread(target=scraper1.run)
    thread1.start()

    # time.sleep(10)

    # scraper2 = WorkingInstance(username, password)
    # thread2 = Thread(target=scraper2.run)
    # thread2.start()


    # Wait for both threads to finish
    thread1.join()
    # thread2.join()
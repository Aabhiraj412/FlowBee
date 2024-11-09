import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class LinkedInScraper:
    def __init__(self, username, password):
        # Initialize undetected Chrome driver
        self.username = username
        self.password = password
        # self.profile_url = profile_url

        print('Opening Chrome...')
        self.driver = uc.Chrome()

    def login(self):
        
        # Open LinkedIn login page
        print('Redirecting to LinkedIn')
        self.driver.get("https://www.linkedin.com/login")
        
        # Wait for the username and password fields to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )


        # Enter credentials and log in
        print('Logging in...')
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)


        # Wait to confirm login
        for i in range(40,0,-1):
            print(f"Waiting for login... {i} seconds remaining.")
            time.sleep(1)
            os.system('clear')
            if "feed" in self.driver.current_url:
                break

        if "feed" in self.driver.current_url:
            print("Login successful!")
        else:
            print("Login failed. Check credentials or CAPTCHA.")

    def navigate_to_profile(self,profile_url):
        # Go to the profile page
        self.driver.get(profile_url)
        time.sleep(3)

    def scroll_down(self):
        # Function to scroll down and load more posts
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def scrape_posts(self, profile_url):
        post_data = []

        # Scroll down multiple times to load more posts
        # for i in range(5):  # Adjust the range for the desired number of posts
        #     print(f"{i+1}th iterstion")
        #     self.scroll_down()
        
        # Locate all post elements after scrolling
        posts = self.driver.find_elements(By.CLASS_NAME, "fie-impression-container")
        print(f"Found {len(posts)} posts.")

        for i, post in enumerate(posts, start=1):
            print(f"Processing post {i}...")
            
            try:
                # Wait for each post's commentary section to be loaded
                WebDriverWait(post, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "feed-shared-update-v2__description-wrapper"))
                )

                # Locate the description wrapper div
                description_wrapper = post.find_element(By.CLASS_NAME, "feed-shared-update-v2__description-wrapper")
                
                media_type = 'none'
                try:
                    video = description_wrapper.find_element(By.CLASS_NAME, "update-components-linkedin-video")
                    media_type = 'video'
                except:
                    pass

                try:
                    image = description_wrapper.find_element(By.CLASS_NAME, "update-components-image")
                    media_type = 'image'
                except:
                    pass

                # Locate the inline show-more text div inside the description wrapper
                show_more_text = description_wrapper.find_element(By.CLASS_NAME, "feed-shared-inline-show-more-text")
                
                # Locate the commentary div inside the show-more text div
                commentary_div = show_more_text.find_element(By.CLASS_NAME, "update-components-text")
                
                # Extract the text from the <span> inside the commentary div
                commentary_text = commentary_div.find_element(By.TAG_NAME, "span").text

                # Locate the reaction bar div
                reaction_bar = post.find_element(By.CLASS_NAME, "update-v2-social-activity")

                # Locate the crutials inside the reaction bar
                crutials = reaction_bar.find_elements(By.CLASS_NAME, "social-details-social-counts")
                crutial = crutials[0]
                relative = crutial.find_elements(By.CLASS_NAME, "relative")
                counts_list = relative[0]

                # Initialize a dictionary to store extracted data for each post
                post_counts = {
                    "profile_url": profile_url,
                    "reactions": None,
                    "comments": None,
                    "reposts": None,
                    "media_type": media_type,
                    "commentary_text": commentary_text
                }

                # Iterate over each <li> element to extract details
                li_elements = counts_list.find_elements(By.CLASS_NAME, "social-details-social-counts__item")
                
                # Extract comments and reposts counts
                for i in range(0,len(li_elements)):
                    button = li_elements[i].find_element(By.TAG_NAME, "button")
                
                    if i==0:
                        reactions = button.find_element(By.TAG_NAME, "span").text
                        post_counts["reactions"] = reactions

                    elif i==1:
                        comments = button.find_element(By.TAG_NAME, "span").text
                        post_counts["comments"] = comments

                    else:
                        reposts = button.find_element(By.TAG_NAME, "span").text
                        post_counts["reposts"] = reposts
                
                # Append post counts to post_data list
                post_data.append(post_counts)

            except Exception as e:
                print(f"Error extracting data from post {i}: {e}")

        print("Scraping completed.")
        return post_data

    def get_profiles(self):
        # Function to extract profile links from the feed
        profile_links = []

        # Locate all profile elements
        profiles = self.driver.find_elements(By.CLASS_NAME, "org-view-entity-card__container")

        for i, profile in enumerate(profiles, start=1):
            print(f"Processing profile {i}...")

            try:
                # Locate the profile link element
                profile_link = profile.find_element(By.CLASS_NAME, "app-aware-link")
                profile_url = profile_link.get_attribute("href")

                # Append the profile link to the list
                profile_links.append(profile_url)


            except Exception as e:
                print(f"Error extracting profile URL from profile {i}: {e}")

        return profile_links

    def close(self):
        # Close the driver
        self.driver.quit()
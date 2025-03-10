import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from bs4 import BeautifulSoup

def scrape_signposts():
    print("\nStarting Signposts scraping...")
    base_url = "https://dev.azure.com/supercomputing2020/Project%20D%20-%20MASS/_wiki/wikis/MASS.wiki/213807/Quality-Signposts"
    driver.get(base_url)
    
    print("Waiting for page content to load...")
    time.sleep(5)

    try:
        # Get all links from the page
        links = {}
        elements = driver.find_elements(By.TAG_NAME, "a")
        
        # Filter for wiki page links
        for element in elements:
            try:
                href = element.get_attribute('href')
                text = element.text.strip()
                
                if (href and 
                    text and 
                    'wikiVersion=GBwikiMaster' in href and 
                    'workitems' not in href and 
                    text.startswith('moo')):
                    links[href] = text
                    print(f"✅ Found valid link: {text}")
            except Exception as e:
                print(f"Error processing link: {str(e)}")
                continue

        # Print found links for verification
        print(f"\nFound {len(links)} pages to scrape")
        for url, title in links.items():
            print(f"- {title}: {url}")

        proceed = input("\nDo you want to proceed with scraping these pages? (y/n): ")
        if proceed.lower() != 'y':
            return

        # Scrape each page
        for url, title in links.items():
            try:
                print(f"\nScraping: {title}")
                driver.get(url)
                time.sleep(2)

                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "markdown-content"))
                )
                
                with open(os.path.join(output_dir, f"{safe_title}.md"), "w", encoding="utf-8") as file:
                    file.write(f"# {title}\n\n")
                    file.write(content_element.text)

                print(f"✅ Saved: {title}")
            except Exception as e:
                print(f"❌ Error scraping {title}: {str(e)}")

    except Exception as e:
        print(f"Error during signposts scraping: {str(e)}")

def scrape_mug():
    print("\nStarting MUG documentation scraping...")
    
    # First open authentication page (you may need to update this URL to the actual auth page)
    auth_url = "https://docs.mass-stg.metoffice.gov.uk/"
    print(f"\nOpening authentication page: {auth_url}")
    driver.get(auth_url)
    
    # Wait for manual authentication
    input("\n👉 Please complete authentication and press Enter to continue...")
    
    # After authentication, navigate to the quick reference page
    quick_ref_url = "https://docs.mass-stg.metoffice.gov.uk/docs/CLI/quick-ref"
    print(f"\nNavigating to Quick Reference page: {quick_ref_url}")
    driver.get(quick_ref_url)
    
    print("Waiting for page content to load...")
    time.sleep(5)  # Wait for page load

    try:
        # Wait for the table to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Find all command links in the table
        links = {}
        elements = driver.find_elements(By.CSS_SELECTOR, "table a[href*='/docs/CLI/Commands/']")
        
        for element in elements:
            try:
                href = element.get_attribute('href')
                text = element.text.strip()
                if href and text:
                    # Remove the code formatting if present
                    text = text.replace('`', '')
                    links[href] = text
                    print(f"✅ Found command link: {text}")
            except Exception as e:
                print(f"Error processing link: {str(e)}")
                continue

        # Print found links for verification
        print(f"\nFound {len(links)} command pages to scrape")
        for url, title in links.items():
            print(f"- {title}: {url}")

        proceed = input("\nDo you want to proceed with scraping these pages? (y/n): ")
        if proceed.lower() != 'y':
            return

        # Scrape each page
        for url, title in links.items():
            try:
                print(f"\nScraping: {title}")
                driver.get(url)
                time.sleep(2)

                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                
                # Wait for content to load
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "theme-doc-markdown"))
                )
                
                # Get the content
                content = content_element.text
                
                # Save the content
                with open(os.path.join(output_dir, f"mug_{safe_title}.md"), "w", encoding="utf-8") as file:
                    file.write(f"# {title}\n\n")
                    file.write(content)

                print(f"✅ Saved: {title}")
                
                # Optional: save raw HTML for debugging
                with open(os.path.join(output_dir, f"mug_{safe_title}_raw.html"), "w", encoding="utf-8") as file:
                    file.write(content_element.get_attribute('innerHTML'))
                
            except Exception as e:
                print(f"❌ Error scraping {title}: {str(e)}")
                print(f"Current URL: {driver.current_url}")

    except Exception as e:
        print(f"Error during MUG scraping: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        print("Page source:")
        print(driver.page_source[:1000])  # Print first 1000 chars of page source for debugging

# Rest of the script remains the same...

# Setup WebDriver
edge_driver_path = "C:\\Users\\kkabza\\Downloads\\edgedriver_win64\\msedgedriver.exe"
options = Options()
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

# Create output directory
output_dir = "mass_documentation"
os.makedirs(output_dir, exist_ok=True)

try:
    # Ask user which content to scrape
    print("\nWhat would you like to scrape?")
    print("1. Quality Signposts")
    print("2. MUG Documentation")
    print("3. Both")
    
    choice = input("\nEnter your choice (1, 2, or 3): ")

    if choice in ['1', '3']:
        scrape_signposts()
    
    if choice in ['2', '3']:
        scrape_mug()

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    input("\n✅ Press Enter to close the browser...")
    driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up Chromium options
chrome_options = Options()

# Specify Chromium binary location (update with correct path)
chrome_options.binary_location = r"C:\Program Files\Chromium\Application\chrome.exe"  # Adjust as needed

# Use an existing user profile to persist cookies
chrome_options.add_argument(r"--user-data-dir=C:\Users\kkabza\AppData\Local\Chromium\User")
chrome_options.add_argument("--profile-directory=Default")  # Default profile (change if using another profile)

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
url = "https://dev.azure.com/supercomputing2020/Project%20D%20-%20MASS/_wiki/wikis/MASS.wiki/213815/moo-login-moo-logout"
driver.get(url)

# Keep browser open for interaction
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

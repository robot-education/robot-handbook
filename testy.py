from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

driver = webdriver.Chrome(
    service=ChromeService("/usr/bin/google-chrome", service_args=["--no-sandbox"])
)

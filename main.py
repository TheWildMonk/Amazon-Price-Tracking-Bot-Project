# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from smtplib import *

# Constants
EMAIL = "demo@email.com"
RECEIVER = "receiver@email.com"
PASSWORD = "##########"

# Amazon url for RTX 3060 Eagle
amazon_url = "https://www.amazon.com/GIGABYTE-REV2-0-WINDFORCE-GV-N3060EAGLE-OC-12GD/" \
             "dp/B0971B5B1L/ref=sr_1_1?dchild=1&" \
             "keywords=gigabyte+rtx+3060+eagle+oc+12gb&qid=1634428596&sr=8-1"

# Retrieve product page response
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9,bn-BD;q=0.8,bn;q=0.7,en-US;q=0.6"
}
response = requests.get(url=amazon_url, headers=HEADERS)
response.raise_for_status()
product_page = response.text

# Create soup of the product page & retrieve the product price
soup = BeautifulSoup(product_page, "html.parser")
product_title = (soup.find(name="span", id="productTitle")).text.strip("\n")
product_price = float(soup.find(name="span", id="priceblock_ourprice").text.strip("$"))

# Check whether the product price is below expected price
# if it is, then send an email to the user
TARGET_PRICE = 600.00
if product_price <= TARGET_PRICE:
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=RECEIVER,
                            msg="subject: Your Product Price Has Fallen!\n\n"
                            f"{product_title} is now at ${product_price}. Grab it right now!\n"
                                f"{amazon_url}")
else:
    print(f"{product_title} is now ${product_price} which is above your target price ${TARGET_PRICE}.")

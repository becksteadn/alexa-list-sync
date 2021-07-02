import requests
import os
from datetime import datetime
from escpos.printer import Usb

def send_to_printer(shopping_list):
    printer = Usb(idVendor=0x0416, idProduct=0x5011)
    now = datetime.now().strftime("%m/%d/%Y")

    printer.set(align="center", width=2)
    printer.text("Groceries for {}!\n".format(now))
    printer.text("\n")

    printer.text(shopping_list)

    printer.set(align="center", width=2)
    printer.text("\n")
    printer.text("Have a great day! :)\n")

    printer.cut()

def main():
    bucket = os.environ["GROCERY_BUCKET"]
    key = os.environ["GROCERY_KEY"]
    stop_url = os.environ["STOP_PRINT_URL"]
    url = f"https://{bucket}.s3.amazonaws.com/{key}"

    test = requests.head(url)
    if test.status_code == 200:
        response = requests.get(url)
        shopping_list = response.text
        send_to_printer(shopping_list)
        response = requests.get(stop_url)
    


if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
import shelve
import time
import sys,time,random

print("Welcome to my bookstore")
time.sleep(1)
first_time = True

with shelve.open("money.db") as db:
    mon = db['mon']

username = input("What is your username: ").strip().capitalize()

def user():
    global first_time
    global username
    with shelve.open("users.db") as db:
        if username not in db:
            print("Your new around here, welcome {}.".format(username))
            db[username] = True
            first_time = True
        else:
            first_time = False
            print("Welcome back {}".format(username))


def discount():
    global coupon_code
    global code
    discount_coupon = input("Do you have the discount coupon? [y/n] : ").strip().lower()
    code = "1234"
    
    if discount_coupon == "y":
        coupon_code = input("Please enter coupon code: ").strip()
        if coupon_code == code:
            print("You now have a 10% discount on all your purchases!!!")
            time.sleep(2)
        else:
            print("Sorry incorrect coupon code")
    elif discount_coupon == "n":
        print("No worries you can aquire a coupon after three purchases.")
        time.sleep(2)
        coupon_code = 123
    else:
        print("Sorry incorrect input")

def money():
    global first_time
    global mon
    with shelve.open("money.db", writeback=True) as db:
        if first_time:
            mon = 100
            db["mon"] = mon
            print("Current credits {}".format(mon))
            time.sleep(3)
        else:
            mon = db.get('mon', 0)
            print("You have {} credits".format(mon))
            time.sleep(1)

def slow_type(t, typing_speed):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)
    print()

typing_speed = 90

print("=" * 50)
print("We will start shopping for books of your interest.")
time.sleep(2)

url = "https://books.toscrape.com/"
soup = BeautifulSoup(requests.get(url).content, "html.parser")

categories = soup.select(".side_categories ul.nav-list li a")
print("What category would you like to choose from:")

number = 0

for category in categories[:11]:
    number = number + 1
    new_category = str(number) + "." + category.get_text(strip=True)
    slow_type(new_category, typing_speed)
    
choice_number = input("Enter the number of your choice: ").strip().capitalize()

if choice_number.isdigit() and 1 <= int(choice_number) <= 11:
    global chosen_category
    chosen_category = categories[int(choice_number) - 1].get_text(strip=True)
else:
    print("Sorry, incorrect input")

chosen_category_link = categories[int(choice_number) - 1]['href']
category_url = url + chosen_category_link
category_page = BeautifulSoup(requests.get(category_url).content, "html.parser")
books = category_page.select("h3 a")  

typing_speed = 500

print("=" * 50)
content = chosen_category
line_width = 100

centered_line = content.center(line_width)
print(centered_line)

min_space = 5
second_number = -1
new_num = 0

for i in range(0, len(books), 2):
    global book1_title
    second_number = second_number + 2
    new_num = new_num + 2
    book1_title = books[i].get('title', '').strip()  
    book2_title = books[i + 1].get('title', '').strip() if i + 1 < len(books) else ""
    space_between_titles = " " * min_space
    slow_type(f"{second_number}.{book1_title:<50}{space_between_titles}{new_num}.{book2_title:<50}", typing_speed)
    print("")

choice_book = input("What book would you like to buy? [number]: ").strip()

maximum = max(second_number, new_num)
typing_speed = 90

if choice_book.isdigit() and 1 <= int(choice_book) <= maximum:
    global chosen_book
    global chosen_price
    chosen_book = books[int(choice_book) - 1].get_text(strip=True) 
    slow_type(f"\nTitle: {chosen_book}", typing_speed)

    price_elements = category_page.select(".price_color")
    chosen_price = price_elements[int(choice_book) - 1].get_text(strip=True) 
    slow_type(f"Price: {chosen_price}", typing_speed)

    stock_elements = category_page.select(".instock.availability")
    chosen_stock = stock_elements[0].get_text(strip=True)
    slow_type(f"Stock: {chosen_stock}", typing_speed)

else:
    print("Invalid input. Please enter a valid book number.")

print("=" * 50)

buy = input(f"Would you like to buy {chosen_book} [y,n] : ").strip()

if buy == "y":
    pass
elif buy == "n":
    print("Ok, bye")
    time.sleep(1)
    exit
else:
    print("Invalid input.")

buys = 0

if buy == "y":
    with shelve.open("buys.db", writeback=True) as db:
        buys = db.get('buys', 0)
        buys += 1
        db['buys'] = buys

if buys == 3:
    print("Discount coupon code is 1234")

user()
money()

add_mon = input(f"Would you like to add some credits? [y,n]: ").strip()

with shelve.open("money.db", writeback=True) as db:
    if 'mon' not in db:
        mon = 100
        db['mon'] = mon 
    else:
        mon = db['mon']

if add_mon == "y":
    amount = input("Enter an amount: ").strip()
    mon += int(amount) 
    with shelve.open("money.db", writeback=True) as db:
        db['mon'] = mon
    print(f"Updated balance: {mon}")
elif add_mon == "n":
    print("Ok")
else:
    print("Invalid input. ")

discount()

chosen_price = chosen_price.replace('£', '')
chosen_price = float(chosen_price)

if coupon_code == code:
    discounted = chosen_price * 10 / 100
    chosen_price -= discounted
else:
    pass

left_money = mon - chosen_price
with shelve.open("money.db", writeback=True)  as db:
    db["mon"] = int(left_money)

no = True

if left_money > 0:
    print(f"Money remaining: {int(left_money)}")
else:
    print("Sorry, you do not have enough money to purchase this book.")
    no = True

if no == True:
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_week = random.choice(days_of_week)

    print(f"Your book will arrive on {day_week}")
else:
    exit(1)


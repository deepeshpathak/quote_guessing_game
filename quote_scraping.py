import requests #The requests module allows you to send HTTP requests using Python. which returns data
from bs4 import BeautifulSoup #Beautiful Soup is a Python library for getting data out of HTML, XML, and other markup languages
from csv import DictReader # to work and read csv file
from random import choice #to get a random quote choice 
from time import sleep #to get some delay before making another requests

def scrape_quotes():
	main_url = "http://quotes.toscrape.com/"
	page_url = "/page/1"
	quote_dicts = []
	while page_url:
		response = requests.get(f"{main_url}{page_url}") #requesting a response 
		print(f"Currently scraping {main_url}{page_url}...")
		soup = BeautifulSoup(response.text, "html.parser")#getting text out of the response
		quotes = soup.find_all(class_="quote") #finding all quotes having class name ="quote"
		for quote in quotes:#appending data to a dictionary
			quote_dicts.append({
				"text": quote.find(class_="text").get_text(),
				"author": quote.find(class_="author").get_text(),
				"link": quote.find("a")['href']
			})
		next_page = soup.find(class_="next")#finding next page 
		page_url = next_page.find("a")["href"] if next_page else None #finding the url if not found then set it to one
		sleep(1)
	return quote_dicts

def write_quotes(quotes):#saving all the responses on a csv file 
	with open("quote_data.csv", "w",encoding="utf-8") as file:
		headers = ["text", "author", "link"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for quote in quotes:
			csv_writer.writerow(quote)
quotes = scrape_quotes()
write_quotes(quotes)

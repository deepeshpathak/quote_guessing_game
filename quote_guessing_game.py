import requests #The requests module allows you to send HTTP requests using Python. which returns data
from bs4 import BeautifulSoup #Beautiful Soup is a Python library for getting data out of HTML, XML, and other markup languages
from csv import DictReader # to work and read csv file
from random import choice #to get a random quote choice 
from time import sleep #to get some delay before making another requests
from pyfiglet import figlet_format #to me ASCII text int FONTS
from termcolor import colored #to give color

main_url = "http://quotes.toscrape.com/"

def read_quotes(filename): #reading from CSV file and returning a list of quotes
	with open(filename, "r",encoding="utf-8") as file:
		csv_reader = DictReader(file)
		quotes = list(csv_reader)
	return quotes

def replay(): #asking for replay
	return input('Would you like to play again? Yes or No: ').lower().startswith('y')


def win(guess, answer): #check weather author is guessed or not case insensitive
	return guess.lower() == answer.lower()


def play(quotes):
	while True:
		quote = choice(quotes)#getting a random quote
		print(quote["text"])
		guess = ""
		answer = quote["author"]#actual answer
		guesses_remaining = 4

		while not win(guess, answer) and guesses_remaining >= 0: #up untill our answer is wrong
			guess = input(f"Who said this? You have {guesses_remaining} guesses.\n")
			guesses_remaining -= 1
			if win(guess, answer):#break if ans is correct
				print("Congratulations! You are correct.")
				break
			elif guesses_remaining == 3:#first hint
				res = requests.get(f"{main_url}{quote['link']}")
				soup = BeautifulSoup(res.text, "html.parser")
				date = soup.find(class_="author-born-date").get_text()
				place = soup.find(class_="author-born-location").get_text()
				print(f"Incorrect!! Here is a clue:\nThey were born on {date} {place}.")
			elif guesses_remaining == 2:#second hint
				first_initial = quote["author"][0] #first letter of first name
				print(f"Incorrect!! Here is a clue:\nTheir first name starts with {first_initial}.")
			elif guesses_remaining == 1:# last hint
				last_initial = quote["author"].split()[1][0]#first letter of last name
				print(f"Incorrect!! Here is a clue:\nTheir last name starts with {last_initial}.")
			else:
				print(f"You are out of guesses.\nThe answer was: {quote['author']}")
				break

		if not replay():
			print("Goodbye!")
			break

header = figlet_format("Guess the Quote!")
header = colored(header, color="red")
print(header)
quotes = read_quotes("quote_data.csv")
play(quotes)

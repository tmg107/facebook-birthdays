from website import create_app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlite3
import requests 
import json 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pyautogui as py
import numpy as np
import time
from datetime import datetime

### Create Facebook Class Object for pulling friends from a facebook account
class facebook_crawler:
	## Open up facebook website
	# /Users/maxg/Desktop/Weekend_Projects/Bday_Feb_2021
	chromedriver = "./chromedriver"
	facebook = "https://www.facebook.com"
	# Set initial state for class object
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome(self.chromedriver)
		self.wait = WebDriverWait(self.driver, 10)

	# Define instance method for login and find friends list
	def find_friends(self):
		"""
		Method: opens facebook through selenium to get list of friends and their profile urls
		"""
		# Initiate sqlite database to store birthdays
		engine = create_engine('sqlite://', echo=False)
		#conn = sqlite3.connect('birthday_db.sqlite')
		#cur = conn.cursor()

		# Start login to facebook to pull birthdays
		self.driver.get(self.facebook)
		# Enter email 
		inputElement = self.driver.find_element_by_id("email")
		inputElement.send_keys(self.username)
		# Enter password
		inputElement2 = self.driver.find_element_by_id('pass')
		inputElement2.send_keys(self.password)
		# Press enter key
		inputElement2.submit()
		time.sleep(3)

		# Initiate dictionary to store dates
		birthday_dict = {}
		i = 0
		### Pull out container for birthdays starting on * Jan 2022 *
		for month in range(1, 13):
			bday_URL = f'https://mbasic.facebook.com/events/birthdays?cursor=2022-{month:02d}-01&acontext=%7B%22ref%22%3A%222%22%2C%22ref_dashboard_filter%22%3A%22birthdays%22%2C%22source%22%3A%222%22%2C%22action_history%22%3A%22%5B%7B%5C%22surface%5C%22%3A%5C%22dashboard%5C%22%2C%5C%22mechanism%5C%22%3A%5C%22surface%5C%22%2C%5C%22extra_data%5C%22%3A%7B%5C%22dashboard_filter%5C%22%3A%5C%22birthdays%5C%22%7D%7D%5D%22%7D'
			self.driver.get(bday_URL)
			html = self.driver.page_source

			# Use beautiful soup to extract elements
			soup = BeautifulSoup(html, "html.parser")
			print(month)
			
			## Extract container of friends on page
			friends_div = soup.find_all('li', class_='bk cy')
			for friend in friends_div:
				person = friend.find('p', class_='co cz cx').text
				birthday_long = friend.find('p', class_='dc ch dd cx').text
				birthday = birthday_long.split(',')[1]
				birthday_dict[i] = [person, birthday]
				i += 1

			# Pause between iterations to avoid block by system
			time.sleep(2)

		# Convert dictionary to a pandas df w/ columns Friend, Birthday and index number as row 
		birthday_pd = pd.DataFrame.from_dict(birthday_dict, orient='index', columns=['Friend', 'Birthday'])
		# Convert to csv output
		birthday_pd.to_csv('birthdays.csv', index=False)
		# To SQL engine
		birthday_pd.to_sql('birthdays', con=engine, if_exists='replace')
		# print(engine.execute("SELECT * FROM birthdays").fetchall())
		self.driver.close()


### Run Flask application defined in __init__.py in website
# Initiate app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)

# # Test class object
# if __name__ == '__main__':
# 	maxgor_acc = facebook_crawler(username='maxuncgordon@gmail.com', password='poe5waco$')
# 	maxgor_acc.find_friends()






























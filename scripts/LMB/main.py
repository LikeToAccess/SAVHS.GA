# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Find Lunch!?
# author            : Ian Ault
# email             : ianault2022@isd282.org
# date              : 02-14-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import os
import datetime
import time
import json
import uuid
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from settings import *


links = [
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61c1e808534a139e3dea1b36&\
menuType=610aacdb534a1367458b4683&siteCode=20001&showAllNutrients=false",  # Grab N Go
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61c1e82b534a131337ea1b3b&\
menuType=6102de69534a13557755dde1&siteCode=20001&showAllNutrients=false",  # Grill Line
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61c1e84d534a13763fea1b3c&\
menuType=6102de5b534a13a26355ddef&siteCode=20001&showAllNutrients=false",  # Hot Sandwich Line
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61c1e7e6534a136c3fea1b35&\
menuType=6102dd39534a13477155de0b&siteCode=20001&showAllNutrients=false",  # Daily Dish
]

days_of_the_week = {
	"MON": "Monday",
	"TUE": "Tuesday",
	"WED": "Wednesday",
	"THU": "Thursday",
	"FRI": "Friday",
	"SAT": "Saturday",
	"SUN": "Sunday",
}


def remove_file(filename):
	os.remove(filename)

def read_file(filename, encoding="utf8"):
	if not os.path.exists(filename): return []
	with open(filename, "r", encoding=encoding) as file:
		data = file.read().split("\n")

	return data

def write_file(filename, data, encoding="utf8"):
	with open(filename, "w", encoding=encoding) as file:
		file.write(data)

def read_json_file(filename, encoding="utf8"):
	if not os.path.exists(filename): return []
	with open(filename, "r", encoding=encoding) as file:
		data = json.load(file)

	return data

def write_json_file(filename, data, encoding="utf8"):
	with open(filename, "w", encoding=encoding) as file:
		json.dump(data, file, indent=4, sort_keys=True)

	return json.dumps(data, indent=4, sort_keys=True)

def append_json_file(filename, data, encoding="utf8"):
	existing_data = read_json_file(filename, encoding=encoding)
	existing_data.append(data)
	write_json_file(filename, existing_data, encoding=encoding)

def reformat_json_to_js(filename, encoding="utf8"):
	json_text = "\n".join(read_file(filename))
	js_text = "var obj = \n" + json_text + ";"
	write_file(filename + ".js", js_text, encoding=encoding)

def finalize(filename):
	reformat_json_to_js(filename)
	print("\n".join(read_file(filename)))


class Scraper:
	def __init__(self):
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument(f"user-data-dir={user_data_dir}")
		options.add_argument("log-level=3")
		if HEADLESS:
			options.add_argument("--headless")
			options.add_argument("--disable-gpu")
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		# self.driver.minimize()
		print("Init finished")

	def wait_until_element(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		element = wait.until(
			EC.presence_of_element_located(
				(
					selector, locator
				)
			)
		)
		return element

	def wait_until_elements(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		elements = wait.until(
			EC.presence_of_all_elements_located(
				(
					selector, locator
				)
			)
		)
		return elements

	def find_element(self, selector, sequence):
		return self.driver.find_element(selector, sequence)

	def find_elements(self, selector, sequence):
		return self.driver.find_elements(selector, sequence)

	def wait_until_element_by_xpath(self, sequence):
		return self.wait_until_element(By.XPATH, sequence)

	def wait_until_elements_by_xpath(self, sequence):
		return self.wait_until_elements(By.XPATH, sequence)

	def find_element_by_xpath(self, sequence):
		return self.find_element(By.XPATH, sequence)

	def find_elements_by_xpath(self, sequence):
		return self.find_elements(By.XPATH, sequence)

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def refresh(self):
		self.driver.refresh()

	def sign_eula(self):
		self.driver.execute_script("window.localStorage.setItem('acceptedDisclaimer','1');")
		self.driver.execute_script(f"window.localStorage.setItem('profile_uuid','{str(uuid.uuid1())}');")

	# def minimize(self):
	# 	self.driver.minimize_window()

	def get_lunch(self, url):
		self.open_link(url)
		self.sign_eula()
		self.refresh()

		# time.sleep(1.0)  # Wait for text to finish loading (the elements exist but some text is missing)
		# ^^^ This doesn't work :(
		# The above comment ^^^ is a lie :)

		month = self.wait_until_elements_by_xpath(
			'//*[@class="sc-iwsKbI cpOFXO currentmonth"]')
		menu = self.wait_until_element_by_xpath(
			'//*[@id="ng-view"]/react-app/div[1]/div/div[2]/div[2]/span').text

		lunch = {}
		for day in month:
			day_information = day.text.replace("\nzoom_in", "").split("\n")
			extranious_characters = "}{"
			lunch_items = []
			for data in enumerate(day_information[2:]):
				_, lunch_item = data
				lunch_items.append(
					lunch_item.translate(
						{ord(i): None for i in extranious_characters}
					).replace(
						"w/", " with "
					).replace(
						"  ", " "
					)
				)
			day_information[1] = days_of_the_week[day_information[1]]

			while menu == "- SANB Secondary School":
				time.sleep(0.1)
				menu = self.wait_until_element_by_xpath(
					'//*[@id="ng-view"]/react-app/div[1]/div/div[2]/div[2]/span').text
				print("Updating menu type...")

			lunch[day_information[0]] = {
				"lunch_items": lunch_items,
				# "day":         day_information[1],
				"menu_type":   menu
			}

		return lunch, menu

	def run(self):
		os.chdir(f"{LOG_DIRECTORY}/..")
		logs_folder_name = os.path.basename(os.path.normpath(LOG_DIRECTORY))
		if not os.path.exists(logs_folder_name):
			print(logs_folder_name)
			print(LOG_DIRECTORY)
			os.mkdir(logs_folder_name)
		date = datetime.datetime.now()
		filename = date.strftime(logs_folder_name + "/LD_%Y-%m-%d.json")

		full_month_lunch_schedule = {}
		if os.path.exists(filename):
			if len(read_json_file(filename)) != 4:
				remove_file(filename)
			else:
				finalize(filename)
				return
		print("Opening URL")
		for link in tqdm(links):
			lunch, menu_type = self.get_lunch(link)
			full_month_lunch_schedule[menu_type] = lunch
			if date.strftime("%#e") in lunch:
				try:
					append_json_file(filename, lunch[date.strftime("%-d")])
				except (KeyError, ValueError):
					append_json_file(filename, lunch[date.strftime("%#e")])
			else:
				append_json_file(filename, "['No Lunch Today']")
		finalize(filename)


if __name__ == "__main__":
	scraper = Scraper()
	scraper.run()
	scraper.close()

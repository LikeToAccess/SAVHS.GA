# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Convert Senior Survey Google Doc into JSON
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 04-29-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import tkinter as tk
import json
import os
import shutil
import platform
import tqdm


OS = platform.system()


def get_clipboard_text():
	root = tk.Tk()
	# keep the window from showing
	root.withdraw()
	return root.clipboard_get()

def wait_for_input():
	if OS == "Windows":  # Only works on Windows
		os.system("pause")
	else:                # Works for MacOS and Linux
		print("Press any key to continue...", end="", flush=True)
		os.system("read -n1 -r")

def remove_file(filename):
	try:
		os.remove(filename)
		return True
	except OSError:
		return False

def read_file(filename, encoding="utf8"):
	if not os.path.exists(filename): return filename
	with open(filename, "r", encoding=encoding) as file:
		data = file.read()

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
	json_text = read_file(filename)
	js_text = "var seniorSurvey = \n" + json_text + ";"
	write_file(filename + ".js", js_text, encoding=encoding)

def finalize(filename):
	reformat_json_to_js(filename)
	# print(read_file(filename))

def verify_data(data, message=None):
	while not data.startswith("#"):
		if message: print(message)
		wait_for_input()
		data = get_clipboard_text()

	return data

def main():
	# data = input("Please copy/paste the Document text here:\n> ")
	data = verify_data(
		get_clipboard_text(),
		"\nInput data is malformed (expected first character to be '#'), are you sure you copied the correct text?"
	)

	questions = []
	for item in tqdm.tqdm(data.split("\n")):
		if item.startswith("# "):
			questions.append({item.strip("# "): []})
			print(item)
			continue

		if "-" in item:
			response, respondee = item.rsplit("-", 1)
		else:
			response, respondee = item, "Anonymous"

		if response:
			try:
				questions[-1][list(questions[-1].keys())[-1]].append([response, respondee])
			except IndexError as error:
				print(f"\nGot '{error}' error: are you sure you copied the correct text?")
				wait_for_input()
				main()

	remove_file("senior_survey.json")
	append_json_file("senior_survey.json", questions)
	finalize("senior_survey.json")
	shutil.copyfile("senior_survey.json", "../../senior_survey.json")
	shutil.copyfile("senior_survey.json.js", "../../senior_survey.json.js")


if __name__ == "__main__":
	main()

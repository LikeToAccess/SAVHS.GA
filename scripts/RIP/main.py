# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Download and convert Instagram posts from an account
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 04-27-2022
# version           : v1.0
# usage             : python main.py profile [profile ...]
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import platform
import sys
import os
import time
import json
import shutil
import tqdm
import instaloader
from settings import *


OS = platform.system()
profiles = sys.argv[1:]
il = instaloader.Instaloader()


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
	js_text = "var instagramData = \n" + json_text + ";"
	write_file(filename + ".js", js_text, encoding=encoding)

def finalize(filename):
	reformat_json_to_js(filename)
	print(read_file(filename))

def login_to_instagram():
	try:
		il.login(USERNAME, PASSWORD)
		return True
	except instaloader.exceptions.ConnectionException:
		return False

def download_posts(profile):
	profile = instaloader.Profile.from_username(il.context, profile)
	posts = profile.get_posts()
	# il.download_profiles([profile], profile_pic=False)#, post_filter="congrats")
	for post in posts:
		print(post.date_utc)
		print(post.caption)
		il.download_post(post, target=profile.username)

	return profile

def main():
	if OS == "Windows":
		ffmpeg_binary = "ffmpeg.exe"
	else:  # Works for MacOS and Linux
		ffmpeg_binary = "./ffmpeg"

	profile = None
	for profile in profiles:
		print(profile)
		# while not login_to_instagram():
		# 	time.sleep(3)
		# download_posts(profile)
		remove_file("2022-03-19_06-15-57_UTC.png")
		remove_file("2022-03-19_06-15-57_UTC.webp")

		profile_images = []
		for file in tqdm.tqdm(os.listdir(profile)):
			profile_image = []
			if file.endswith(".webp"):
				os.system(f"{ffmpeg_binary} -i {profile}/{file} {profile}/{file.replace('.webp','.png')} -y -hide_banner -loglevel error")
				if not os.path.exists(f"../../{profile}/"):
					os.mkdir(f"../../{profile}/")

				shutil.copyfile(f"{profile}/{file.replace('.webp','.png')}", f"../../{profile}/{file.replace('.webp','.png')}")

				profile_image.append({
					"image_filename": file.replace(".webp", ".png"),
					"text":           read_file(profile+"/"+file.replace(".webp", ".txt")).strip("\n"),
				})

				profile_images.append(profile_image)

		remove_file(profile+".json")
		append_json_file(f"{profile}.json", profile_images)
		shutil.copyfile(f"{profile}.json", f"../../{profile}.json")

	finalize(profile+".json")
	shutil.copyfile(f"{profile}.json.js", f"../../{profile}.json.js")



if __name__ == "__main__":
	main()

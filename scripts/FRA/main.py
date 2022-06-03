# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Flask Restful API
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 06-02-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import json
import os
import jmespath
import shutil
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from waitress import serve


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})
data_filename = "quotes.json"


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
	js_text = "var quotes = \n" + json_text + ";"
	write_file(filename + ".js", js_text, encoding=encoding)

def finalize(filename):
	reformat_json_to_js(filename)
	print("\n".join(read_file(filename)))


seniors = read_json_file("../DGP/domain_group_memberships.json")
seniors = jmespath.search('[]."12th Grade"[].member', seniors)


class Quotes(Resource):
	def get(self):
		# Gets all senior quotes
		quotes = read_json_file(data_filename)
		return {"message": quotes}, 200

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("email", required=True, type=str, location="args")
		parser.add_argument("name", required=True, type=str, location="args")
		parser.add_argument("quote", required=True, type=str, location="args")
		parser.add_argument("profile_picture", required=False, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		email, name, quote = args["email"], args["name"], args["quote"]
		if "profile_picture" in args: profile_picture = args["profile_picture"]
		else: profile_picture = False

		if "ISD282\\"+ email.split("@isd282.org")[0] not in seniors:
			return {"message": "Unauthorized"}, 401

		data = {
			"email": email,
			"name": name,
			"quote": quote,
			"profile_picture": profile_picture,
		}

		print(json.dumps(data))

		quotes = read_json_file(data_filename)
		# print(quotes)
		new_quote = True
		updated_quotes = []
		for _quote in quotes:
			if _quote["email"] == email:
				print("User already has a quote!")
				_quote["quote"] = quote
				new_quote = False
			updated_quotes.append(_quote)
		if new_quote:
			updated_quotes.append(data)

		write_json_file(data_filename, updated_quotes)
		finalize(data_filename)
		shutil.copyfile(data_filename, f"../../{data_filename}")
		shutil.copyfile(data_filename+ ".js", f"../../{data_filename}.js")

		return {"message": f"Succesfully added quote for {name}"}, 200

class Sample(Resource):
	def get(self):
		return {"message": "Not implemented"}, 501

	def post(self):
		return {"message": "Not implemented"}, 501


def main():
	api.add_resource(Quotes, "/quotes")
	api.add_resource(Sample, "/sample")
	serve(app, host="0.0.0.0", port=8080)
	# app.run()


if __name__ == "__main__":
	main()

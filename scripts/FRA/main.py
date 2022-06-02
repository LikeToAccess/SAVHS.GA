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
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from waitress import serve


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})
data_filename = "quotes.json"


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


seniors = read_json_file("../DGP/domain_group_memberships.json")
seniors = jmespath.search('[]."12th Grade"[].member', seniors)
# print(seniors)


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

		data = {
			"email": email,
			"name": name,
			"quote": quote,
			"profile_picture": profile_picture,
		}

		append_json_file(data_filename, data)

		return {"message": f"Succesfully added quote for {name}"}

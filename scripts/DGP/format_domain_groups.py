# -*- coding: utf-8 -*-
# filename          : format_domain_groups.py
# description       : Format Domain Controller user dumps
# author            : Ian Ault
# email             : ianault2022@isd282.org
# date              : 04-06-2022
# version           : v1.0
# usage             : python format_domain_groups.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import json
import os


files = [
	"domain_group_memberships.txt",
	"domain_groups.txt",
]


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
		json.dump(data, file, indent=4)

	return json.dumps(data, indent=4)

def append_json_file(filename, data, encoding="utf8"):
	existing_data = read_json_file(filename, encoding=encoding)
	existing_data.append(data)
	write_json_file(filename, existing_data, encoding=encoding)

def reformat_json_to_js(filename, encoding="utf8"):
	json_text = "\n".join(read_file(filename))
	js_text = "var domain_group_memberships = \n" + json_text + ";"
	write_file(filename + ".js", js_text, encoding=encoding)

def finalize(filename):
	reformat_json_to_js(filename)
	print("Done!")
	# print("\n".join(read_file(filename)))

def main():
	members_raw, groups_raw = read_file(files[0]), read_file(files[1])
	members, groups = {}, []

	for group in groups_raw:
		if group.strip().startswith("#"):
			print(group)
			continue
		group = group.split("group:[")[1].split("] rid:")[0]
		members[group] = []
		groups.append(group)

	for member in members_raw:
		if member.strip().startswith("#"):
			print(member)
			continue
		group_name = member.split("Group '")[1].split("' (")[0]
		rid, member_name = member.split("(RID: ")[1].split(") has member: ")
		if group_name not in groups:
			print(f"{group_name}:{member_name} is not in known any groups!")
			continue
		members[group_name].append(
			{
				"member": member_name,
				"group": group_name,
				"rid": rid,
			}
		)

	filename = \
		files[0].replace(
			"."+files[0].rsplit(".", maxsplit=1)[-1],
			".json"
		)
	if os.path.exists(filename):
		remove_file(filename)
	append_json_file(filename, members)
	finalize(filename)


if __name__ == "__main__":
	main()

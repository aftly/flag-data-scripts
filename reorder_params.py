import json
import os

data_DIR = "data"

flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")
flags_dict_all_params_path = os.path.join(data_DIR, "flags_dict_all_params.json")
flags_dict_ordered_all_params_path = os.path.join(data_DIR, "flags_dict_ordered_all_params_new.json")

#with open(flags_dict_names_categories_path, "r") as file:
#    flags_dict = json.load(file)

with open(flags_dict_all_params_path, "r") as file:
    flags_dict = json.load(file)


"""New key order"""
ordered_keys = [
    "wikipedia_en_url",
    "image",
    "flag_from_year",
    "flag_from_year_circa",
    "flag_to_year",
    "flag_to_year_circa",
    "flag_of",
    "flag_of_descriptor",
    "flag_of_official",
    "flag_of_alt_count",
    "flag_of_alt",
    "flag_of_is_the",
    "flag_of_official_is_the",
    "international_organizations",
    "associated_state",
    "sovereign_state",
    "parent_unit",
    "latest_entities",
    "previous_flag_of",
    "category_count",
    "categories"
]

"""Reconstruct dictionary in new order"""
reordered_dict = {}
for flag, info in flags_dict.items():
    reordered_dict[flag] = {}
    reordered_dict[flag] = {key: info[key] for key in ordered_keys}


"""Export flags_dict to JSON"""
with open(flags_dict_ordered_all_params_path, "w") as file:
    json.dump(reordered_dict, file, indent=4)
print(f"\"{flags_dict_ordered_all_params_path}\" exported.")

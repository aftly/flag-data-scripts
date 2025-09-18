import json
import os

data_DIR = "data" # For existing data
exceptions_DIR = "exceptions"
staging_DIR = "staging" # For new data

flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")
#flags_dict_names_categories_path = os.path.join(staging_DIR, "flags_dict_names_categories.json")
flag_image_filenames_path = os.path.join(data_DIR, "flag_image_filenames.json")
#flag_image_filenames_path = os.path.join(staging_DIR, "flag_image_filenames.json")
wiki_page_exceptions_path = os.path.join(exceptions_DIR, "wiki_page_exceptions.json")
#wiki_page_exceptions_path = os.path.join(staging_DIR, "wiki_page_exceptions.json")

with open(flags_dict_names_categories_path, "r") as file:
    flags_dict = json.load(file)
    
with open(flag_image_filenames_path, "r") as file:
    flag_image_filenames = json.load(file)
    
with open(wiki_page_exceptions_path, "r") as file:
    wiki_page_exceptions = json.load(file)


"""Add images from wiki_images dict to flags_dict 'image' parameter"""
for flag, image in flag_image_filenames.items():
    flags_dict[flag]["image"] = image


"""Add wikipedia url param"""
for flag in flags_dict:
    if flag in wiki_page_exceptions:
        flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + wiki_page_exceptions[flag]
    else:
        flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + flag

"""Add miscellaneous params"""
for flag in list(flags_dict):
    try:
        from_year = flags_dict[flag]["flag_from_year"]
    except:
        flags_dict[flag]["flag_from_year"] = None
    try:
        to_year = flags_dict[flag]["flag_to_year"]
    except:
        flags_dict[flag]["flag_to_year"] = None
    try:
        descriptor = flags_dict[flag]["flag_of_descriptor"]
    except:
        flags_dict[flag]["flag_of_descriptor"] = None
    try:
        descriptor = flags_dict[flag]["associated_state"]
    except:
        flags_dict[flag]["associated_state"] = None
    try:
        descriptor = flags_dict[flag]["sovereign_state"]
    except:
        flags_dict[flag]["sovereign_state"] = None
    try:
        descriptor = flags_dict[flag]["parent_unit"]
    except:
        flags_dict[flag]["parent_unit"] = None
    try:
        descriptor = flags_dict[flag]["latest_entities"]
    except:
        flags_dict[flag]["latest_entities"] = []
    try:
        descriptor = flags_dict[flag]["previous_flag_of"]
    except:
        flags_dict[flag]["previous_flag_of"] = None
    try:
        descriptor = flags_dict[flag]["international_organizations"]
    except:
        flags_dict[flag]["international_organizations"] = []


"""----- EXPORT DATA & PARAM JSONs -----"""
with open(flags_dict_all_params_path, "w") as file:
    json.dump(flags_dict, file, indent=4)
print(f"\"{flags_dict_all_params_path}\" exported.")

#with open(flags_dict_all_params_new_path, "w") as file:
#    json.dump(flags_dict, file, indent=4)
#print(f"\"{flags_dict_all_params_new_path}\" exported.")

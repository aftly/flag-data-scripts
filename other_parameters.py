import json
import os

data_DIR = "data" # For existing data
exceptions_DIR = "exceptions"
staging_DIR = "staging" # For new data

flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")
#flags_dict_names_categories_path = os.path.join(staging_DIR, "flags_dict_names_categories.json")
flags_dict_all_params_path = os.path.join(data_DIR, "flags_dict_all_params.json")
#flags_dict_all_params_path = os.path.join(staging_DIR, "flags_dict_all_params.json")
flags_dict_all_params_new_path = os.path.join(data_DIR, "flags_dict_all_params_new.json")

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
for flag, info in list(flags_dict.items()):
    try:
        if info["previous_flag_of"]:
            flags_dict[flag]["wikipedia_en_url"] = None
        elif flag in wiki_page_exceptions:
            flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + wiki_page_exceptions[flag]
        else:
            flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + flag
    except:
        if flag in wiki_page_exceptions:
            flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + wiki_page_exceptions[flag]
        else:
            flags_dict[flag]["wikipedia_en_url"] = "https://en.wikipedia.org/wiki/" + flag

"""Add miscellaneous params"""
for flag, info in list(flags_dict.items()):
    try:
        flag_of = info["flag_of"]
    except:
        flags_dict[flag]["flag_of"] = None
    try:
        flag_of_official = info["flag_of_official"]
    except:
        flags_dict[flag]["flag_of_official"] = None
    try:
        flag_of_alt = info["flag_of_alt"]
    except:
        flags_dict[flag]["flag_of_alt"] = None
    try:
        flag_of_alt_count = info["flag_of_alt_count"]
    except:
        try:
            if info["previous_flag_of"]:
                flags_dict[flag]["flag_of_alt_count"] = None
            else:
                flags_dict[flag]["flag_of_alt_count"] = []
        except:
            flags_dict[flag]["flag_of_alt_count"] = []
    try:
        flag_of_is_the = info["flag_of_is_the"]
    except:
        flags_dict[flag]["flag_of_is_the"] = None
    try:
        flag_of_official_is_the = info["flag_of_official_is_the"]
    except:
        flags_dict[flag]["flag_of_official_is_the"] = None
    try:
        from_year = info["flag_from_year"]
    except:
        flags_dict[flag]["flag_from_year"] = None
    try:
        from_year_circa = info["flag_from_year_circa"]
    except:
        flags_dict[flag]["flag_from_year_circa"] = None
    try:
        to_year = info["flag_to_year"]
    except:
        flags_dict[flag]["flag_to_year"] = None
    try:
        from_to_circa = info["flag_to_year_circa"]
    except:
        flags_dict[flag]["flag_to_year_circa"] = None
    try:
        descriptor = info["flag_of_descriptor"]
    except:
        flags_dict[flag]["flag_of_descriptor"] = None
    try:
        associated = info["associated_state"]
    except:
        flags_dict[flag]["associated_state"] = None
    try:
        sovereign = info["sovereign_state"]
    except:
        flags_dict[flag]["sovereign_state"] = None
    try:
        parent = info["parent_unit"]
    except:
        flags_dict[flag]["parent_unit"] = None
    try:
        latest = info["latest_entities"]
    except:
        try:
            if info["previous_flag_of"]:
                flags_dict[flag]["latest_entities"] = None
            else:
                flags_dict[flag]["latest_entities"] = []
        except:
            flags_dict[flag]["latest_entities"] = []
    try:
        previous = info["previous_flag_of"]
    except:
        flags_dict[flag]["previous_flag_of"] = None
    try:
        international = info["international_organizations"]
    except:
        try:
            if info["previous_flag_of"]:
                flags_dict[flag]["international_organizations"] = None
            else:
                flags_dict[flag]["international_organizations"] = []
        except:
            flags_dict[flag]["international_organizations"] = []


"""----- EXPORT DATA & PARAM JSONs -----"""
with open(flags_dict_all_params_path, "w") as file:
    json.dump(flags_dict, file, indent=4, sort_keys=True)
print(f"\"{flags_dict_all_params_path}\" exported.")

#with open(flags_dict_all_params_new_path, "w") as file:
#    json.dump(flags_dict, file, indent=4, sort_keys=True)
#print(f"\"{flags_dict_all_params_new_path}\" exported.")

import json
import os
import re
import requests

data_DIR = "data"
exceptions_DIR = "exceptions"
staging_DIR = "staging"

flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")
#flags_dict_names_categories_path = os.path.join(staging_DIR, "flags_dict_names_categories.json")
flag_image_filenames_path = os.path.join(data_DIR, "flag_image_filenames.json")
#flag_image_filenames_path = os.path.join(staging_DIR, "flag_image_filenames.json")
#flag_image_filenames_path = os.path.join(staging_DIR, "flag_image_filenames_new.json")
wiki_images_not_found_path = os.path.join(data_DIR, "wiki_images_not_found.json")
#wiki_images_not_found_path = os.path.join(staging_DIR, "wiki_images_not_found.json")
#wiki_images_not_found_path = os.path.join(staging_DIR, "wiki_images_not_found_new.json")
wiki_images_duplicate_path = os.path.join(data_DIR, "wiki_images_duplicate.json")
#wiki_images_duplicate_path = os.path.join(staging_DIR, "wiki_images_duplicate.json")
image_exceptions_path = os.path.join(exceptions_DIR, "image_exceptions.json")
#image_exceptions_path = os.path.join(staging_DIR, "image_exceptions.json")
wiki_page_exceptions_path = os.path.join(exceptions_DIR, "wiki_page_exceptions.json")
#wiki_page_exceptions_path = os.path.join(staging_DIR, "wiki_page_exceptions.json")

"""Input/Output sources"""
with open(flags_dict_names_categories_path, "r") as file:
    flags_dict = json.load(file)

#with open(wiki_images_not_found_path, "r") as file:
#    flags_not_found = json.load(file)
    
with open(image_exceptions_path, "r") as file:
    image_exceptions = json.load(file)
    
with open(wiki_page_exceptions_path, "r") as file:
    page_exceptions = json.load(file)

"""Collections for found and not found images"""
wiki_images = {}
wiki_images_not_found = []
wiki_images_duplicate = {}
flag_strings_main = ["Flag_of", "Bandera_de", "Drapeau_du", "Banner_of"]
flag_strings = ["Flag", "flag", "Bandera", "bandera", "Bandeira", "bandeira", "Drapeau", "drapeau", "Banner", "banner"]

"""Wikipedia API URL"""
API_URL = "https://en.wikipedia.org/w/api.php"

"""Persistent get session during script execution"""
session = requests.Session()
session.headers.update({
    "User-Agent": "Educational purposes"
})

"""Return wikipedia page image filename from title"""
def get_wiki_page_image_free_filename(page):
    params = {
        "action": "query",
        "format": "json",
        "titles": page,
        "redirects": "true",
        "prop": "pageprops",
        "ppprop": "page_image_free"
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    #filename = f"{page}_page_props.json"
    #with open(filename, "w") as file:
    #    json.dump(data, file, indent=4)
    
    try:
        first_page = next(iter(data["query"]["pages"].values()))
        return first_page["pageprops"]["page_image_free"]
    except:
        return None
        

def get_wiki_page_filtered_image(page, flag_info):
    params = {
        "action": "query",
        "format": "json",
        "titles": page,
        "redirects": "true",
        "prop": "images"
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    #filename = f"{page}_images.json"
    #with open(filename, "w") as file:
    #    json.dump(data, file, indent=4)
    
    try:
        first_page = next(iter(data["query"]["pages"].values()))
        starts_with_flags = []
        contains_flags = []
        """Strip bracketed words like '(province)' for match with flag_of"""
        flag_specific = re.sub(r"\s\([^)]*\)", "", flag_info["flag_of"]).replace(" ", "_")
        
        for image_dict in first_page["images"]:
            image = image_dict["title"].replace("File:", "").replace(" ", "_")
            if any(image.startswith(string) for string in flag_strings_main):
                starts_with_flags.append(image)
                
        if len(starts_with_flags) == 1:
            filename = starts_with_flags[0]
            if flag_specific in filename:
                return filename
            elif flag_info["sovereign_state"] not in filename:
                if flag_info["parent_entity"] != None:
                    parent = re.sub(r"_\([^)]*\)", "", flag_info["parent_entity"])
                    if parent not in filename:
                        return filename
                else:
                    return filename
        elif len(starts_with_flags) > 1:
            for filename in starts_with_flags:
                if flag_specific in filename:
                    return filename
                
        for image_dict in first_page["images"]:
            image = image_dict["title"].replace("File:", "").replace(" ", "_")
            if any(string in image for string in flag_strings):
                contains_flags.append(image)
                
        if len(contains_flags) == 1:
            filename = contains_flags[0]
            if flag_info["sovereign_state"] not in filename:
                if flag_info["parent_entity"] != None:
                    parent = re.sub(r"_\([^)]*\)", "", flag_info["parent_entity"])
                    if parent not in filename:
                        return filename
                else:
                    return filename
        elif len(contains_flags) > 1:
            for filename in contains_flags:
                if flag_specific in filename:
                    return filename
                    
        """Try extracting flag filename from get continue"""
        continue_image = next(iter(data["continue"]["imcontinue"]))
        for string in flag_strings_main:
            if string in continue_image and flag_specific in continue_image:
                stripped_image = re.sub(rf"^.*?(?={re.escape(string)})", "", continue_image)
                return stripped_image
                
        return None
    except:
        return None


"""Loop through flags in flags_dict"""
for flag, info in flags_dict.items():
#for flag, info in flags_not_found_dict.items():
    """If flag in image exceptions use exception filename. If in page exceptions, query exception page, else query with flags_dict keys"""
    if flag in image_exceptions:
        image_filename = image_exceptions[flag]
    elif flag in page_exceptions:
        image_filename = get_wiki_page_image_free_filename(page_exceptions[flag])
    else:
        image_filename = get_wiki_page_image_free_filename(flag)
    
    if image_filename:
        page = flag if flag not in page_exceptions else page_exceptions[flag]
        """If wiki page found use primary filename get method"""
        if flag in image_exceptions:
            print(f"{flag} --- Wikipedia image FOUND")
            wiki_images[flag] = image_filename
        elif image_filename.startswith("Flag_of_") or image_filename.startswith("Bandera_de_") or any(string in image_filename for string in flag_strings):
            print(f"{flag} --- Wikipedia image FOUND")
            wiki_images[flag] = image_filename
        else:
            """Use alternative filename get method"""
            image_filename_2 = get_wiki_page_filtered_image(page, info)
            if image_filename_2 != None:
                wiki_images[flag] = image_filename_2
            else:
                """Use original filename get method crudely"""
                
                image_filename_3 = get_wiki_page_image_free_filename("Flag_of_" + page)
                if image_filename_3:
                    print(f"{flag} --- Wikipedia image FOUND")
                    wiki_images[flag] = image_filename_3
                elif any(string in image_filename for string in flag_strings):
                    print(f"{flag} --- Wikipedia image FOUND")
                    wiki_images[flag] = image_filename
                else:
                    wiki_images_not_found.append(flag)
    else:
        wiki_images_not_found.append(flag)
        
    try:
        if wiki_images.values().count(wiki_images[flag]) > 1:
            wiki_images_duplicate[flag] = wiki_images[flag]
    except:
        exceptnothing = None


"""Export wiki_images to .json"""
if wiki_images:
    with open(flag_image_filenames_path, "w") as file:
        json.dump(wiki_images, file, indent=4, sort_keys=True)
    print(f"--- \"{flag_image_filenames_path}\" exported. ---")
else:
    print("--- NO WIKI IMAGES FOUND ---")


"""Export wiki_images_not_found to .json"""
if wiki_images_not_found:
    with open(wiki_images_not_found_path, "w") as file:
        json.dump(wiki_images_not_found, file, indent=4)    
    print(f"--- \"{wiki_images_not_found_path}\" exported. ---")
else:
    print("--- IMAGES FOUND FOR ALL ENTRIES IN FLAGS_DICT ---")


"""Export wiki_images_duplicate to .json"""
if wiki_images_duplicate:
    with open(wiki_images_duplicate_path, "w") as file:
        json.dump(wiki_images_duplicate, file, indent=4)    
    print(f"--- \"{wiki_images_duplicate_path}\" exported. ---")
else:
    print("--- NO IMAGES ARE DUPLICATES ---")

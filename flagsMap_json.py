import json
import os
import re
import unicodedata

data_DIR = "data"
exceptions_DIR = "exceptions"

flags_dict_ordered_all_params_path = os.path.join(data_DIR, "flags_dict_ordered_all_params.json")
svg_exceptions_preview_path = os.path.join(exceptions_DIR, "svg_exceptions_preview.json")
flags_map_path = os.path.join(data_DIR, "flags_map.json")

with open(flags_dict_ordered_all_params_path, "r") as file:
    flags_dict = json.load(file)

with open(svg_exceptions_preview_path, "r") as file:
    svg_exceptions_preview = json.load(file)


def toKotlinKey(key):
    key_whitespace = key.replace("_", " ")
    key_capitalized = key_whitespace.title() # Capitalizes first letter of each word
    key_no_whitespace = key_capitalized.replace(" ", "")
    return key_no_whitespace[0].lower() + key_no_whitespace[1:]
    
flag_id = 0

json_dict = {}

for key, info in flags_dict.items():
    """Reformat flag key to strings resource format"""
    name_res = key.lower().replace("(", "").replace(")", "").replace(".", "").replace(",", "").replace("-", "_").replace("–", "_")
    """Filter out special characters that aren't outputted in Android Studio"""
    image_res = info["image"].replace(".svg", "").replace(".png", "").replace(".jpg", "").replace(".webp", "")
    image_res = image_res.replace("–", "").replace("-", "_").replace(")", "_").replace("(", "_").replace(",", "_").replace(".", "_").replace("'", "_")
    image_res = unicodedata.normalize("NFD", image_res)
    image_res = re.sub(r"([^\W\d_])[\u0300-\u036f]+", "_", image_res)
    image_res = unicodedata.normalize("NFC", image_res)
    image_res = image_res.lower()
    image_res = "_" + image_res[1:] if image_res[0].isdigit() else image_res
    #image_res = re.sub("[-'.,()Åãáéíôóçü]", "_", image_res).lower()

    """Reformat flag key to Kotlin format"""
    new_key = toKotlinKey(key)
    
    flag_id += 1
    
    if key in svg_exceptions_preview:
        preview_append = "_preview"
    else:
        preview_append = ""
        
    flag_view_dict = {}

    #print(f"\"{new_key}\" to FlagResources(")
    
    flag_view_dict["id"] = flag_id
    #print(f"    id = {flag_id},")
    
    if info["wikipedia_en_url"] == None:
        wikipedia_en_url_dict = {}
        wikipedia_en_url_dict["type"] = "StringResSource.Inherit"
        flag_view_dict["wikipediaUrlPath"] = wikipedia_en_url_dict
        #flag_view_dict["wikipediaUrlPath"] = "StringResSource.Inherit"
    else:
        wikipedia_en_url_dict = {}
        wikipedia_en_url_dict["type"] = "StringResSource.Explicit"
        wikipedia_en_url_dict["resName"] = f"{name_res}_wikipedia_url_path"
        flag_view_dict["wikipediaUrlPath"] = wikipedia_en_url_dict
    
    flag_view_dict["image"] = image_res
    flag_view_dict["imagePreview"] = image_res + preview_append
    
    flag_view_dict["fromYear"] = info["flag_from_year"]
    flag_view_dict["fromYearCirca"] = info["flag_from_year_circa"]
    flag_view_dict["toYear"] = info["flag_to_year"]
    flag_view_dict["toYearCirca"] = info["flag_to_year_circa"]
    
    if info["previous_flag_of"] != None:
        flag_of_dict = {}
        flag_of_dict["type"] = "StringResSource.Inherit"
        flag_view_dict["flagOf"] = flag_of_dict
    else:
        flag_of_dict = {}
        flag_of_dict["type"] = "StringResSource.Explicit"
        flag_of_dict["resName"] = name_res
        flag_view_dict["flagOf"] = flag_of_dict
        
    if info["previous_flag_of"] != None:
        flag_of_dict = {}
        flag_of_dict["type"] = "StringResSource.Inherit"
        flag_view_dict["flagOfDescriptor"] = flag_of_dict
    else:
        flag_of_dict = {}
        if info["flag_of_descriptor"] == None:
            flag_of_dict = None
        else:
            flag_of_dict["type"] = "StringResSource.Explicit"
            flag_of_dict["resName"] = f"{name_res}_descriptor"
        flag_view_dict["flagOfDescriptor"] = flag_of_dict
    
    if info["previous_flag_of"] != None:
        flag_of_official_dict = {}
        flag_of_official_dict["type"] = "StringResSource.Inherit"
        flag_view_dict["flagOfOfficial"] = flag_of_official_dict
    else:
        flag_of_official_dict = {}
        flag_of_official_dict["type"] = "StringResSource.Explicit"
        flag_of_official_dict["resName"] = f"{name_res}_official"
        flag_view_dict["flagOfOfficial"] = flag_of_official_dict
    
    if info["previous_flag_of"] != None:
        flag_of_alternate_list_dict = []
        string_inherit_dict = {"type": "StringResSource.Inherit"}
        flag_of_alternate_list_dict.append(string_inherit_dict)
        flag_view_dict["flagOfAlternate"] = flag_of_alternate_list_dict
    elif info["flag_of_alt_count"] == 0:
        flag_view_dict["flagOfAlternate"] = []
    else:
        flag_of_alternate_list_dict = []
        if info["flag_of_alt_count"] == 1:
            string_explicit_dict = {
                "type": "StringResSource.Explicit",
                "resName": f"{name_res}_alt"
            }
            flag_of_alternate_list_dict.append(string_explicit_dict)
        else:
            for i in range(1, info["flag_of_alt_count"] + 1): # Range is exclusive of stop (end) value
                string_explicit_dict = {
                    "type": "StringResSource.Explicit",
                    "resName": f"{name_res}_alt_{i}"
                }
                flag_of_alternate_list_dict.append(string_explicit_dict)
                
        flag_view_dict["flagOfAlternate"] = flag_of_alternate_list_dict
    
    if info["flag_of_is_the"] == None:
        flag_of_is_the_dict = {}
        flag_of_is_the_dict["type"] = "BooleanSource.Inherit"
        flag_view_dict["isFlagOfThe"] = flag_of_is_the_dict
    elif info["flag_of_is_the"]:
        flag_of_is_the_dict = {}
        flag_of_is_the_dict["type"] = "BooleanSource.Explicit"
        flag_of_is_the_dict["bool"] = True
        flag_view_dict["isFlagOfThe"] = flag_of_is_the_dict
    else:
        flag_of_is_the_dict = {}
        flag_of_is_the_dict["type"] = "BooleanSource.Explicit"
        flag_of_is_the_dict["bool"] = False
        flag_view_dict["isFlagOfThe"] = flag_of_is_the_dict
        
    if info["flag_of_official_is_the"] == None:
        flag_of_official_is_the_dict = {}
        flag_of_official_is_the_dict["type"] = "BooleanSource.Inherit"
        flag_view_dict["isFlagOfOfficialThe"] = flag_of_official_is_the_dict
    elif info["flag_of_official_is_the"]:
        flag_of_official_is_the_dict = {}
        flag_of_official_is_the_dict["type"] = "BooleanSource.Explicit"
        flag_of_official_is_the_dict["bool"] = True
        flag_view_dict["isFlagOfOfficialThe"] = flag_of_official_is_the_dict
    else:
        flag_of_official_is_the_dict = {}
        flag_of_official_is_the_dict["type"] = "BooleanSource.Explicit"
        flag_of_official_is_the_dict["bool"] = False
        flag_view_dict["isFlagOfOfficialThe"] = flag_of_official_is_the_dict
        
    international_orgs_list = []
    if info["international_organizations"] != None:
        for flag in info["international_organizations"]:
            international_orgs_list.append(toKotlinKey(flag))
    flag_view_dict["internationalOrganisations"] = international_orgs_list
        
    try:
        flag_view_dict["associatedState"] = toKotlinKey(info["associated_state"])
    except:
        flag_view_dict["associatedState"] = None
    
    try:
        flag_view_dict["sovereignState"] = toKotlinKey(info["sovereign_state"])
    except:
        flag_view_dict["sovereignState"] = None
        
    try:
        flag_view_dict["parentUnit"] = toKotlinKey(info["parent_unit"])
    except:
        flag_view_dict["parentUnit"] = None
        
    latest_entity_list = []
    if info["latest_entities"] != None:
        for flag in info["latest_entities"]:
            latest_entity_list.append(toKotlinKey(flag))
    flag_view_dict["latestEntities"] = latest_entity_list
        
    try:
        flag_view_dict["previousFlagOf"] = toKotlinKey(info["previous_flag_of"])
    except:
        flag_view_dict["previousFlagOf"] = None

    
    categories_upper = [category.upper() for category in info["categories"]]
    flag_view_dict["categories"] = categories_upper
    
    json_dict[f"{new_key}"] = flag_view_dict
    

with open(flags_map_path, "w") as file:
    json.dump(json_dict, file, indent=4)

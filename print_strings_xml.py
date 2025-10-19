import json
import os

data_DIR = "data"

flags_dict_ordered_all_params_path = os.path.join(data_DIR, "flags_dict_ordered_all_params.json")

with open(flags_dict_ordered_all_params_path, "r") as file:
    flags_dict = json.load(file)

"""strings.xml prototypes"""
xml_1 = '<string name="'
xml_2 = '">'
xml_3 = '</string>'

"""Print string res xml entries from flags_dict for relevant strings"""
for key, info in flags_dict.items():
    """Reformat flag key to strings resource format"""
    name_res = key.lower().replace(")", "").replace("(", "").replace(".", "").replace(",", "").replace("-", "_").replace("–", "_")
    
    """flag_of"""
    if info["flag_of"] != None:
        primary_name = info["flag_of"].replace("'", "\\'")
        print(f"{xml_1}{name_res}{xml_2}{primary_name}{xml_3}")
        
    """flag_of_descriptor"""
    if info["flag_of_descriptor"] != None:
        descriptor_name = info["flag_of_descriptor"].replace("'", "\\'")
        print(f"{xml_1}{name_res}_descriptor{xml_2}{descriptor_name}{xml_3}")
    
    """flag_of_official"""
    if info["flag_of_official"] != None:
        official_name = info["flag_of_official"].replace("'", "\\'")
        print(f"{xml_1}{name_res}_official{xml_2}{official_name}{xml_3}")
    
    """wiki_path"""
    if info["wikipedia_en_url"] != None:
        wiki_path = info["wikipedia_en_url"].replace("https://en.wikipedia.org/wiki/", "")
        print(f"{xml_1}{name_res}_wikipedia_url_path{xml_2}{wiki_path}{xml_3}")
    
    """flag_of_alt"""
    if info["flag_of_alt"] and len(info["flag_of_alt"]) != 0:
        if len(info["flag_of_alt"]) == 1:
            alt_name = info["flag_of_alt"][0].replace("'", "\\'").replace("&", "&amp;")
            print(f"{xml_1}{name_res}_alt{xml_2}{alt_name}{xml_3}")
        else:
            for i in range(1, len(info["flag_of_alt"]) + 1): # Range is exclusive of stop (end) value
                alt_name = info["flag_of_alt"][i - 1].replace("'", "\\'").replace("&", "&amp;")
                print(f"{xml_1}{name_res}_alt_{i}{xml_2}{alt_name}{xml_3}")

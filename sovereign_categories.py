from collections import defaultdict
import json
import os

# Example source: https://en.wikipedia.org/wiki/List_of_countries_by_system_of_government

data_DIR = "data"
category_DIR = "category"

flags_dict_categories_path = os.path.join(data_DIR, "flags_dict_categories.json")

sovereign_state_path = os.path.join(category_DIR, "sovereign_state.json")
unitary_path = os.path.join(category_DIR, "unitary.json")
federal_path = os.path.join(category_DIR, "federal.json")
directorial_system_path = os.path.join(category_DIR, "directorial_system.json")
parliamentary_monarchy_path = os.path.join(category_DIR, "parliamentary_monarchy.json")
parliamentary_republic_path = os.path.join(category_DIR, "parliamentary_republic.json")
semi_presidential_republic_path = os.path.join(category_DIR, "semi_presidential_republic.json")
dual_executive_path = os.path.join(category_DIR, "dual_executive.json")
presidential_republic_path = os.path.join(category_DIR, "presidential_republic.json")
socialist_path = os.path.join(category_DIR, "socialist.json")
one_party_state_path = os.path.join(category_DIR, "one_party_state.json")
monarchy_absolute_or_nominally_constitutional_path = os.path.join(category_DIR, "monarchy_absolute_or_nominally_constitutional.json")
theocracy_path = os.path.join(category_DIR, "theocracy.json")
military_junta_path = os.path.join(category_DIR, "military_junta.json")
provisional_government_path = os.path.join(category_DIR, "provisional_government.json")

with open(sovereign_state_path, "r") as file:
    sovereign_state = json.load(file)
with open(unitary_path, "r") as file:
    unitary = json.load(file)
with open(federal_path, "r") as file:
    federal = json.load(file)
with open(directorial_system_path, "r") as file:
    directorial_system = json.load(file)
with open(parliamentary_monarchy_path, "r") as file:
    parliamentary_monarchy = json.load(file)
with open(parliamentary_republic_path, "r") as file:
    parliamentary_republic = json.load(file)
with open(semi_presidential_republic_path, "r") as file:
    semi_presidential_republic = json.load(file)
with open(dual_executive_path, "r") as file:
    dual_executive = json.load(file)
with open(presidential_republic_path, "r") as file:
    presidential_republic = json.load(file)
with open(socialist_path, "r") as file:
    socialist = json.load(file)
with open(one_party_state_path, "r") as file:
    one_party_state = json.load(file)
with open(monarchy_absolute_or_nominally_constitutional_path, "r") as file:
    monarchy_absolute_or_nominally_constitutional = json.load(file)
with open(theocracy_path, "r") as file:
    theocracy = json.load(file)
with open(military_junta_path, "r") as file:
    military_junta = json.load(file)
with open(provisional_government_path, "r") as file:
    provisional_government = json.load(file)

    
cat_dict = {
    # Territorial distribution of power
    "unitary_categories": ["unitary"],
    "federal_categories": ["federal"],
    "confederation_categories": ["confederation"],
    
    # Executive structure and accountability
    "directorial_system_categories": ["directorial", "constitutional", "republic"],
    "parliamentary_monarchy_categories": ["parliamentary", "constitutional", "monarchy"],
    "parliamentary_republic_categories": ["parliamentary", "constitutional", "republic"],
    "semi_presidential_republic_categories": ["semi_presidential", "constitutional", "republic"],
    "dual_executive_categories": ["dual_executive", "republic"],
    "presidential_republic_categories": ["presidential", "constitutional", "republic"],
    
    # Ideological orientation
    "socialist_categories": ["socialist"],
    
    # Power derivation
    "one_party_state_categories": ["one_party"],
    "monarchy_absolute_or_nominally_constitutional_categories": ["monarchy"],
    "theocracy_categories": ["theocracy"],
    "military_junta_categories": ["military_junta"],
    "provisional_government_categories": ["provisional_government"]
}


flag_cat_dict_list = {
    "sovereign_state": sovereign_state,
    "unitary": unitary,
    "federal": federal,
    "directorial_system": directorial_system,
    "parliamentary_monarchy": parliamentary_monarchy,
    "parliamentary_republic": parliamentary_republic,
    "semi_presidential_republic": semi_presidential_republic,
    "dual_executive": dual_executive,
    "presidential_republic": presidential_republic,
    "socialist": socialist,
    "one_party_state": one_party_state,
    "monarchy_absolute_or_nominally_constitutional": monarchy_absolute_or_nominally_constitutional,
    "theocracy": theocracy,
    "military_junta": military_junta,
    "provisional_government": provisional_government
}

    
flags_dict = defaultdict(lambda: defaultdict(list))

"""Loop through flag lists in categories dict list "flag_cat_dict_list" and assign flags to new dict "flags_dict" with the corresponding categories"""
for category, flags in flag_cat_dict_list.items():
    for flag in flags:
        """Extend the flag's categories list from the category + '_categories' list in cat_dict"""
        flags_dict[flag]["categories"].extend(cat_dict[category + "_categories"])
        
        """Ensure no duplicate entries"""
        list_temp = flags_dict[flag]["categories"]
        unique_list = list(dict.fromkeys(list_temp))
        flags_dict[flag]["categories"] = unique_list
        
        """Remove 'constitutional' category entry if also has 'one_party', 'theocracy', 'military_junta' or 'provisional_government' category entry"""
        if any(i in flags_dict[flag]["categories"] for i in ("one_party", "theocracy", "military_junta", "provisional_government")) and "constitutional" in flags_dict[flag]["categories"]:
            flags_dict[flag]["categories"].remove("constitutional")
            
        """Remove 'constitutional' category entry if flag also in cat_dict["monarchy_absolute_or_nominally_constitutional"] list"""
        if flag in flag_cat_dict_list["monarchy_absolute_or_nominally_constitutional"] and "constitutional" in flags_dict[flag]["categories"]:
            flags_dict[flag]["categories"].remove("constitutional")
            
        """Remove 'republic' category entry if also has 'one_party', 'theocracy', 'military_junta' or 'provisional_government' category entry"""
        if any(i in flags_dict[flag]["categories"] for i in ("one_party", "theocracy", "military_junta", "provisional_government")) and "republic" in flags_dict[flag]["categories"]:
            flags_dict[flag]["categories"].remove("republic")
            
        """Remove 'republic' category entry if flag also in cat_dict["monarchy_absolute_or_nominally_constitutional"] list"""
        if flag in flag_cat_dict_list["monarchy_absolute_or_nominally_constitutional"] and "republic" in flags_dict[flag]["categories"]:
            flags_dict[flag]["categories"].remove("republic")


"""Add each flag's cat count to cat count key"""
for flag in flags_dict:
    flags_dict[flag]["category_count"] = len(flags_dict[flag]["categories"])


"""Export flags_dict to .json"""
with open(flags_dict_categories_path, "w") as file:
    json.dump(flags_dict, file, indent=4, sort_keys=True)
print(f"\"{flags_dict_categories_path}\" exported.")

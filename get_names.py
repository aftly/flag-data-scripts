import json
import os
import re
import requests

"""Set paths for input sources"""
data_DIR = "data" # For existing data
exceptions_DIR = "exceptions"
staging_DIR = "staging" # For new data

flags_dict_categories_path = os.path.join(data_DIR, "flags_dict_categories.json")
#flags_dict_categories_path = os.path.join(staging_DIR, "flags_dict_categories.json")
flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")
#flags_dict_names_categories_path = os.path.join(staging_DIR, "flags_dict_names_categories.json")

alias_exceptions_path = os.path.join(exceptions_DIR, "alias_exceptions.json")
label_exceptions_path = os.path.join(exceptions_DIR, "label_exceptions.json")
#label_exceptions_path = os.path.join(staging_DIR, "label_exceptions.json")
official_name_exceptions_path = os.path.join(exceptions_DIR, "official_name_exceptions.json")
flag_of_is_the_exceptions_path = os.path.join(exceptions_DIR, "flag_of_is_the_exceptions.json")
flag_of_official_is_the_exceptions_path = os.path.join(exceptions_DIR, "flag_of_official_is_the_exceptions.json")
wiki_page_exceptions_path = os.path.join(exceptions_DIR, "wiki_page_exceptions.json")
#wiki_page_exceptions_path = os.path.join(staging_DIR, "wiki_page_exceptions.json")

"""Input/Output sources"""
with open(flags_dict_categories_path, "r") as file:
    flags_dict = json.load(file)

with open(alias_exceptions_path, "r") as file:
    alias_exceptions = json.load(file)
    
with open(label_exceptions_path, "r") as file:
    label_exceptions = json.load(file)

with open(official_name_exceptions_path, "r") as file:
    official_name_exceptions = json.load(file)
    
with open(flag_of_is_the_exceptions_path, "r") as file:
    flag_of_is_the_exceptions = json.load(file)
    
with open(flag_of_official_is_the_exceptions_path, "r") as file:
    flag_of_official_is_the_exceptions = json.load(file)
    
with open(wiki_page_exceptions_path, "r") as file:
    wiki_page_exceptions = json.load(file)


"""Wikipedia API URL"""
API_URL = "https://en.wikipedia.org/w/api.php"

"""Persistent get session during script execution"""
session = requests.Session()
session.headers.update({
    "User-Agent": "Educational purposes"
})

"""For replacing standard apostrophe ' in flag_of and flag_of_official names"""
curly_apostrophe = "’"

"""Saving presence of 'the' before first bold name, or before the bold names of relevant subsequent bold names when they are shorter"""
flag_of_is_the = False
flag_of_official_is_the = False

def return_official_name_from_wiki_intro(page):
    global flag_of_is_the
    global flag_of_official_is_the
    flag_of_is_the = False
    flag_of_official_is_the = False
    first_bold_name_is_the = False
    subsequent_bold_name_is_the = False
    
    """Get first sentence of info from wiki page"""
    params = {
        "action": "query",
        "format": "json",
        "titles": page,
        "redirects": "true",
        "prop": "extracts",
        "exsentences": 1  # Gets first sentence from wiki page (intro)
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    #filename = f"{page}.json"
    #with open(filename, "w") as file:
    #    json.dump(data, file, indent=4)
    
    try:
        first_page = next(iter(data["query"]["pages"].values()))
        intro_html = first_page["extract"]
    except:
        print(f"----- ERROR: {page} --- when querying API for Wikipedia page first sentence string")
        return None

    """return string enclosed between first <b> & </b> after 'officially' or 'formally' if present, else return None""" 
    keyword1 = " officially "
    keyword2 = " formally "
    keyword3 = " or the "
    keyword4 = " also known as the "
    keyword5 = " also the "
    match1 = re.search(re.escape(keyword1), intro_html)
    match2 = re.search(re.escape(keyword2), intro_html)
    match3 = re.search(re.escape(keyword3), intro_html)
    match4 = re.search(re.escape(keyword4), intro_html)
    match5 = re.search(re.escape(keyword5), intro_html)
    
    """Check if first boldname is preceded by 'The ' and set flag_of_is_the variable as True if so"""
    extractions_the = re.finditer(r"The\s<b>", intro_html[0:])
    try:
        first_match_object = next(extractions_the)
        if first_match_object.group(0):
            flag_of_is_the = True
            flag_of_official_is_the = True
            first_bold_name_is_the = True
            #print(f"INITIAL 'the' --- FOUND for --- {page}")
    except:
        #print(f"INITIAL 'the' --- NOT found for --- {page}")
    
    """Iteratively check matches to determine official name"""
    if match1:
        start_index = match1.end()
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html[start_index:])
        try:
            first_match_object = next(extractions)
            """If extracted value, check for if preceded by 'the' """
            if first_match_object.group(1):
                the_index = start_index - 2
                extractions_the = re.finditer(r"\sthe\s<b>", intro_html[the_index:])
                try:
                    first_match_object_2 = next(extractions_the)
                    if first_match_object_2.group(0):
                        flag_of_official_is_the = True
                        #print(f"OFFICIAL name 'the' --- FOUND for --- {page}")
                    else:
                        flag_of_official_is_the = False
                        #print(f"OFFICIAL name 'the' --- NOT found for --- {page}")
                except:
                    flag_of_official_is_the = False
                    #print(f"OFFICIAL name 'the' --- NOT found for --- {page}")
                    
            """Try returning extracted value"""
            return first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")

    elif match2:
        start_index = match2.end()
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html[start_index:])
        try:
            first_match_object = next(extractions)
            """If extracted value, check for if preceded by 'the' """
            if first_match_object.group(1):
                the_index = start_index - 2
                extractions_the = re.finditer(r"\sthe\s<b>", intro_html[the_index:])
                try:
                    first_match_object_2 = next(extractions_the)
                    if first_match_object_2.group(0):
                        flag_of_official_is_the = True
                        #print(f"OFFICIAL name 'the' --- FOUND for --- {page}")
                    else:
                        flag_of_official_is_the = False
                        #print(f"OFFICIAL name 'the' --- NOT found for --- {page}")
                except:
                    flag_of_official_is_the = False
                    #print(f"OFFICIAL name 'the' --- NOT found for --- {page}")
                    
            """Try returning extracted value"""
            return first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
    elif match3:
        start_index = match3.end()
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html[start_index:])
        try:
            first_match_object = next(extractions)
            name3 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
        """Get first bold name for comparison"""
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html)
        try:
            first_match_object = next(extractions)
            name1 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
        """Try getting ' the ' from before match3"""
        the_index = start_index - 6
        extractions_the = re.finditer(r"\sthe\s<b>", intro_html[the_index:])
        try:
            first_match_object = next(extractions_the)
            if first_match_object.group(0):
                subsequent_bold_name_is_the = True
            #print(f"SUBSEQUENT 'the' --- FOUND for --- {page}")
        except:
            #print(f"SUBSEQUENT 'the' --- NOT found for --- {page}")
        
        """Return the longer of the extracted names since longer length more likely to mean official/formal name"""
        try:
            if len(name3) > len(name1):
                """If name3 is longer (ie. official), return name3. If preceded by 'the', official name is 'the'."""
                if subsequent_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                    
                return name3
            else:
                """If name3 is not longer (ie. not official), return (presumed official) name1."""
                """If (official) name1 preceded by 'the', official name is 'the'."""
                """If (not official) name3 is preceded by 'the', unofficial name is 'the'."""
                """NOTE: official_is_the operations may be redundant here since are set before 'if match(n)' operations"""
                if first_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                
                if subsequent_bold_name_is_the:
                    flag_of_is_the = True
                else:
                    flag_of_is_the = False
                    
                return name1
        except:
            try:
                """If name3 has value, official name is 'the'."""
                if name3:
                    if subsequent_bold_name_is_the:
                        flag_of_official_is_the = True
                    else:
                        flag_of_official_is_the = False
                        
                return name3
            except:
                print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
    
    elif match4:
        start_index = match4.end()
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html[start_index:])
        try:
            first_match_object = next(extractions)
            name4 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
        """Get first bold name for comparison"""
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html)
        try:
            first_match_object = next(extractions)
            name1 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
         
        """Try getting ' the ' from before match3"""
        the_index = start_index - 6
        extractions_the = re.finditer(r"\sthe\s<b>", intro_html[the_index:])
        try:
            first_match_object = next(extractions_the)
            if first_match_object.group(0):
                subsequent_bold_name_is_the = True
            #print(f"SUBSEQUENT 'the' --- FOUND for --- {page}")
        except:
            #print(f"SUBSEQUENT 'the' --- NOT found for --- {page}")
        
        """Return the longer of the extracted names since longer length more likely to mean official/formal name"""
        try:
            if len(name4) > len(name1):
                """If name4 is longer (ie. official), return name4. If preceded by 'the', official name is 'the'."""
                if subsequent_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                    
                return name4
            else:
                """If name4 is not longer (ie. not official), return (presumed official) name1."""
                """If (official) name1 preceded by 'the', official name is 'the'."""
                """If (not official) name4 is preceded by 'the', unofficial name is 'the'."""
                """NOTE: official_is_the operations may be redundant here since are set before 'if match(n)' operations"""
                if first_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                
                if subsequent_bold_name_is_the:
                    flag_of_is_the = True
                else:
                    flag_of_is_the = False
                    
                return name1
        except:
            try:
                """If name4 has value, official name is 'the'."""
                if name4:
                    if subsequent_bold_name_is_the:
                        flag_of_official_is_the = True
                    else:
                        flag_of_official_is_the = False
                        
                return name4
            except:
                print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
                
    elif match5:
        start_index = match5.end()
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html[start_index:])
        try:
            first_match_object = next(extractions)
            name5 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
        """Get first bold name for comparison"""
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html)
        try:
            first_match_object = next(extractions)
            name1 = first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            
        """Try getting ' the ' from before match3"""
        the_index = start_index - 6
        extractions_the = re.finditer(r"\sthe\s<b>", intro_html[the_index:])
        try:
            first_match_object = next(extractions_the)
            if first_match_object.group(0):
                subsequent_bold_name_is_the = True
            #print(f"SUBSEQUENT 'the' --- FOUND for --- {page}")
        except:
            #print(f"SUBSEQUENT 'the' --- NOT found for --- {page}")
            
        """Return the longer of the extracted names since longer length more likely to mean official/formal name"""
        try:
            if len(name5) > len(name1):
                """If name5 is longer (ie. official), return name5. If preceded by 'the', official name is 'the'."""
                if subsequent_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                    
                return name5
            else:
                """If name5 is not longer (ie. not official), return (presumed official) name1."""
                """If (official) name1 preceded by 'the', official name is 'the'."""
                """If (not official) name5 is preceded by 'the', unofficial name is 'the'."""
                """NOTE: official_is_the operations may be redundant here since are set before 'if match(n)' operations"""
                if first_bold_name_is_the:
                    flag_of_official_is_the = True
                else:
                    flag_of_official_is_the = False
                
                if subsequent_bold_name_is_the:
                    flag_of_is_the = True
                else:
                    flag_of_is_the = False
                    
                return name1
        except:
            try:
                """If name5 has value, official name is 'the'."""
                if name5:
                    if subsequent_bold_name_is_the:
                        flag_of_official_is_the = True
                    else:
                        flag_of_official_is_the = False
                        
                return name5
            except:
                print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
    
    else:
        extractions = re.finditer(r"<b>(.*?)</b>", intro_html)
        try:
            first_match_object = next(extractions)
            return first_match_object.group(1)
        except:
            print(f"----- ERROR: {flag} --- when extracting (bold) name from Wikipedia page intro string. --- Extraction list = {list(extractions)}")
            return None
    


"""Query wikipedia API for page label and aliases and return the GET JSON"""
def return_wiki_label_aliases_get(page):
    params = {
        "action": "query",
        "format": "json",
        "titles": page,
        "redirects": "true",
        "prop": "pageterms",
        "wbptlanguage": "en",
        "wbptterms": "label|alias"
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    #filename = f"{page}_label_alias.json"
    #with open(filename, "w") as file:
    #    json.dump(data, file, indent=4)
    
    if response.status_code == 200:
        return data
    else:
        print(f"----- ERROR: {page} --- API query for Wikipedia page labels and aliases")
        return None


"""From the GET JSON return the page's label (official name)"""
def return_label(data, page):
    try:
        first_page = next(iter(data["query"]["pages"].values()))
        return first_page["terms"]["label"][0]
    except:
        print(f"----- ERROR: {page} --- Wiki label not found")


"""From the GET JSON return the page's aliases (secondary names)"""
def return_aliases(data, page):
    try:
        first_page = next(iter(data["query"]["pages"].values()))
        return first_page["terms"]["alias"]
    except:
        print(f"----- ERROR: {page} --- Wiki aliases not found")


"""Loop through flags_dict and get and set names extracted from wikipedia, then export updated flags_dict to JSON"""
for flag in flags_dict:
    """Initialise flag_of_alt"""
    flags_dict[flag]["flag_of_alt"] = []

    """Get relevant info from queries"""
    if flag in wiki_page_exceptions:
        page_exception = wiki_page_exceptions[flag]
        official_name = return_official_name_from_wiki_intro(page_exception)
        label_aliases_data = return_wiki_label_aliases_get(page_exception)
    else:
        official_name = return_official_name_from_wiki_intro(flag)
        label_aliases_data = return_wiki_label_aliases_get(flag)
        
    label = return_label(label_aliases_data, flag)
    aliases = return_aliases(label_aliases_data, flag)

    """Set flag_of_is_the param since return_official_name_from_wiki_intro() modifies flag_of_is_the value"""
    flags_dict[flag]["flag_of_is_the"] = flag_of_is_the
    flags_dict[flag]["flag_of_official_is_the"] = flag_of_official_is_the
    
    """If queries are not null, add info flags_dict, else add to respective not_found list"""
    """If flag in label exception list use exception, else follow regular protocol"""
    if flag in label_exceptions:
        flags_dict[flag]["flag_of"] = label_exceptions[flag]
        try:
            flags_dict[flag]["flag_of_is_the"] = flag_of_is_the_exceptions[flag]
        except:
            print(f"--- {flag} NOT found in LABEL_IS_THE_EXCEPTIONS dict. Independently ensure is_the parameter is correct ---")
    elif label:
        """If key in label set flag_of to key (as label will likely be official name)"""
        if flag in label:
            label = flag.replace("_", " ")   
        flags_dict[flag]["flag_of"] = label.replace("'", curly_apostrophe)
    else:
        print(f"----- ERROR: {flag} --- Wikipedia label not found --- SETTING flag_of name to FLAG KEY with whitespace.")
        flags_dict[flag]["flag_of"] = flag.replace("_", " ")
        
    
    """If flag in official name exception list use exception, else follow regular protocol"""
    if flag in official_name_exceptions:
        flags_dict[flag]["flag_of_official"] = official_name_exceptions[flag]
        try:
            flags_dict[flag]["flag_of_official_is_the"] = flag_of_official_is_the_exceptions[flag]
        except:
            print(f"--- {flag} NOT found in OFFICIAL_NAME_IS_THE_EXCEPTIONS dict. Independently ensure is_the parameter is correct ---")
    elif official_name:
        official_name = official_name.replace("'", curly_apostrophe)
        flags_dict[flag]["flag_of_official"] = official_name
    elif label:
        print(f"----- ERROR: {flag} --- Wikipedia intro BOLD name not found --- SETTING official name to PRIMARY (label) name.")
        flags_dict[flag]["flag_of_official"] = flags_dict[flag]["flag_of"]
        
    
    if flag in alias_exceptions:
        flags_dict[flag]["flag_of_alt"] = alias_exceptions[flag]
    elif aliases:
        flags_dict[flag]["flag_of_alt"] = aliases


with open(flags_dict_names_categories_path, "w") as file:
    json.dump(flags_dict, file, indent=4, sort_keys=True)
print(f"----- \"{flags_dict_names_categories_path}\" exported. -----")

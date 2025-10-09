import json
import re
import os

data_DIR = "data"
category_DIR = "category"
exceptions_DIR = "exceptions"
staging_DIR = "staging"

flags_dict_names_categories_path = os.path.join(data_DIR, "flags_dict_names_categories.json")

flags_dict_all_params_path = os.path.join(data_DIR, "flags_dict_all_params.json")
flags_dict_all_params_new_path = os.path.join(data_DIR, "flags_dict_all_params_new.json")
flags_dict_ordered_all_params_path = os.path.join(data_DIR, "flags_dict_ordered_all_params.json")
flag_image_filenames_path = os.path.join(data_DIR, "flag_image_filenames.json")
flag_image_filenames_new_path = os.path.join(data_DIR, "flag_image_filenames_new.json")
flag_image_filenames_select_new_path = os.path.join(data_DIR, "flag_image_filenames_select_new.json")

flag_of_is_the_exceptions_path = os.path.join(exceptions_DIR, "flag_of_is_the_exceptions.json")
flag_of_is_the_exceptions_new_path = os.path.join(exceptions_DIR, "flag_of_is_the_exceptions_new.json")
flag_of_official_is_the_exceptions_path = os.path.join(exceptions_DIR, "flag_of_official_is_the_exceptions.json")
flag_of_official_is_the_exceptions_new_path = os.path.join(exceptions_DIR, "flag_of_official_is_the_exceptions_new.json")
label_exceptions_path = os.path.join(exceptions_DIR, "label_exceptions.json")
label_exceptions_new_path = os.path.join(exceptions_DIR, "label_exceptions_new.json")
alias_exceptions_path = os.path.join(exceptions_DIR, "alias_exceptions.json")
alias_exceptions_new_path = os.path.join(exceptions_DIR, "alias_exceptions_new.json")
wiki_page_exceptions_path = os.path.join(exceptions_DIR, "wiki_page_exceptions.json")
wiki_page_exceptions_new_path = os.path.join(exceptions_DIR, "wiki_page_exceptions_new.json")
image_exceptions_path = os.path.join(exceptions_DIR, "image_exceptions.json")
image_exceptions_new_path = os.path.join(exceptions_DIR, "image_exceptions_new.json")
svg_exceptions_path = os.path.join(exceptions_DIR, "svg_exceptions.json")
svg_exceptions_new_path = os.path.join(exceptions_DIR, "svg_exceptions_new.json")
svg_exceptions_android_path = os.path.join(exceptions_DIR, "svg_exceptions_android.json")
svg_exceptions_android_new_path = os.path.join(exceptions_DIR, "svg_exceptions_android_new.json")
svg_exceptions_preview_path = os.path.join(exceptions_DIR, "svg_exceptions_preview.json")
svg_exceptions_preview_new_path = os.path.join(exceptions_DIR, "svg_exceptions_preview_new.json")

flag_image_download_failed_path = os.path.join(staging_DIR, "flag_image_download_failed.json")


#with open(flags_dict_names_categories_path, "r") as file:
#    flags_dict = json.load(file)
    
#with open(flags_dict_ordered_all_params_path, "r") as file:
#    flags_dict = json.load(file)
    
with open(flags_dict_all_params_path, "r") as file:
    flags_dict = json.load(file)
    
with open(flag_image_filenames_path, "r") as file:
    flag_image_filenames = json.load(file)   
    
#with open(flag_image_download_failed_path, "r") as file:
#    flag_image_download_failed = json.load(file)
    
with open(flag_of_is_the_exceptions_path, "r") as file:
    flag_of_is_the_exceptions = json.load(file)
    
with open(flag_of_official_is_the_exceptions_path, "r") as file:
    flag_of_official_is_the_exceptions = json.load(file)
    
with open(label_exceptions_path, "r") as file:
    label_exceptions = json.load(file)
    
with open(alias_exceptions_path, "r") as file:
    alias_exceptions = json.load(file)

with open(wiki_page_exceptions_path, "r") as file:
    wiki_page_exceptions = json.load(file)
 
with open(image_exceptions_path, "r") as file:
    image_exceptions = json.load(file)

with open(svg_exceptions_path, "r") as file:
    svg_exceptions = json.load(file)
    
with open(svg_exceptions_android_path, "r") as file:
    svg_exceptions_android = json.load(file)
    
with open(svg_exceptions_preview_path, "r") as file:
    svg_exceptions_preview = json.load(file)



#with open(flags_dict_all_params_new_path, "w") as file:
#    json.dump(flags_dict, file, indent=4, sort_keys=True)
    
#with open(flag_image_filenames_new_path, "w") as file:
#    json.dump(flag_image_filenames, file, indent=4, sort_keys=True)

#with open(flag_image_filenames_select_new_path, "w") as file:
#    json.dump(flag_image_filenames_select, file, indent=4, sort_keys=True)

#with open(flag_of_is_the_exceptions_new_path, "w") as file:
#    json.dump(flag_of_is_the_exceptions, file, indent=4, sort_keys=True)

#with open(flag_of_official_is_the_exceptions_new_path, "w") as file:
#    json.dump(flag_of_official_is_the_exceptions, file, indent=4, sort_keys=True)

#with open(label_exceptions_new_path, "w") as file:
#    json.dump(label_exceptions, file, indent=4, sort_keys=True)

#with open(alias_exceptions_new_path, "w") as file:
#    json.dump(alias_exceptions, file, indent=4, sort_keys=True)
    
#with open(image_exceptions_new_path, "w") as file:
#    json.dump(image_exceptions, file, indent=4, sort_keys=True)    
    
#with open(svg_exceptions_new_path, "w") as file:
#    json.dump(svg_exceptions, file, indent=4)

#with open(svg_exceptions_android_new_path, "w") as file:
#    json.dump(svg_exceptions_android, file, indent=4)

#with open(svg_exceptions_preview_new_path, "w") as file:
#    json.dump(svg_exceptions_preview, file, indent=4)

#with open(wiki_page_exceptions_new_path, "w") as file:
#    json.dump(wiki_page_exceptions, file, indent=4, sort_keys=True)

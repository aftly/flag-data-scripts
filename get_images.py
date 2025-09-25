import requests
import os
import json
import time

"""Set paths for input/output"""
data_DIR = "data" # For existing data
exceptions_DIR = "exceptions"
image_DIR = "image"
staging_DIR = "staging" # For new data
os.makedirs(image_DIR, exist_ok=True)

flag_filenames_path = os.path.join(data_DIR, "flag_image_filenames.json")
#flag_filenames_path = os.path.join(staging_DIR, "flag_image_filenames.json")
flag_filenames_select_path = os.path.join(data_DIR, "flag_image_filenames_select.json")
flag_image_download_failed_path = os.path.join(image_DIR, "flag_image_download_failed.json")
#flag_image_download_failed_path = os.path.join(staging_DIR, "flag_image_download_failed.json")
thumburl_not_found_path = os.path.join(image_DIR, "thumburl_not_found.json")
#thumburl_not_found_path = os.path.join(staging_DIR, "thumburl_not_found.json")

svg_exceptions_path = os.path.join(exceptions_DIR, "svg_exceptions.json")
#svg_exceptions_path = os.path.join(staging_DIR, "svg_exceptions.json")
svg_exceptions_android_path = os.path.join(exceptions_DIR, "svg_exceptions_android.json")
svg_exceptions_preview_path = os.path.join(exceptions_DIR, "svg_exceptions_preview.json")
#svg_exceptions_preview_path = os.path.join(staging_DIR, "svg_exceptions_preview.json")


"""Import flag image filenames to query Wikimedia Commons API for full image URLs"""
with open(flag_filenames_path, "r") as file:
    flag_filenames = json.load(file)
#with open(flag_filenames_select_path, "r") as file:
#    flag_filenames = json.load(file)
    
"""Uncomment to retry downloads of failed images"""
#with open(flag_image_download_failed_path, "r") as file:
#    flag_filenames = json.load(file)

"""List of flags with global rendering issues or size > 500kb, to instead be downloaded as .png"""
with open(svg_exceptions_path, "r") as file:
    svg_exceptions = json.load(file)

"""For vectors with rendering issues on Android"""
with open(svg_exceptions_android_path, "r") as file:
    svg_exceptions_android = json.load(file)

"""For vectors above 50kb, unsuitable for use as preview images"""
with open(svg_exceptions_preview_path, "r") as file:
    svg_exceptions_preview = json.load(file)


"""Wikimedia Commons API URL"""
API_URL = "https://commons.wikimedia.org/w/api.php"

"""Persistent get session during script execution"""
session = requests.Session()
session.headers.update({
    "User-Agent": "Educational purposes"
})

"""Dict for failed downloads"""
failed_to_download = {}
thumburl_not_found = {}


def get_image_url(image_filename):
    """Fetch original file URL from it's corresponding Commons filename"""
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": f"File:{image_filename}"
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            return page["imageinfo"][0]["url"]
            
    print(f"----- ERROR: {image_filename} : *url* not found")
    return None
    

def get_image_thumburl(image_filename, width):
    # Example (common) widths: 2560, 1280, 320 (318 for Denmark)
    """Fetch original file URL from it's corresponding Commons filename"""
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": f"{width}",
        "titles": f"File:{image_filename}"
    }
    response = session.get(API_URL, params=params)
    data = response.json()
    
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            return page["imageinfo"][0]["thumburl"]
            
    print(f"----- ERROR: {image_filename} : {width}px width *thumburl* not found")
    return None


def download_flag(url, filename, flag):
    """Downloads flag and saves it to specified directory"""
    response = session.get(url)
    if response.status_code == 200:
        filepath = os.path.join(image_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        if "_preview" in filename:
            failed_to_download[flag] = filename.replace("_preview.png", ".svg")
        else:
            failed_to_download[flag] = filename.replace(".png", ".svg")
        print(f"--- ERROR: {filename} failed to download ---")
        
    """Add delay"""
    time.sleep(0.25)
        

"""Loop through flag_filenames, query image URLs then download found images"""
for flag, filename in flag_filenames.items():
    """Get detailed image"""
    if flag in svg_exceptions or flag in svg_exceptions_android:
        image_url = get_image_thumburl(filename, 2560)
    else:
        image_url = get_image_url(filename)
    
    if image_url:
        if flag in svg_exceptions or flag in svg_exceptions_android:
            download_flag(image_url, filename.replace(".svg", ".png"), flag)
        else:
            download_flag(image_url, filename, flag)

    """Get preview_image"""
    if flag in svg_exceptions_preview:
        image_url_preview = get_image_thumburl(filename, 320)
        if image_url_preview:
            download_flag(image_url_preview, filename.replace(".svg", "_preview.png"), flag)
        else:
            thumburl_not_found[flag] = 320
            image_url_preview = get_image_thumburl(filename, 318)
            if image_url_preview:
                del thumburl_not_found[flag]
                download_flag(image_url_preview, filename.replace(".svg", "_preview.png"), flag)
            else:
                thumburl_not_found[flag] = 318
                image_url_preview = get_image_thumburl(filename, 305)
                if image_url_preview:
                    del thumburl_not_found[flag]
                    download_flag(image_url_preview, filename.replace(".svg", "_preview.png"), flag)
                else:
                    thumburl_not_found[flag] = 305


print("------------ DOWNLOADS FINISHED ------------")
print("-> If flags failed to download try changing the user-agent, uncommenting failed downloads JSON and re-executing script.")



"""Export flags that failed to download to JSON"""
with open(flag_image_download_failed_path, "w") as file:
    json.dump(failed_to_download, file, indent=4, sort_keys=True)
print(f"--- \"{flag_image_download_failed_path}\" exported. ---")

"""Export flags whose thumburls were not found to JSON"""
with open(thumburl_not_found_path, "w") as file:
    json.dump(thumburl_not_found, file, indent=4, sort_keys=True)
print(f"--- \"{thumburl_not_found_path}\" exported. ---")

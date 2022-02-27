from argparse import ArgumentError
import os, bs4, requests, sys
from time import sleep
from random import random

def main():
    if (len(sys.argv) < 2):
        raise ArgumentError("Too few command line arguments passed to script (at least 1 expected)")
    rawUrls = sys.argv[1:]
    urls = []
    flags = {
        "new-folder": False,
        "path": None
    }
    for rawUrl in rawUrls:
        if rawUrl[:6] == "-path=":
            if os.access(rawUrl.split("=")[1], os.W_OK):
                flags["path"] = rawUrl.split("=")[1]
        elif rawUrl[:12] == "-new_folder=":
            if rawUrl.split("=")[1].lower() == "true":
                flags["new-folder"] = True
            else:
                flags["new-folder"] = False
        else:
            urls.append(rawUrl)
    if flags["path"] == None:
        flags["path"] = os.getcwd()

    for url in urls:
        scrape_images(url, flags)

def scrape_images(url, flags):
    folder_path = flags["path"]
    if flags["new-folder"] == True:
        chunks = url.split(".")
        folder_name = chunks[max(0, len(chunks)-2)]
        fol_ver = 1
        while os.access(f"{flags['path']}/{folder_name}_{fol_ver}", os.W_OK):
            fol_ver += 1
        os.mkdir(f"{flags['path']}/{folder_name}_{fol_ver}")
        folder_path = f"{flags['path']}/{folder_name}_{fol_ver}"
    page = requests.get(url).text
    bowl = bs4.BeautifulSoup(page, "html.parser") # a bowl of soup, perhaps?
    bowl_images = bowl.findAll("img")
    bowl_len = len(bowl_images)
    index = 1
    for image in bowl_images:
        img_src = ""
        if image.has_attr("src"):
            img_src = image["src"]
        elif image.has_attr("data-src"):
            img_src = image["data-src"]
        elif image.has_attr("data-image"):
            img_src = image["data-image"]
        else:
            print(f"Could not retrieve src attribute for img tag: {image}")
            index += 1
            continue
        img_src = img_src.split("?")[0]
        if img_src[:6] != "https:":
            img_src = f"https:{img_src}"
        img_req = requests.get(img_src)
        img_chunks = img_src.split("/")
        img_name = img_chunks[len(img_chunks)-1]
        with open(f"{folder_path}/{img_name}", "wb") as img_write:
            img_write.write(img_req.content)
            print(f"Wrote image {index} of {bowl_len} to {folder_path}/{img_name}")
        sleep(round(random(), 2))
        index += 1

if __name__ == "__main__":
    main()
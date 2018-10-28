import re
import requests
import logging
import argparse
import sys
import os
import time
from threading import Thread

logging.basicConfig(filename="markdown-link-checker.log", format="%(asctime)-15s %(levelname)-8s %(message)s")
log = logging.getLogger("__main__")
log.setLevel(logging.INFO)

def create_argparse():
    app_desc = """
        This application tests hyperlinks within a user-specified Markdown file \
        to see if they are accessible, as well as checks to see if they can be \
        accessed via HTTPS instead of HTTP.
    """
    parse = argparse.ArgumentParser(description=app_desc)
    parse.add_argument("markdownFile", help="Filepath to Markdown file to be tested")
    parse.add_argument("--debug", help="Enable debug logging", action="store_true")
    return parse

def fetch_url(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
    except requests.exceptions.ConnectionError:
        log.error("[%s] Timed out while accessing URL", url)
        return False
    if res.status_code != 200:
        if res.status_code == 503:
            log.warning("[%s] 503 encountered, trying three more times...", url)
            attempts = 3
            while attempts > 0:
                time.sleep(1)
                log.warning("[%s] Attempt #%s...", url, 4 - attempts)
                new_res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
                if new_res.status_code != 200:
                    attempts -= 1
                    log.warning("[%s] Attempt failed!", url)
                else:
                    return True
        log.error("[%s] Issue with URL | Code: %s", url, res.status_code)
        log.debug("[%s] Contents: %s", url, res.text)
        return False
    else:
        return True

def check_url(url):
    log.debug("[%s] Checking URL", url)
    if "https" in url:
        if not fetch_url(url):
            print("Issue with URL: {}".format(url))
    elif "http" in url and "https" not in url:
        log.debug("[%s] URL uses HTTP and not HTTPS, checking if HTTPS works...", url)
        new_url = url.replace("http://", "https://")
        if fetch_url(new_url):
            log.error("[%s] Insecure URL found - use %s instead", url, new_url)
            print("Insecure URL {} detected!".format(url))
            print("\tUse {} instead".format(new_url))
        else:
            log.debug("[%s] HTTPS does not work, reverting to HTTP", url)
            if not fetch_url(url):
                print("Issue with URL: {}".format(url))

def main():
    arg_parse = create_argparse()
    parsed_args = arg_parse.parse_args(sys.argv[1:])
    markdown_filepath = parsed_args.markdownFile
    debug_mode = parsed_args.debug
    if debug_mode:
        log.setLevel(logging.DEBUG)
        log.debug("Debugging mode enabled!")
    if not os.path.exists(markdown_filepath):
        logstr = "Provided filepath does not exist! Please ensure the provided filepath is correct."
        log.error(logstr)
        print(logstr)
        sys.exit()
    log.info("Getting contents of Markdown file")
    with open(markdown_filepath) as mdfile:
        md_contents = mdfile.read()
    link_re = re.compile(r"\((.*?)\)")
    url_list = []
    log.info("Scanning file for URLs...")
    for line in md_contents.splitlines():
        log.debug("File line: %s", line)
        res = re.search(link_re, line)
        if res:
            url = res.group(1)
            log.debug("Found potential match...")
            if "http" in url:
                url_list.append(url)
                log.debug("Added URL %s to the list! List is now %s long", url, len(url_list))
    log.info("Found %s URLs, checking each one now...", len(url_list))
    thr_list = []
    for url in url_list:
        log.debug("Starting thread for %s", url)
        thr = Thread(target=check_url, args=(url,))
        thr_list.append(thr)
        thr.start()
    for thr in thr_list:
        thr.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
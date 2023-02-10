import re
from urllib.parse import urlparse


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return list()


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        # check if url has correct format
        if invalid_url_format(parsed):
            return False

        # check for invalid extensions
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|img|mpg|war|apk|ppsx|txt|DS_Store|db|odc|Z"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


def invalid_url_format(parsed):
    hostname = parsed.hostname
    query = parsed.query

    # check if url has a domain
    if hostname == None:
        return True

    # check if url has valid scheme
    if parsed.scheme not in set(["http", "https"]):
        return True

    # check if url has a valid domain
    domains = [".ics.uci.edu", ".cs.uci.edu",
               ".informatics.uci.edu", ".stat.uci.edu"]
    valid_domain = any([d in hostname for d in domains])
    if not valid_domain:
        return True

    # check if url has repeated words (e.g., www.example.com/aaa/bbb/aaa/index.html)
    paths = parsed.path.split("/")
    store = set()
    for p in paths:
        if p != "" and p in store:
            return True
        store.add(p)

    # check for invalid queries
    queries = query.split("&")
    invalid_params = ["action=download", "action=login", "action=edit"]
    invalid_query = any([p in queries for p in invalid_params])
    if invalid_query:
        return True

    return False

def info_value(soup):
    # first condition: large files
    # Check if the text in the page is more 10k words
        length = len(soup.text)
        if length > 10000:
            return False
    
    # second condition: images
    # Check if the number of images is less than 2
        images = soup.find_all('img')
        if len(images) < 2:
            return False
      
    # third condition: headers
    # Check the number of headings - more headings = valuable
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(headings) < 2:
            return False

        return True


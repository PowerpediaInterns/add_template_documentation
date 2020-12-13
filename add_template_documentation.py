import pywikibot
import requests
import urllib3

# Template to append to pages
TEMPLATE = "<noinclude>\n\n{{documentation}}\n</noinclude>"
# The namespace to retrieve pages from
# https://www.mediawiki.org/wiki/Manual:Namespace#Built-in_namespaces to see available namespaces
NAMESPACE = 10
# Number of pages to extract at a time; used in get_pages_json() in params for "aplimit"
PAGES_LIMIT = 3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_api_url() -> str:
	"""
	Retrieves the API URL of the wiki

	:return: String of the path to the API URL of the wiki
	"""

	site = pywikibot.Site()
	url = site.protocol() + "://" + site.hostname() + site.apipath()
	return url


def get_params(continue_from="") -> {}:
	"""
	Gets the parameters dictionary to make the GET request to the wiki

	:param continue_from: String of page title to continue from; defaults to beginning of wiki
	:return: a dictionary of the parameters
	"""

	return {
		"action": "query",
		"format": "json",
		"list": "allpages",
		"apcontinue": continue_from,
		"apnamespace": NAMESPACE,
		"aplimit": PAGES_LIMIT
	}


def has_template(page_title):
	"""
	Checks if the parameter page has TEMPLATE

	:param page_title: title of the page to be scanned
	:return: True if the page has TEMPLATE; False if otherwise
	"""

	site = pywikibot.Site()
	page = pywikibot.Page(site, page_title)
	page_text = page.text
	pass


def get_pages_to_modify(url) -> []:
	"""
	Retrieves a Page Generator with all old pages to be tagged

	:param url: String of the path to the API URL of the wiki
	:return: returns a list of page title
	"""

	# Retrieving the JSON and extracting page titles
	session = requests.Session()
	request = session.get(url=url, params=get_params(), verify=False)
	pages_json = request.json()
	pages = pages_json["query"]["allpages"]
	print("Pages to be scanned:", pages)

	pages_to_modify = []

	# Checks the pages for the template
	for page in pages:
		curr_title = page["title"]
		if not(has_template(curr_title)):
			pages_to_modify.append(curr_title)

	if "continue" in pages_json:
		continue_from = pages_json["continue"]["apcontinue"]
		print("Continuing from:", continue_from)
	else:
		continue_from = ""

	# Continue iterating through wiki
	while continue_from:
		# Retrieving the JSON and extracting page titles
		request = session.get(url=url, params=get_params(continue_from), verify=False)
		pages_json = request.json()
		pages = pages_json["query"]["allpages"]
		print("Pages to be scanned:", pages)

		# Checks the pages for the template
		for page in pages:
			curr_title = page["title"]
			if not(has_template(curr_title)):
				pages_to_modify.append(curr_title)

		# Extracting title to continue iterating from
		if "continue" in pages_json:
			continue_from = pages_json["continue"]["apcontinue"]
			print("Continuing from:", continue_from)
		else:
			continue_from = ""

	return pages_to_modify


def add_template(pages) -> None:
	"""
	Adds the instance variable TEMPLATE to the parameter pages

	:param pages: pages to be modified; consists of titles
	:return: None
	"""

	site = pywikibot.Site()
	for title in pages:
		page = pywikibot.Page(site, title)
		page_text = page.text

		if page_text.find(TEMPLATE) == -1:
			print("'%s' not in '%s'... Adding" % (TEMPLATE, page))
			page_text = u''.join((page_text, TEMPLATE))
			page.text = page_text
			page.save(u"Tagged with: " + TEMPLATE, botflag=True)
		else:
			print("'%s' already in '%s'... Skipping." % (TEMPLATE, page))


def main() -> None:
	"""
	Driver. Retrieves all the pages that need to be tagged then tags them.
	"""

	url = get_api_url()
	print(url)

	pages_to_modify = get_pages_to_modify(url)
	add_template(pages_to_modify)

	print("No pages left to be tagged")


if __name__ == '__main__':
	main()

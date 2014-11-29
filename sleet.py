#------------------------------------------------------------------------------
#	Author: Frank Carotenuto			Date: 11/27/2014
#
#	Description: Constructs a list of all Known pharmaceutical drugs
#------------------------------------------------------------------------------
import urllib, sys, re, threading  
from Queue import Queue

#------------------------------------------------------------------------------
#	Retrives all pharmaceutical drugs on page and appends them to parent_list
#------------------------------------------------------------------------------
def get_drugs(uri):
	global parent_list
	URL = "http://en.wikipedia.org" + uri.replace('\"', '').strip()
	regex = '\">.*?</a></b>'
	child_list = findall_on_page(regex, URL)
	parent_list += child_list

#------------------------------------------------------------------------------
#	Constructs a list of all with lists of pharmaceutical drugs
#------------------------------------------------------------------------------
def get_wiki_pages():
	URL = "http://en.wikipedia.org/wiki/List_of_drugs"
	regex = '/wiki/List_of_drugs:_...'
	URI_list = findall_on_page(regex, URL)

	X = set()
	for URI in URI_list:
		URL = "http://en.wikipedia.org" + URI.replace('\"', '').strip()
		regex, split_by, index = '/wiki/List_of_drugs:_.*?"', '</p>', 4
		URL_list = findall_on_page(regex, URL, split_by, index)

		X = set(URL_list).difference(set(URI_list)).union(X)

	return X

#------------------------------------------------------------------------------
#	Finds all regular expression matches on a given page. Option to split
#	the page and find all matches at given index.
#------------------------------------------------------------------------------
def findall_on_page(Rx, URL, split_by = '', index = -1):     
	sock = urllib.urlopen(URL)

	if split_by is '':
		htmlSource = sock.read()
	else:
		htmlSource = sock.read().split(split_by)[index]

	re_list = re.findall(Rx, htmlSource)
	sock.close()

	return re_list


#------------------------------------------------------------------------------
#	Runs each thread in an infinite loop until Queue q is empty. 
#------------------------------------------------------------------------------
def do_work():
	global q
	while True:
		uri = q.get()
		get_drugs(uri)
		q.task_done()

#------------------------------------------------------------------------------
# 	Creates given number of threads, having them retrieve data from 
#	pool of URLs
#------------------------------------------------------------------------------
if __name__ == "__main__":
	parent_list = []
	q = Queue()

	for x in range(int(sys.argv[1])):
		t = threading.Thread(target=do_work)
		t.daemon = True
		t.start()

	for URI in list(get_wiki_pages()):
		q.put(URI)

	q.join()

	text_file = open("Output.txt", "w")
	for Rx_drug in list(set(parent_list)):
		text_file.write(Rx_drug[2:-8] + "\n")

	text_file.close()
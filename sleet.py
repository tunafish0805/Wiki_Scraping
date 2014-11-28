#------------------------------------------------------------------------------
#	Author: Frank Carotenuto				Date: 11/27/2014
#
#	Description: Creates a list of Known pharmaceutical drugs
#------------------------------------------------------------------------------
import urllib, re, threading  
from Queue import Queue

#------------------------------------------------------------------------------
#
#
#
#------------------------------------------------------------------------------
def get_drugs(uri):
	global F
	temp = "http://en.wikipedia.org" + uri.replace('\"', '').strip()
	sock3 = urllib.urlopen(temp)
	htmlSource2 = sock3.read()
	Q = re.findall(r'\">.*?</a></b>', htmlSource2)
	F = set(Q).union(F)
	sock3.close()

#------------------------------------------------------------------------------
#
#
#
#------------------------------------------------------------------------------
def get_uris():
	sock = urllib.urlopen("http://en.wikipedia.org/wiki/List_of_drugs")
	htmlSource = sock.read()
	L = re.findall(r'/wiki/List_of_drugs:_...', htmlSource)
	sock.close()

	N = set()
	for x in range(len(L)):
		temp = "http://en.wikipedia.org" + L[x].replace('\"', '').strip()
		sock2 = urllib.urlopen(temp)
		htmlSource2 = sock2.read().split("</p>")
		M = re.findall(r'/wiki/List_of_drugs:_.*?"', htmlSource2[4])
		sock2.close()
		N = set(M).difference(set(L)).union(N)

	return N

#------------------------------------------------------------------------------
#
#
#
#------------------------------------------------------------------------------
def do_work():
	global q
	while True:
		uri = q.get()
		get_drugs(uri)
		q.task_done()


F = set()
q = Queue()

for subsite in list(get_uris()):
	q.put(subsite)

for x in range(15):
	t = threading.Thread(target=do_work)
	t.daemon = True
	t.start()

q.join()

W = list(F)
text_file = open("Output.txt", "w")
for j in range(0, len(W)):
	text_file.write(W[j].replace('</a></b>', '').replace('">', '') + "\n")

text_file.close()
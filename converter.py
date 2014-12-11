from patents import *
# -*- coding: utf-8 -*-#

for doc in documents:
    output = open("GROUP_3_{0}.html".format(doc),"w")
    html = "<!DOCTYPE html> \n<html>\n<head>\n<title>{0}</title>\n</head>\n\n<h1>{0}</h1>\n<body>\n<p>\n<em>{1}</em>\n<p>\n</body> \n\n</html>".format(doc,documents[doc])
    output.write(html) 
    

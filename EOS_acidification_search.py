import webbrowser
import pdfx

file = 'database_files/Advanced_Search.pdf'
pdf = pdfx.PDFx(file)
refs_dict = pdf.get_references_as_dict()

vncdr_list = []

for k in refs_dict['url']:
    if "ViewNewCompleteDisplayRecord" in k:
        vncdr_list.append(k)

bib_codes = [i.replace('javascript:ViewNewCompleteDisplayRecord','') for i in vncdr_list]

for i in range(0, len(bib_codes)):
    item = bib_codes[i]
    length = len(item)
    bib_codes[i] = str(item[2:length-3])

#print(bib_codes)

bib_codes_test = [bib_codes[i] for i in range(0,4)]

webbrowser.open("http://eos.ucs.uri.edu/EOSWebOPAC/OPAC/Search/AdvancedSearch.aspx")
acidif_search = input("Click Ocean Acidification filter. ENTER when done.")
print("Select first result.")
task_code = input("Task Code: ")
current_link_code = input("Current Link Code: ")

base_url = "http://eos.ucs.uri.edu/EOSWebOPAC/OPAC/Details/Record.aspx?IndexCode=-1&TaskCode=" + task_code + "&HitCount=247&CollectionCode=2&SortDirection=Descending&CurrentPage=1&CurrentLinkCode=" + current_link_code + "&SelectionType=0&SearchType=2&BibCode="

webbrowser.open_new(base_url + bib_codes[0])
import re
import sys
import time
import os

END_OF_TEI_HEADER = "</teiHeader>"
PERSON_TAG = "persName"
REGEX_BEFORE = re.compile("[a-zA-Z\-]", re.UNICODE)
REGEX_AFTER = re.compile("[a-zA-Z\-]", re.UNICODE)

# Add a word here if you want rabourdin to check it with and without a capital letter!
# NOTE: ALWAYS add words in lowercase in this list! :]
CASE_INSENSIVE_WORDS = ["monsieur", "madame", "mademoiselle"]

class Person:
	def __init__(self, id, lead, aliases):
		self.id = id
		self.lead = lead
		self.aliases = aliases
		
class PersonAlias:
	def __init__(self, name, person, type):
		self.id = id
		self.name = name
		self.person = person
		self.type = type
		self.has_matched = False

PEOPLE_LIST = []
REFERENCE_LIST = []

def find_all_from(a_str, sub, from_pos):
    start = from_pos
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

# I'm so sorry
def in_persname_tag(xml, match):
	prev_close = xml.rfind("</"+PERSON_TAG, 0, match)
	prev_open = xml.rfind("<"+PERSON_TAG, 0, match)
	
	if prev_open == -1:
		return False
	if prev_close == -1:
		return True
	return prev_close < prev_open

# Everytime we find a person in the text, we call this function
def process_match(xml, person, name, match, type):
	# Look for a <persName> before the match
	before_tag_lenght = len(PERSON_TAG)
	if in_persname_tag(xml, match):
		#print("Skipping %s, already in a persname tag!" % name)
		return xml, match+len(name), False
		
	# If the character before/after is a letter, we're cutting in the middle of a word! Skip this.
	if REGEX_BEFORE.match(xml[match-1]):
		#print("Skipping %s, bad character before" % name)
		return xml, match+len(name), False
	if REGEX_AFTER.match(xml[match+len(name)]):
		#print("Skipping %s, bad character after" % name)
		return xml, match+len(name), False
	
	# Modify the XML: Add a persName tag before and after the match
	before = '<'+PERSON_TAG+' ref="'+str(person.id)+type+'">'
	after =  "</"+PERSON_TAG+">"
	xml = xml[:match] + before + name + after + xml[match+len(name):]
	
	#print("Found new match for %s at %s" % (name, match))
	return xml, match+len(before)+len(name), True

# Parse a single txt database file (_P or _R) and return a list of people/references
def parse_txt_database_file(file):
	people_data = file.read()
	everybody_list = []
	
	# Split the raw data into an array of people
	people_array = people_data.split("\n\n")
	for people in people_array:
		# Each person may have multiple lines in the file
		# One lead, plus several aliases
		lines = people.split("\n")
		# The first line (the lead) is split by ">" characters
		identity = lines[0].split(">")
		id = identity[0]
		lead = identity[1]
		aliases = []
		for line in lines[1:]:
			if len(line) >= 1 and line[0] == '@':
				continue
			aliases.append(line)
		
		everybody_list.append(Person(id, lead, aliases))	
	return everybody_list

if len(sys.argv) != 2:
	print("Please drag and drop the XML file you want to process onto the .py file!")
	sys.stdout.flush()
	time.sleep(5)
	sys.exit(1)

SOURCE_XML = sys.argv[1]
SOURCE_PEOPLE = os.path.splitext(os.path.basename(SOURCE_XML))[0]+'_P.txt'
SOURCE_REFERENCES = os.path.splitext(os.path.basename(SOURCE_XML))[0]+'_R.txt'
	
print(SOURCE_PEOPLE)
	
# Open the people file and read contents
with open(SOURCE_PEOPLE) as people_file:
	PEOPLE_LIST = parse_txt_database_file(people_file)

# Open the reference file and read contents
with open(SOURCE_REFERENCES) as reference_file:
	REFERENCE_LIST = parse_txt_database_file(reference_file)
	
# Open the XML and add persName tags
with open(SOURCE_XML, "r+") as xml_file:
	xml = xml_file.read()
	
	# Skip the TEI header, because we don't want to add tags in there!
	start = xml.find(END_OF_TEI_HEADER)
	
	all_names_list = []
	
	for person in PEOPLE_LIST:
		all_names_list.append(PersonAlias(person.lead, person, 'P'))
		for alias in person.aliases:
			if alias.isspace():
				print("WARNING: There are some spaces under %s, instead of an empty line!" % person.lead)
			all_names_list.append(PersonAlias(alias, person, 'P'))

	for person in REFERENCE_LIST:
		all_names_list.append(PersonAlias(person.lead, person, 'R'))
		for alias in person.aliases:
			if alias.isspace():
				print("WARNING: There are some spaces under %s, instead of an empty line!" % person.lead)
			all_names_list.append(PersonAlias(alias, person, 'R'))
			
	all_names_list.sort(key=lambda item: len(item.name), reverse=True)
	for alias in all_names_list:
		pos = start
		name = alias.name
		if len(name) == 0:
			print("WARNING: There's an empty line under %s's aliases!" % person.lead)
			continue
		while True:		
			pos = xml.find(name, pos)
			if pos == -1: break
			xml, pos, ok = process_match(xml, alias.person, name, pos, alias.type)
			if ok:
				alias.has_matched = True
		if name.split(" ")[0].lower() in CASE_INSENSIVE_WORDS:
			altname = (name[0].upper() + name[1:]) if name[0] == name[0].lower() else (name[0].lower() + name[1:])
			pos = start
			while True:		
				pos = xml.find(altname, pos)
				if pos == -1: break
				xml, pos, ok = process_match(xml, alias.person, altname, pos, alias.type)
				if ok:
					alias.has_matched = True
		
		if alias.has_matched == False:
			print('"%s" was not found!' % alias.name)
	
	xml_file.truncate(0)
	xml_file.seek(0)
	xml_file.write(xml)

 

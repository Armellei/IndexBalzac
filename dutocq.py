import glob
import os

SOURCE_INDEX = "index-template.html"
DEST_INDEX = "index.html"
TEMPLATE_MARKER = "###TEMPLATE###"

def getGenderString(person):
	s = person.gender

	if s == 0:
		return 'Ensemble de personnes ou genre inconnu'
	elif s == 1:
		return 'Personnage masculin'
	elif s == 2:
		return 'Personnage féminin'
	elif s == 3:
		return 'Famille ou maison'
	elif s == 4:
		return 'Animal'
	else:
		raise Exception("Fix the gender field! %s is not a valid gender for %s" % (s, person.lead))

def parseRelation(relations, line):
	colon = line.find(':')
	relname = line[1:colon]
	args = [arg.strip() for arg in line[colon+1:].split(',')]
	relations[relname] = args 
	return relations

class Person:
	def __init__(self, id, lead, first_letter, occupation, city, gender, relations, aliases, type, sourcefile):
		self.id = id
		self.lead = lead
		self.first_letter = first_letter
		self.aliases = aliases
		self.occupation = occupation
		self.city = city
		self.gender = gender
		self.relations = relations
		self.type = type
		self.sourcefiles = [sourcefile]
		
people_list = []
people_map = {}

# Parse a single txt database file (_P or _R) and return a list of people/references
def parse_txt_database_file(file, filename, type):
	people_data = file.read().decode('utf-8').replace('\r\n', '\n')
	
	list = []
	# Split the raw data into an array of people
	people_array = people_data.split("\n\n")
	for people in people_array:
		# Each person may have multiple lines in the file
		# One lead, plus several aliases
		lines = people.split("\n")
		# The first line (the lead) is split by ">" characters
		identity = lines[0].split(">")
		try:
			if len(identity) > 6:
				print("There are more than 5 '>' for %s" % identity[1])
				input("")
			id = int(identity[0])
			lead = identity[1]
			occupation = identity[2]
			city = identity[3]
			gender = int(identity[4]) if len(identity[4]) > 0 else 0
			first_letter = identity[5]
			aliases = []
			relations = {}
			for line in lines[1:]:
				if len(line) >= 1 and line[0] == '@':
					relations = parseRelation(relations, line)
					continue
				aliases.append(line)
			
			list.append(Person(id, lead, first_letter, occupation, city, gender, relations, aliases, type, filename))
		except Exception as e:
			print('Error in the character file! Possibly a missing ">" or extra blank line for this character, or a reversal between a place and a number (0/1/2/3/4): \n%s' % people)
			input("")
	return list
	

# Open the people file and read contents
for people_path in glob.glob("*_P.txt"):
	print("Opening people file "+people_path)
	filename = os.path.splitext(people_path)[0]
	with open(people_path, 'rb') as file:
		people_list += parse_txt_database_file(file, filename, 'P')

# Open the people file and read contents
for people_path in glob.glob("*_R.txt"):
	print("Opening reference file "+people_path)
	filename = os.path.splitext(people_path)[0]
	with open(people_path, 'rb') as file:
		people_list += parse_txt_database_file(file, filename, 'R')

# Merge people list (and find dupes)
hasError = False
people_list_with_dupes = people_list
for people in people_list_with_dupes:
	typeid = str(people.id)+people.type
	if not typeid in people_map:
		people_map[typeid] = people
		continue
	ours = people
	theirs = people_map[typeid]
	
	# Find mismatches
	try:
		if ours.lead != theirs.lead and not (ours.lead in theirs.aliases and theirs.lead in ours.aliases):
			raise Exception("Names don't match for character %s (%s and %s)" % (ours.id, ours.lead, theirs.lead))
		if ours.first_letter != theirs.first_letter:
			raise Exception("First letters don't match for character %s %s" % (ours.id, ours.lead))
		if ours.occupation != theirs.occupation:
			raise Exception("Occupation don't match for character %s %s" % (ours.id, ours.lead))
		if ours.gender != theirs.gender:
			raise Exception("Gender don't match for character %s %s" % (ours.id, ours.lead))
		if ours.city != theirs.city:
			raise Exception("Cities don't match for character %s %s" % (ours.id, ours.lead))
	except Exception as e:
		hasError = True
		print(e)
		continue
	
	# Merge the two characters (they have the same ID, but appear in a different book)
	for alias in ours.aliases:
		if not alias in theirs.aliases:
			theirs.aliases.append(alias)
	for rel in ours.relations:
		if not rel in theirs.relations:
			theirs.relations[rel] = ours.relations[rel]
		else:
			for arg in rel:
				if not arg in theirs.relations[rel]:
					theirs.relations[rel].append(arg)
	theirs.sourcefiles += ours.sourcefiles
					
people_list = []
for id in people_map:
	people_list.append(people_map[id])
				
if hasError:
	input("Press enter to quit...")

# Open the index page and add each character
src=""
with open(SOURCE_INDEX, 'rb') as index_file:
	src = index_file.read().decode('utf-8')

with open(DEST_INDEX, "wb+") as index_file:
	contents = src
	pos = contents.find(TEMPLATE_MARKER)
	contents = contents.replace(TEMPLATE_MARKER, '')
	before = contents[:pos]
	after = contents[pos:]
	
	index_menu = "<p id='index-menu'>"
	mid = ""
	last_letter = ''
	for person in sorted(people_list, key=lambda p: p.first_letter):
		if last_letter != person.first_letter:
			mid += "</ul><h1 id='index-entry-"+person.first_letter+"' class='index-entry'>"+person.first_letter+"</h1><ul>"
			index_menu += '<a href="#index-entry-'+person.first_letter+'">'+person.first_letter+"</a> "
			last_letter = person.first_letter
	
		mid += "<li id='person-"+str(person.id)+"' class='person'><span class='lead'>"+person.lead+'</span>'
		# Class details contains all the details about a character (aliases, occupation, city, gender, ...)
		mid += "<div class='details'>"
		
		# Add aliases
		if len(person.aliases) != 0:
			mid += "<ul class='aliases'>"
			for alias in person.aliases:
				mid += "<li>"+alias+"</li>"
			mid += "</ul>"
		
		# Occupation
		if len(person.occupation) != 0:
			mid += "<p class='occupation'>"+person.occupation+"</p>"
		
		# City
		if len(person.city) != 0:
			mid += "<p class='city'>"+person.city+"</p>"
		
		# Gender
		if person.gender != 0:
			mid += "<p class='gender'>"+getGenderString(person)+"</p>"
		
		### DEBUG: Show relations
		if len(person.relations) != 0:
			mid += "<p class='relations'>Relations: </p>"				
		for rel in person.relations:
			mid += "<ul class='relation'>"+rel+":"
			for target in person.relations[rel]:
				mid += "<li><a href='#person-"+str(target)+"'>"+str(target)+"</a></li>"
			mid += "</ul>"
		
		# DEBUG: Show the source files
		mid += "<p class='sourcefile'>"+", ".join(person.sourcefiles)+"</p>"
		
		
		# DEBUG: Show the ID (in case there are duplicates)
		mid += "<p class='id'>"+str(person.id)+"</p>"
		
		mid += "</div>"
		mid +="</li>"
	
	index_menu += "</p>"
	contents = before+index_menu+mid+after
	index_file.write(contents.encode('utf-8'))

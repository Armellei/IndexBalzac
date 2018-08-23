# IndexBalzac

IndexBalzac allows you to semi-automatically index every single character's name found in Balzac's books. You'll find five programs helping you to do the work, and html/css illustrated index, some engravings from 1842-46 and 1874 and a report helping you understand it all.
The indexing process uses Python and Awk, and you can start working with the help of 5 scripts easy to manipulate after you've installed both languages, even though you don't understand anything about coding : read the report, install the files and start indexing!

### Indexing process :
Manually create your databases in txt > Use **Dutocq** to tag the XML-TEI file > Use **Colleville** to highlight your work in the HTML preview of the book and make adjustments in the databases if needed > Use **Rabourdin** to generate the index in HTML > Use **Bixiou** to sort the names properly > Once you're done with all these debugging steps, use **txt2json** to export the txt databases into JSON files. > Congrats, you're done!

### This repo contains :

'Database' contains txt files for each book to be converted into pretty json files.

'Draft HTML index' contains all you need to create your own index. Good luck.

'Hdef Gallica' contains the engravings (standardized size 1350x2000 px)

'Hdef Icons' contains circle icons (standardized size 400x400 px)

'Indexing scripts' contains awk & python scripts :

- **rabourdin.py** adds <persName> tags to any XML-TEI file from the txt databases
- **dutocq.py** instantly generates an index in HTML and debugs the txt databases
- **colleville.py** will highlight the HTML files directly from the P & R txt databases to let us check whether we forgot any names, or not
- **bixiou.py** is great at sorting all those indexed names in alphabetical order, previously pasted in a 'tri.txt' file
- **txt2json.awk** transforms txt databases into proper JSON files for web integration
  
 'Heraldry' contains the coats-of-arms (svg, jpeg icons & jpeg hdef files)

'Identification' reports the names of the engravers and/or draughtsman for each illustration, if known

'Img links from Gallica' contains the links from Gallica to download the images again/identify the artists, if needed

'Typefaces/ttf' contains the typefaces used to generate the index in its HTML draft version.

The reports are here to help you understand it all.

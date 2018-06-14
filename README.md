# IndexBalzac

*Process :*
Manually create your databases in txt > Use Dutocq to tag the XML-TEI file > Use Colleville to highlight your work and make adjustments in the databases if needed > Use Rabourdin to generate the index in HTML > Use Bixiou to sort the names properly > Once you're done with debugging, use txt2json to export the txt databases into JSON files. > Congrats, you're done!

_This repo contains :_

'Database' contains txt files for each book to be converted into pretty json files.

'Hdef Gallica' contains the engravings (standardized size 1350x2000 px)

'Hdef Icons' contains circle icons (standardized size 400x400 px)

'Indexing scripts' contains awk & python scripts :

- *rabourdin.py* adds <persName> tags to any XML-TEI file from the txt databases
- *dutocq.py* instantly generates an index in html and debugs the txt databases
- *colleville.py* is will highlight the HTML files directly from the P & R txt databases to let us check whether we forgot any names, or not
- _bixiou.py_ is great at sorting all those names in alphabetical order, previously pasted in a 'tri.txt' file
- _txt2json.awk_ transforms txt databases into proper json files for web integration
  
 'Heraldry' contains the coats-of-arms (svg, jpeg icons & jpeg hdef files)

'Identification' reports the names of the engravers and/or draughtsman for each illustration, if known

'Img links from Gallica' contains the links from Gallica to download the images again/identify the artists, if needed

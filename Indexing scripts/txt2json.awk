BEGIN {
	#thank you windows
    RS="\r\n\r\n"
    FS="\r\n"
}

{
	# Finish end of last record
	if (NR != 1)
        print "},"
	
	split($1, a, ">")	
	
	print "{"
	
	#arguments 3 and 4 might be null, if they are, its taken into account
    print "  \"id\": " a[1] ","
	print "  \"lead\": \"" a[2] "\","
	if (a[3] == "")
		print "  \"role\": null,"
	else
		print "  \"role\": \""  a[3] "\","
	if (a[4] == "")
		print "  \"location\": null,"
	else
		print "  \"location\": \"" a[4] "\","
    print "  \"type\": " a[5] ","
	print "  \"indexation\": \"" a[6] "\","
	
	print "  \"aliases\": ["
	
	# Goes over each line, and prints the variable if there are aliases (any lines but $1 without @)
	for (moreinfo=2; moreinfo<=NF; moreinfo++) {
		if ($moreinfo ~ /^[^@]/) {
			print "    \"" $moreinfo "\","
		}
    }

	#writes relations only if there are any (any lines but $1 with @)
	print "  ],"
	print "  \"relations\": ["
	
	for (moreinfo=2; moreinfo<=NF; moreinfo++) {
		if ($moreinfo ~ /^[@]/) {
			split($moreinfo, b, ":")	
			print "    \"" b[1] "\": \"" b[2] "\","
		}
    }
	
	print "  ]"
}
	
#No comma for the very last group
END {
    print "}"
}

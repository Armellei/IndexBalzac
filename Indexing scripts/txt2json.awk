BEGIN {
    RS="\r\n\r\n"
    FS="\r\n"
}

{
    # Finish end of last record
    if (NR != 1)
        print "},"

    nargs = split($1, args, ">")

    for (i=1; i<=nargs; i++)
        if (args[i] == "")
            args[i] = "null"
        else if (i != 1 && i != 5)
            args[i] = "\"" args[i] "\""

    print "{"
    print "  \"id\": " args[1] ","
    print "  \"lead\": " args[2] ","
    print "  \"role\": " args[3] ","
    print "  \"location\": " args[4] ","
    print "  \"type\": " args[5] ","
    print "  \"gender\": " args[6] ","
    print "  \"aliases\": ["

    # The last record has a stray newline due to being the end of file, skip it
    if ($NF == "")
        NF = NF-1

    for (i=2; i<=NF; i++) {
        if (i != NF)
            print "    \"" $i "\","
        else
            print "    \"" $i "\""
    }

    print "  ]"
}

END {
    print "}"
}

#!/bin/env bash

# 1. Shape xml files into valid xml.
# 2. Process xml into csv.
# 3. Commit to Solr.

process_data() {

    DATA=data/split_xml*

    for dat in $DATA
    do
   
    echo "Processing $dat"
    python parse_stackexchange.py $dat

    done
}

commit_data() {

    CSV=data/*.csv

    for csv in $CSV
    do
    # Commit each csv file to Solr.
    
    echo "Committing $csv to Solr"
    curl http://localhost:8983/solr/update/csv?commit=true -F stream.file=`pwd`/$csv -F f.t_r_attributes.split=true

    done
}

delete_data() {

    echo "Deleting all data from Solr."
    curl http://localhost:8983/solr/update?commit=true --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'
}

# If the file has not already been split, split it.
if [ ! -e ./data/split ]
then
    rm ./data/split_xml* # Remove any data if it exists.
    echo "Splitting file into 10,000 line chunks."
    split ./data/posts.xml -l 10000 "data/split_xml"
    # Poor man's flag
    touch ./data/split

    DATA=./data/split_xml*

    for dat in $DATA
    do
     # All files will be missing the xml header, as well as an opening
    # and closing <post> tag.
    # Well, all except for the first and last files, so the workaround
    # to this is to simply remove these from the master, and process
    # all files alike.
    echo "Writing valid xml for $dat"
    echo "<?xml version=\"1.0\" encoding=\"utf-8\"?><posts>" | cat > $dat
    cat /tmp/$dat >> $dat
    echo "</posts>" | cat >> $dat
    done

fi

process_data;
commit_data;

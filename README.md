Stack Overflow Search
================================


To start Solr:

`$ cd solr_example_dir`
`$ java -jar -Dsolr.solr.home=<full_path_to_this_dir>/solr_home start.jar`


To index documents:

`$ python parse_stackexchange.py "/path/to/posts.xml"` 

`$ curl http://localhost:8983/solr/update/csv?commit=true \
    -F stream.file=/path/to.csv -F f.t_r_attributes.split=true`

Configuration details in `solr/collection1/conf/schema.xml.`

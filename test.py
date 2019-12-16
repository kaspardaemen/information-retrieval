import sys
sys.path.append("/home/kaspar/Github/nordlys/nordlys/")

import core.retrieval
from nordlys.el import el 
dir(core.retrieval)
es=Elasticsearch([{'host':'localhost','port':9200}])

retrieval.retrieval()
res=es.get(index='dbpedia_2015_10',doc_type='doc',id='<dbpedia:2007–08_FA_Trophy>' )

res= es.search(index='dbpedia_2015_10',body={'query':{}})
print (res['hits']['hits'])

es.doc_length(index='dbpedia_2015_10')

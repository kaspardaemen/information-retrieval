from elasticsearch import Elasticsearch

import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

from nordlys.logic.entity.entity import Entity
from nordlys.core.eval.eval import Eval
from nordlys.core.eval.query_diff import QueryDiff
from nordlys.core.retrieval.retrieval import Retrieval
from nordlys.core.retrieval.elastic import Elastic

elastic = Elastic('dbpedia_2015_10')

elastic.num_docs()

elastic.search("paris", 'names' , num=100, start=0)

elastic.get_fields()


querydiff = QueryDiff(run1_file="/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/runs/bm25.run", run2_file="/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/runs/lm.run", qrels='/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/qrels-v2.txt', metric='map' )
querydiff.dump_differences('output' )

es=Elasticsearch([{'host':'localhost','port':9200}])

res=es.get(index='dbpedia_2015_10',doc_type='doc',id='<dbpedia:2007–08_FA_Trophy>' )

res= es.search(index='dbpedia_2015_10',body={'query':{}})
print (res['hits']['hits'])


config = {"index_name": "dbpedia_2015_10",
  "first_pass": {
    "1st_num_docs": 100
  },
  "model": "bm25",
  "num_docs": 100,
  "smoothing_method": "dirichlet",
  "smoothing_param": 2000,
  "fields": ["names", "categories", "attributes", "similar_entity_names", "related_entity_names"],
  "query_file": "/home/kaspar/Github/information-retrieval/queries_stopped.json",
  "output_file": "/home/kaspar/Github/information-retrieval/output.txt",
  "run_id": "bm25"
}
  
#RETRIEVAL:
retrieval = Retrieval(config)
res = retrieval.retrieve("Parijs", scorer=None)
retrieval.batch_retrieval()




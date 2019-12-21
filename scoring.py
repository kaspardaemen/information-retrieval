import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

from nordlys.core.retrieval.retrieval import Retrieval


config = {"index_name": "dbpedia_2015_10",
  "first_pass": {
    "1st_num_docs": 100
  },
  "model": "bm25",
  "num_docs": 100,
  "smoothing_method": "dirichlet",
  "smoothing_param": 2000,
  "fields": ["names", "categories", "attributes", "similar_entity_names", "related_entity_names"],
  "query_file": "/home/kaspar/Github/information-retrieval/expanded_queries/queries_expanded_longer3_90.json",
  "output_file": "/home/kaspar/Github/information-retrieval/outputs/output_expanded_longer3_90.txt",
  "run_id": "bm25"
}
  
retrieval = Retrieval(config)
retrieval.batch_retrieval()
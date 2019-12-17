from elasticsearch import Elasticsearch

import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

from nordlys.logic.entity.entity import Entity
from nordlys.core.eval.eval import Eval
from nordlys.core.eval.query_diff import QueryDiff
from nordlys.core.retrieval.retrieval import Retrieval
from nordlys.core.retrieval.elastic import Elastic
import pytrec_eval
import json
import pandas as pd
import os

#elastic = Elastic('dbpedia_2015_10')

#elastic.num_docs()

#elastic.search("paris", 'names' , num=100, start=0)

#elastic.get_fields()


#querydiff = QueryDiff(run1_file="/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/runs/bm25.run", run2_file="/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/runs/lm.run", qrels='/home/kaspar/Github/nordlys/data/dbpedia-entity-v2/qrels-v2.txt', metric='map' )
#querydiff.dump_differences('output' )

#es=Elasticsearch([{'host':'localhost','port':9200}])

#res=es.get(index='dbpedia_2015_10',doc_type='doc',id='<dbpedia:2007–08_FA_Trophy>' )

#res= es.search(index='dbpedia_2015_10',body={'query':{}})
#print (res['hits']['hits'])














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
  
def reformat_dict(d):
    result = {}
    for key in d.keys():
        values = {}
        for value  in d[key]:
            query_id = next(iter(value))
            score = int(value[next(iter(value))])
            values[query_id] = score
        result[key] = values
    return result
            
            
        



  
def make_qrel_dict(file_path):
    
    df = pd.read_csv(file_path, sep='\t')
    
    df.columns = ['query_id', 'query_number', 'document_id', 'judgement' ]
    d = {}
    for i in df['query_id'].unique():
        d[i] = [{df['document_id'][j]: df['judgement'][j]} for j in df[df['query_id']==i].index]
    
    
    return d

def make_run_dict(file_path):
    
    df = pd.read_csv(file_path, sep='\t')
    
    df.columns = ['query_id', 'query_number', 'document_id', 'nr', 'score', 'method' ]
    d = {}
    for i in df['query_id'].unique():
        d[i] = [{df['document_id'][j]: df['score'][j]} for j in df[df['query_id']==i].index]
    
    return d
  
retrieval = Retrieval(config)
retrieval.batch_retrieval()

qrel = {
    'q1': {
        'd1': 0,
        'd2': 1,
        'd3': 0,
    },
    'q2': {
        'd2': 1,
        'd3': 1,
    },
}

run = {
    'q1': {
        'd1': 1.0,
        'd2': 0.0,
        'd3': 1.5,
    },
    'q2': {
        'd1': 1.5,
        'd2': 0.2,
        'd3': 0.5,
    }
}

qrel_dict = make_qrel_dict('qrels-v2.txt')
run_dict = make_run_dict('output.txt')


#DIT RUNNEN
qrel_temp = reformat_dict(qrel_dict)
run_temp = reformat_dict(run_dict)



        


evaluator = pytrec_eval.RelevanceEvaluator(
    qrel_temp, {'map', 'ndcg'})

results = json.dumps(evaluator.evaluate(run_temp), indent=1)




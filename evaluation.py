import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

import pytrec_eval
import json
import pandas as pd


# FUNCTIONS:
  
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
    
    df = pd.read_csv(file_path, sep='\t', header=None)
    
    df.columns = ['query_id', 'query_number', 'document_id', 'judgement' ]
    d = {}
    for i in df['query_id'].unique():
        d[i] = [{df['document_id'][j]: df['judgement'][j]} for j in df[df['query_id']==i].index]
    
    
    return d

def make_run_dict(file_path):
    
    df = pd.read_csv(file_path, sep='\t',header=None)
    
    df.columns = ['query_id', 'query_number', 'document_id', 'nr', 'score', 'method' ]
    d = {}
    for i in df['query_id'].unique():
        d[i] = [{df['document_id'][j]: df['score'][j]} for j in df[df['query_id']==i].index]
    
    return d

#EVALUATION

qrel_dict = make_qrel_dict('qrels-v2.txt')
run_dict = make_run_dict('output.txt')
    
qrel_temp = reformat_dict(qrel_dict)
run_temp = reformat_dict(run_dict)
    
evaluator = pytrec_eval.RelevanceEvaluator(qrel_temp, {'map', 'ndcg'})
results = evaluator.evaluate(run_temp)

    
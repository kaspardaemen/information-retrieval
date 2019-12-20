import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

import pytrec_eval
import json
import pandas as pd
import numpy as np


# FUNCTIONS:
  
def reformat_dict(d, qrel):
    result = {}
    for key in d.keys():
        values = {}
        for value  in d[key]:
            query_id = next(iter(value))
            score = int(value[next(iter(value))]) if qrel else value[next(iter(value))]
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
read_qrels = make_qrel_dict('qrels-v2.txt')
read_run = make_run_dict('output.txt')
read_run_expanded = make_run_dict('output_expanded_80.txt')
    
qrel = reformat_dict(read_qrels, True)
run = reformat_dict(read_run, False)
run_80 = reformat_dict(read_run_expanded, False)
    
evaluator = pytrec_eval.RelevanceEvaluator(qrel, {'map', 'ndcg'})
results = evaluator.evaluate(run)
results_80 = evaluator.evaluate(run_80)

#with open('queries_expanded_80.json') as f:
#  test= json.load(f)


maps_results = []
maps_results_80 = []

ndcg_results = []
ndcg_results_80 = []
#COMPARE RESULTS
for key, value in results.items():
    maps_results.append(value['map'])
    ndcg_results.append(value['ndcg'])
for key, value in results_80.items():
    maps_results_80.append(value['map'])
    ndcg_results_80.append(value['ndcg'])
    
print('MAP average of results {}'.format(np.mean(maps_results)))
print('MAP average of results_80 {}'.format(np.mean(maps_results_80)))
print('gain average of results {}'.format(np.mean(ndcg_results)))
print('gain average of results_80 {}'.format(np.mean(ndcg_results_80)))

   
    






    
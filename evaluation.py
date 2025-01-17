import sys
sys.path.insert(0, "/home/kaspar/Github/nordlys")

import pytrec_eval
import pandas as pd
import numpy as np
import scipy.stats


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

def compare_results(result_dict, result1, result2, measure):
    if not (measure in ['map','ndcg']):
        print("invalid measure")
        return
    
    query_ids = [key for key in result_dict[result1].keys()]
    first_results = result_dict[result1]
    second_results = result_dict[result2]
    
    first_scores = [ first_results[query_id][measure] for query_id in query_ids]
    second_scores = [second_results[query_id][measure] for query_id in query_ids]
    
    print("-----------------------------------------------------------------------------------------")
    print("Comparison with !{}! as measure: {} VS {} ".format(measure, result1,result2))
    print("\nThe average score of {} is: {}".format(result1, np.mean(first_scores)))
    print("The average score of {} is: {}".format(result2, np.mean(second_scores)))
 
    ttest = scipy.stats.ttest_rel(first_scores, second_scores)
    print("\nT-test results: \nTwo-sided p-value: {} \nT-statistic: {}".format(ttest.pvalue, ttest.statistic))
    print("-----------------------------------------------------------------------------------------")

def get_all_means(result_dict, measure):
    query_ids = [key for key in result_dict[next(iter(result_dict))].keys()]
    means = {}
    for key in result_dict.keys():
        mean = np.mean([ result_dict[key][query_id][measure] for query_id in query_ids])
        means[key] = mean
    return means
    
    
    

#EVALUATION
    
#read the files
read_qrels = make_qrel_dict('qrels-v2.txt')
read_run = make_run_dict('outputs/output.txt')
read_run_80 = make_run_dict('outputs/output_expanded_80.txt')
read_run_90 = make_run_dict('outputs/output_expanded_90.txt')
read_run_long3_80 = make_run_dict('outputs/output_expanded_long3_80.txt') 
read_run_long3_90 = make_run_dict('outputs/output_expanded_longer3_90.txt')  
    
#reformat into the right input for pytrec_eval
qrel = reformat_dict(read_qrels, True)
run = reformat_dict(read_run, False)
run_80 = reformat_dict(read_run_80, False)
run_90 = reformat_dict(read_run_90, False)
run_long3_80 = reformat_dict(read_run_long3_80, False)
run_long3_90 = reformat_dict(read_run_long3_90, False) 

#evaluate results    
evaluator = pytrec_eval.RelevanceEvaluator(qrel, {'map', 'ndcg'})
results = evaluator.evaluate(run)
results_80 = evaluator.evaluate(run_80)
results_90 = evaluator.evaluate(run_90)
results_long3_80 = evaluator.evaluate(run_long3_80)
results_long3_90 = evaluator.evaluate(run_long3_90)


#COMPARISON
result_dict = {
        'results': results,
        'results_80': results_80,
        'results_90': results_90,
        'results_long3_80': results_long3_80,
         'results_long3_90': results_long3_90
        }

compare_results(result_dict, 'results', 'results_90', 'map')
compare_results(result_dict, 'results', 'results_90', 'ndcg')

ndcg_means = get_all_means(result_dict,'ndcg')
map_means = get_all_means(result_dict,'map')

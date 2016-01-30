import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
import json

#pretty print
def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)

#Function to map the values of a training dataset(name hard coded for now)
#to unique values in a dict as integers
def map_values(header):
	unique_values = list(enumerate(np.unique(train_df[header]))) #get unique values
	#print unique_values
	unique_dict = {value : i for i, value in unique_values}      #create dict for values
	#print json.dumps(unique_dict)
	#print unique_dict
	return unique_dict

#Function to unmap values
def un_map(header):
	unique_values = list(enumerate(np.unique(train_df[header]))) #get unique values
	unique_dict = {value : i for i, value in unique_values}      #create dict for values
	return unique_dict

#read from .txt file --> Dec20trainingset.csv, data.txt HARDCODED IN THIS SCRIPT RodoniTraningSet
train_df = pd.read_csv('Feb12014-Dec182015-training-cleansed.csv', header=0, low_memory = False)
#print train_df

#Print HEADERS #
#print list(train_df.columns.values)

#drop oppID and amounts
#train_df = train_df.drop(['OpportunityID','PushCounter','NextSteps','CompellingEvent','ACV','Employees','Amount','AnalyticsAmount','DatacomAmount','CustomAmount','SalesAmount','ServiceAmount']) #, axis=1)
dropcols = ['opportunityID','pushCounter','amount']
train_df = train_df.drop(dropcols, axis = 1)

#Get all of the header names in file
headers = list(train_df.columns.values)
unmap_df = pd.DataFrame()
dict_of_dicts = {}
#print type(dict_of_dicts)
for header in headers:
	unique_dict = map_values(header)
	rev_ref = dict((v,k) for k,v in unique_dict.iteritems())
	dict_of_dicts[header] = rev_ref

	#....code to save each dict...
	#train_df[header] = train_df[header].map(lambda x: unique_dict[x]).astype(int)
	#unmap_df[header] = train_df[header].map(lambda x: rev_ref[x])
	#in the map maybe we convert to <col_name>-int ??

#print the dataframe after to verify it scrambled
#pretty(dict_of_dicts,0)
print json.dumps(dict_of_dicts)

""" Writing my first randomforest code.
Author : AstroDave
Date : 23rd September 2012
Revised: 15 April 2014
please see packages.python.org/milk/randomforests.html for more

""" 
import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

##################################
# Get Data
# TO BE BUILT:
# 1: sysargv to read in the training file and the testing file
##################################

train_df = pd.read_csv('Feb12014-Dec182015-training-cleansed.csv', header=0) # encoding="utf-8-sig", Load the train file into a dataframe
test_df =  pd.read_csv('Dec14-Dec18-cleansed.csv', header=0) #test set Dec14-Dec18-cleansed
headers = list(train_df.columns.values)
print headers

##################################
#Determine which columns to encode from csv
##################################
drop_cols = []
for header in headers:
	if (train_df[header].dtype == np.int64 or train_df[header].dtype == np.float):
		print "DROP: ", header
		col_ind = train_df.columns.get_loc(header)
		drop_cols.append(header)
		#train_df = train_df.drop(train_df.columns[col_ind], axis=1, inplace=True)
		#train_df.drop(header, axis=1)
	else:
		print "Don't Drop: ", header
print drop_cols

##################################
# Call function to generate encode all columns by the int and float columns in 
# the list above: drop_cols
# We can use the anon_dataframe.py script to do this
# TO BE BUILT:
# 1: The anon_dataframe.py script has to be modified to save the model for future use
# 2: The script needs to be modified to check all values to be encoded, and if a new value
#    is present in the new prediction set then add this to the model
# 3: Modify interface of anon_dataframe.py to take in drop_cols list as an argument for --keep
#    while removing the inputs for input file and output file
##################################

# INSERT: code to pass drop_cols to anon_dataframe.py and return encoded dataframe for training
#train_df = anon_dataframe(drop_cols)

# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
#train_df = train_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 


# Collect the test data's opportunityIDs before dropping it
ids = test_df['opportunityID'].values
# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)

test_df = test_df.drop(['opportunityID'], axis=1) 

# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array

train_data = train_df.values
test_data = test_df.values

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,4] )

print 'Predicting...'
output = forest.predict(test_data).astype(int)


predictions_file = open("Sales_Predictions.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["opportunityID","Won"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'

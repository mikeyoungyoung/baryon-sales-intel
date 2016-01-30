import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import argparse,sys

#Run the script as python anon_dataframe.py test.csv --keep GUID_column_name --outfilename blah.csv
#By default it'll scramble anything that's not a float 
#(scikit-learn treats all non-floats as categoricals). 
#You can do "--keep GUID_column_name,some_other_column_name" if you want to keep more. 
#The mappings are stored within the module, so if you wanted to convert back 
#and forth you can call "mcle.inverse_transform(df)" from within the script to 
#go the other way. 

class MultiColumnLabelEncoder(LabelEncoder):
    """
    Wraps sklearn LabelEncoder functionality for use on multiple columns of a
    pandas dataframe.

    """
    def __init__(self, dframe, columns=None,keep=None):
        if not columns:
            columns = dframe.iloc[:, :].select_dtypes(include=['object']).columns
        if keep:
            for x in keep:
            	print "@@@@@ INDEX @@@@@@"
            	print type(x)
            	print "^^^^^^ TYPE COL ^^^^^^"
            	print columns
                columns = columns.drop(x) #This line is the original
                #columns = columns.drop(x, axis=1) #try adding index
                #columns = columns.remove(x)
        self.columns = columns
        self.fit(dframe)
        #pick the classes here to save them for future use

    def fit(self, dframe):
        """
        Fit label encoder to pandas columns.

        Access individual column classes via indexig `self.all_classes_`

        Access individual column encoders via indexing
        `self.all_encoders_`
        """
        # if columns are provided, iterate through and get `classes_`
        if self.columns is not None:
            # ndarray to hold LabelEncoder().classes_ for each
            # column; should match the shape of specified `columns`
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            self.all_encoders_ = np.ndarray(shape=self.columns.shape,
                                            dtype=object)
            for idx, column in enumerate(self.columns):
                # fit LabelEncoder to get `classes_` for the column
                le = LabelEncoder()
                le.fit(dframe.loc[:, column].values)
                # append the `classes_` to our ndarray container
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                # append this column's encoder
                self.all_encoders_[idx] = le
        else:
            # no columns specified; assume all are to be encoded
            self.columns = dframe.iloc[:, :].columns
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            for idx, column in enumerate(self.columns):
                le = LabelEncoder()
                le.fit(dframe.loc[:, column].values)
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
        return self

    def fit_transform(self, dframe):
        """
        Fit label encoder and return encoded labels.

        Access individual column classes via indexing
        `self.all_classes_`

        Access individual column encoders via indexing
        `self.all_encoders_`

        Access individual column encoded labels via indexing
        `self.all_labels_`
        """
        # if columns are provided, iterate through and get `classes_`
        if self.columns is not None:
            # ndarray to hold LabelEncoder().classes_ for each
            # column; should match the shape of specified `columns`
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            self.all_encoders_ = np.ndarray(shape=self.columns.shape,
                                            dtype=object)
            self.all_labels_ = np.ndarray(shape=self.columns.shape,
                                          dtype=object)
            for idx, column in enumerate(self.columns):
                # instantiate LabelEncoder
                le = LabelEncoder()
                # fit and transform labels in the column
                dframe.loc[:, column] =\
                    le.fit_transform(dframe.loc[:, column].values)
                # append the `classes_` to our ndarray container
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
                self.all_labels_[idx] = le
        else:
            # no columns specified; assume all are to be encoded
            self.columns = dframe.iloc[:, :].columns
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            for idx, column in enumerate(self.columns):
                le = LabelEncoder()
                dframe.loc[:, column] = le.fit_transform(
                        dframe.loc[:, column].values)
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
        return dframe

    def transform(self, dframe):
        """
        Transform labels to normalized encoding.
        """
        if self.columns is not None:
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[
                    idx].transform(dframe.loc[:, column].values)
        else:
            self.columns = dframe.iloc[:, :].columns
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .transform(dframe.loc[:, column].values)
        #return dframe.loc[:, self.columns].values
        return dframe

    def inverse_transform(self, dframe):
        """
        Transform labels back to original encoding.
        """
        if self.columns is not None:
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .inverse_transform(dframe.loc[:, column].values)
        else:
            self.columns = dframe.iloc[:, :].columns
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .inverse_transform(dframe.loc[:, column].values)
        return dframe


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',default=None,help='Input csv filename')
    parser.add_argument('--columns', required=False, default=None,
                    help='Columns to convert')
    parser.add_argument('--keep', required=False, default=None,
                    help='Columns to keep.')
    parser.add_argument('--outfilename', required=False,
                    help='Filename to write out to.')
    options = parser.parse_args()

    if options.columns:
        options.columns=options.columns.split(",")
    if options.keep:
        options.keep=options.keep.split(",")
    if not options.outfilename:
        options.outfilename = "{}.encoded".format(options.filename)

    df = pd.read_csv(options.filename, low_memory = False) #add low memory false b/c large number of columns
    print "$$$$ OPTIONS $$$$"
    print options.keep
    print "$$$$ COLUMNS $$$$"
    print options.columns
    
    mcle = MultiColumnLabelEncoder(df,columns=options.columns,keep=options.keep)
    
    mcle.transform(df)

    df.to_csv(options.outfilename,index=False)
    print "Output csv at: {}".format(options.outfilename)


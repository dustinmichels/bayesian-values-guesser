import pandas as pd
import numpy as np


all_vars = {
    'V2A': 'country code',
    'V4': 'import in life: family',
    'V10': 'feeling of happiness',
    'V80': 'most serious world problem',
    'V100': 'Hard work brings success',
    'V148': 'Believe in God',
    'V179': 'victim of crime',
    'V178': 'carried knife for security',
    'V187': 'war is necessary',
    'V209': 'Justifiable parents beat children',
    'V211': 'proud of nationality',
    'V225': 'how often use personal computer',
    'V238': 'social class subjective',
    'V248': 'highest educational level',}


def head_and_tail(df, n=4):
    """Show first and last n items in DF"""
    return df.iloc[np.r_[0:n, -n:0]]


def load_files(responses_file='data/wvs_data.csv',
               codebook_file='data/F00003861-WV6_Codebook_v_2014_11_07.xls'):

    # Read responses from csv, discard some unwanted columns
    responses = pd.read_csv(responses_file)
    keep_cols = responses.columns[responses.columns.str.startswith('V')]
    responses = responses[keep_cols]

    # Read the codebook excel file
    codebook = pd.read_excel(codebook_file, header=3, index_col=1)
    codebook.columns = codebook.columns.str.lower()
    codebook = codebook.drop(['filter', 'length', 'var'], axis=1)
    codebook = codebook[codebook.index.str.startswith('V')]

    return responses, codebook


def about_q(codebook, var):
    q = codebook.loc[var]
    label = q.label
    question = q.question.replace('\r\n\r\n', ' ')
    try:
        _cats = q.categories.replace('##', '. ').split('\n')
        _cats = [' ' + c if not c.startswith('-') else c for c in _cats]
        categories = '\n'.join(_cats)
    except:
        categories = 'NaN'
        
    print('Label: {}\n\n'
          'Question: {}\n\n'
          'Categories: \n{}'.format(label, question, categories))

    
def parse_categories(codebook, var):
    vals = codebook.loc[var, 'categories']
    try:
        vals = vals.rstrip('\n').split('\n')
        return pd.DataFrame([x.split('##') for x in vals])
    except AttributeError:
        return "Error! No categories to parse!"

    
def remove_negatives(responses, cutoff_percent=0.1):
    """Remove all rows with any negative responses.
    Pre-removes columns with more negatives than cutoff_percent"""
    
    # set value based off cutoff_percent and # of responses
    cutoff = cutoff_percent * len(responses)
    
    # count negative responses in each column (s is a Series)
    s = (responses < 0).sum()

    # keep_vars: vars where % negative under cutoff
    keep_vars = s[s <= cutoff]
    keep_vars = list(keep_vars.index)

    # filter df down to keep_vars
    df = responses[keep_vars]

    # Drop negative responses
    df = df.mask(df < 0).dropna()    
    return df


def locate_col_lables(new_X, df):
    
    new_X = pd.DataFrame(new_X)
    new_X = new_X.set_index(df.index)
    new_X = new_X.astype('float64')

    use_df = df.astype('float64')
    
    name_dict = {}
    for new_name, new_col in new_X.items():
        col_name, use_df = _find_matching_col(new_col, use_df)
        name_dict[new_name] = col_name
        
    return new_X.rename(name_dict, axis=1)


def _find_matching_col(new_col, use_df):
    for df_name, df_col in use_df.items():
        if new_col.equals(df_col):
            use_df = use_df.drop(df_name, axis=1)
            return df_name, use_df
        
        
        
def get_col_labels(df, codebook):
    return codebook.reindex(df.columns)['label'].to_dict()
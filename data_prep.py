import pandas as pd

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
    'V248': 'highest educational level',
}


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
    print('L:', q.label)
    print('Q:', q.question)
    print('C:')
    print(q.categories.replace('##', '. '))


def parse_cat(var):
    vals = codebook.loc[var, 'categories']
    vals = vals.rstrip('\n').split('\n')
    return pd.DataFrame([x.split('##') for x in vals])

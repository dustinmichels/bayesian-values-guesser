import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.dummy import DummyClassifier

def bayes(df, test_var, NB=MultinomialNB, return_clf=False):
    """Given df and test_var, runs Bayesian and baseline classifier.
    Returns results as (clf_score, base_score) tuple."""
    
    # y is test var, X is all other vars
    y = df[test_var]
    X = df.drop(test_var, axis=1)
    
    # split into test/training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42)
    
    # create, fit, and score bayesian classifier
    clf = NB()
    clf.fit(X_train, y_train)
    clf_score = clf.score(X_test, y_test)
    
    # create, fit, and score baseline classifier
    base = DummyClassifier(strategy='most_frequent', random_state=0)
    base.fit(X_train, y_train)
    base_score = base.score(X_test, y_test)
    
    # return either classifier or scores
    if return_clf:
        return clf
    return clf_score, base_score


def test_all_vars(df, all_vars, NB=MultinomialNB):
    
    # iteratve over all keys, making list of dicts with score data
    res = []
    for k, v in all_vars.items():
        score, base_score = bayes(df, test_var=k, NB=NB)
        res.append(dict(var=k, des=v, score=score, baseline=base_score))
        
    # convert list of dicts to DF
    res_df = pd.DataFrame(res, columns=['var','des','baseline','score'])

    # compute "improve" column (score - baseline)
    res_df['improve'] = res_df['score'] - res_df['baseline']

    # sort DF by improvement
    res_df.sort_values(by=['improve'], ascending=False)
    
    return res_df
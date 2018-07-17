import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import gzip
import difflib
import datetime
import time
from scipy import stats
from scipy.stats import chi2_contingency

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    searches = pd.read_json(searchdata_file, lines=True)
    odd_id = searches[(searches['uid'] %2 != 0)]
    even_id = searches[(searches['uid'] %2 == 0)]
    odds_searched = odd_id[(odd_id['search_count'] > 0)]
    odd_unsearched = odd_id[(odd_id['search_count'] == 0)]

    evens_searched = even_id[(even_id['search_count'] > 0)]
    evens_unsearched = even_id[(even_id['search_count'] == 0)]

    
    obs1 = np.array([[odds_searched.shape[0], odd_unsearched.shape[0]], [evens_searched.shape[0], evens_unsearched.shape[0]]])
    chi = (chi2_contingency(obs1))
    mannwhitneyu = stats.mannwhitneyu(odd_id['search_count'], even_id['search_count'])

    odds_searched = odds_searched[(odds_searched['is_instructor'] == True)]
    odd_unsearched = odd_unsearched[(odd_unsearched['is_instructor'] == True)]

    evens_searched = evens_searched[(evens_searched['is_instructor'] == True)]
    evens_unsearched = evens_unsearched[(evens_unsearched['is_instructor'] == True)]

    odd_id = odd_id[(odd_id['is_instructor'] == True)]
    even_id = even_id[(even_id['is_instructor'] == True)]

    obs1 = np.array([[odds_searched.shape[0], odd_unsearched.shape[0]], [evens_searched.shape[0], evens_unsearched.shape[0]]])
    chi2 = (chi2_contingency(obs1))

    mannwhitneyu2 = stats.mannwhitneyu(odd_id['search_count'], even_id['search_count'])

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=chi[1],
        more_searches_p=mannwhitneyu[1],
        more_instr_p=chi2[1],
        more_instr_searches_p=mannwhitneyu2[1],
    ))


if __name__ == '__main__':
    main()
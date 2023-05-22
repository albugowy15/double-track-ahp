"""Python external modules for working with data sets"""
import pandas as pd

from AHP import AHP

df = pd.read_csv("assets/dataset.csv")

criteria = df.columns
criteria = criteria.drop(labels="skill_field")
alternative = df.get(key="skill_field")

# determine pairwise comparison matrix
pairwise_matrix = [
    [1, 2, 3, 4, 5, 6],
    [1/2, 1, 3/2, 4/2, 5/2, 6/2],
    [1/3, 2/3, 1, 4/3, 5/3, 6/3],
    [1/4, 2/4, 3/4, 1, 5/4, 6/4],
    [1/5, 2/5, 3/5, 4/5, 1, 6/5],
    [1/6, 2/6, 3/6, 4/6, 5/6, 1]
]

ahp = AHP(df, criteria, alternative, pairwise_matrix)

# normalize matrix
ahp.normalize_matrix()

# calculate criteria weight
ahp.calculate_criteria_weight()

# check consistency ratio (CR)
ahp.calculate_consistency()

# display all criteria with their weight
ahp.show_criteria_weights()

ahp.show_recommendation()

"""Python external modules for working with data sets"""
import pandas as pd

from AHP import AHP

df = pd.read_csv("assets/dataset.csv")

criteria = df.columns
criteria = criteria.drop(labels="skill_field")
alternative = df.get(key="skill_field")

# determine pairwise comparison matrix
pairwise_matrix = [
    [1, 6, 2, 1, 1, 3],
    [1/6, 1, 3, 1, 1/6, 4],
    [1/2, 1/3, 1, 1, 1/5, 1/7],
    [1, 1, 1, 1, 1/3, 4],
    [1, 6, 5, 3, 1, 1],
    [1/3, 1/4, 7, 1/4, 1, 1]
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

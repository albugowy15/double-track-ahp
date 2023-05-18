import pandas as pd


class AHP:
  def __init__(self, df, criteria, alternative, pairwise_matrix) -> None:
    self.df = df
    self.criteria = criteria
    self.alternative = alternative
    self.length = len(criteria)
    self.pairwise_matrix = pairwise_matrix
    self.calculated_sum = [0.0] * self.length
    self.normalized_matrix = [[0.0] * self.length for _ in range(self.length)]
    self.criteria_weights = [0.0] * self.length
    self.random_index = [0.0, 0.0, 0.0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    self.ci = 0.0
    self.cr = 0.0

  def calculate_sum(self):
    for x in range(self.length):
      for j in range(self.length):
        self.calculated_sum[x] += self.pairwise_matrix[j][x]

    return self.calculated_sum
    
  def normalize_matrix(self):
    for x in range(self.length):
      for y in range(self.length):
        self.normalized_matrix[x][y] = (self.pairwise_matrix[x][y] / self.calculated_sum[y])

    return self.normalized_matrix
  
  def calculate_criteria_weight(self):
    for x in range(self.length):
      sum_avg = 0.0
      for y in range(self.length):
        sum_avg += self.normalized_matrix[x][y]
        if y == 5:
          self.criteria_weights[x] = sum_avg / self.length
    
    return self.criteria_weights
  
  def calculate_consistency(self):
    temp = [[0.0] * self.length for _ in range(self.length)]
    weighted_sum_value = [0.0] * self.length
    ratio = [0.0] * self.length
    for x in range(self.length):
      for y in range(self.length):
        temp[x][y] = self.pairwise_matrix[x][y] * self.criteria_weights[y]
        weighted_sum_value[x] += temp[x][y]
            
    for x in range(self.length):
      ratio[x] += weighted_sum_value[x] / self.criteria_weights[x]

    sum_temp = 0.0
    for val in ratio:
      sum_temp += val
    lambda_max = sum_temp / self.length    
    self.ci = (lambda_max - self.length) / (self.length - 1)   
    self.cr = self.ci / self.random_index[self.length]
    if self.cr < 0.10:
      print(f"CR is OK\nCR = {self.cr}")
    else:
      print(f"CR is BAD\nCR = {self.cr}")

  def show_criteria_weights(self):
    criteria_dict = {key: value for key, value in zip(self.criteria, self.criteria_weights)}
    sorted_criteria =  dict(sorted(criteria_dict.items(), key=lambda x: x[1], reverse=True))
    for criteria, weight in sorted_criteria.items():
      print(f"{criteria}: {weight}")
  
  def show_recommendation(self):
    decision_matrix = df.drop(labels="skill_field", axis=1).values
    normalized_decision_matrix = []

    for row in decision_matrix:
      row_sum = sum(row)
      normalized_row = [val / row_sum for val in row]
      normalized_decision_matrix.append(normalized_row)

    weighted_scores = []
    for row in normalized_decision_matrix:
      weighted_score = sum([val * weight for val, weight in zip(row, self.criteria_weights)])
      weighted_scores.append(weighted_score)
    
    total_weighted_score = sum(weighted_scores)
    overall_priorities = [score / total_weighted_score for score in weighted_scores]

    ranked_alternatives = sorted(zip(self.alternative, overall_priorities), key=lambda x: x[1], reverse=True)

    print(f"\n")
    for alternative, priority in ranked_alternatives:
      print(f"{alternative}: {priority}")

        
        


if __name__ == '__main__':
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
  # sum value for each column
  ahp.calculate_sum()

  # normalize matrix
  ahp.normalize_matrix()

  # calculate criteria weight
  ahp.calculate_criteria_weight()

  # check consistency ratio (CR)
  ahp.calculate_consistency()

  # display all criteria with their weight
  ahp.show_criteria_weights()

  ahp.show_recommendation()


"""Python external modules for working with data sets"""
import pandas as pd


class AHP:
    """Class for AHP calculation"""

    def __init__(self, data_frame, input_criteria, input_alternative, input_pairwise_matrix):
        self.data_frame = data_frame
        self.criteria = input_criteria
        self.alternative = input_alternative
        self.length = len(input_criteria)
        self.pairwise_matrix = input_pairwise_matrix
        self.calculated_sum = [0.0] * self.length
        self.normalized_matrix = [[0.0] * self.length for _ in range(self.length)]
        self.criteria_weights = [0.0] * self.length
        self.random_index = [0.0, 0.0, 0.0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        self.consistency_index = 0.0
        self.consistency_ratio = 0.0

    def __calculate_sum(self):
        for col in range(self.length):
            for row in range(self.length):
                self.calculated_sum[col] += self.pairwise_matrix[row][col]

        return self.calculated_sum

    def normalize_matrix(self):
        """Normalize the pairwise matrix"""
        self.__calculate_sum()
        for row in range(self.length):
            for col in range(self.length):
                self.normalized_matrix[row][col] = \
                    self.pairwise_matrix[row][col] / self.calculated_sum[col]
        return self.normalized_matrix

    def calculate_criteria_weight(self):
        """Calculate the weight of each criteria"""
        for row in range(self.length):
            self.criteria_weights[row] = sum(self.normalized_matrix[row]) / self.length
        return self.criteria_weights

    def calculate_consistency(self):
        """Calculate and check consistency ration"""
        temp = [[0.0] * self.length for _ in range(self.length)]
        weighted_sum_value = [0.0] * self.length
        ratio = [0.0] * self.length
        for row in range(self.length):
            for col in range(self.length):
                temp[row][col] = self.pairwise_matrix[row][col] * self.criteria_weights[col]
                weighted_sum_value[row] += temp[row][col]
        for row in range(self.length):
            ratio[row] += weighted_sum_value[row] / self.criteria_weights[row]

        lambda_max = sum(ratio) / self.length
        self.consistency_index = (lambda_max - self.length) / (self.length - 1)
        self.consistency_ratio = self.consistency_index / self.random_index[self.length]
        if self.consistency_ratio < 0.10:
            print(f"CR is OK\nCR = {self.consistency_ratio}")
        else:
            print(f"CR is BAD\nCR = {self.consistency_ratio}")

    def show_criteria_weights(self):
        """Display sorted criteria weights in desc order"""
        criteria_dict = dict(zip(self.criteria, self.criteria_weights))
        sorted_criteria =  dict(sorted(criteria_dict.items(), key=lambda x: x[1], reverse=True))
        for key, value in sorted_criteria.items():
            print(f"{key}: {value}")

    def show_recommendation(self):
        """Display final recommendation for all alternatives"""
        decision_matrix = self.data_frame.drop(labels="skill_field", axis=1).values
        normalized_decision_matrix = []

        for row in decision_matrix:
            row_sum = sum(row)
            normalized_row = [val / row_sum for val in row]
            normalized_decision_matrix.append(normalized_row)

        weighted_scores = []
        for row in normalized_decision_matrix:
            weighted_score = sum(val * weight for (val, weight) in zip(row, self.criteria_weights))
            weighted_scores.append(weighted_score)
        total_weighted_score = sum(weighted_scores)
        overall_priorities = [score / total_weighted_score for score in weighted_scores]
        ranked_alternatives = sorted(zip(self.alternative, overall_priorities), \
                                        key=lambda x: x[1], \
                                        reverse=True)
        print("\n")
        for key, val in ranked_alternatives:
            print(f"{key}: {val}")


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

    # normalize matrix
    ahp.normalize_matrix()

    # calculate criteria weight
    ahp.calculate_criteria_weight()

    # check consistency ratio (CR)
    ahp.calculate_consistency()

    # display all criteria with their weight
    ahp.show_criteria_weights()

    ahp.show_recommendation()

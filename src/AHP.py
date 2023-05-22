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

    def __mpc_sub_criteria(self, length):
        sub_mpc = [[0.0] * length for _ in range(length)]
        sub_sum = [0.0] * length
        sub_weights = [0.0] * length

        for row in range(length):
            for col in range(length):
                sub_mpc[row][col] = (col + 1) / (row + 1)

        # calculate col sum
        for col in range(length):
            for row in range(length):
                sub_sum[col] += sub_mpc[row][col]

        # normalize mpc
        for row in range(length):
            for col in range(length):
                sub_mpc[row][col] /= sub_sum[col]
            sub_weights[row] = sum(sub_mpc[row]) / length

        return sub_weights

    def __calculate_sub_criteria_priority_vector(self):
        all_sub = []
        for _ in range(5):
            all_sub.append(self.__mpc_sub_criteria(4))
        return all_sub


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
        """Calculate and check consistency ratio"""
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
        all_sub_vector = self.__calculate_sub_criteria_priority_vector()
        len_alternative = len(self.alternative)
        alternative_matrix = [[0.0 for _ in range(self.length)] for _ in range(len_alternative)]
        alternative_hpt = []

        for row in range(len_alternative):
            for col in range(self.length):
                sub_vec_idx = decision_matrix[row][col] - 1
                alternative_matrix[row][col] = all_sub_vector[col][sub_vec_idx] * \
                    self.criteria_weights[col]
            alternative_hpt.append(sum(alternative_matrix[row]))

        ranked_alternatives = sorted(zip(self.alternative, alternative_hpt), \
                                        key=lambda x: x[1], \
                                        reverse=True)
        print("\n")
        for key, val in ranked_alternatives:
            print(f"{key}: {val}")

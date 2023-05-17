#input a chromosome 
#return penalty for constraint violation
# this is a class

class ConstraintManager:
    def __init__(self, constraints):
        self.constraints = constraints  # list of tuples with (min, max) for each gene in the chromosome

    def evaluate_chromosome(self, chromosome):
        penalty = 0
        for gene, constraint in zip(chromosome, self.constraints):
            min_val, max_val = constraint
            if gene < min_val:
                penalty += min_val - gene  # or some other penalty function
            elif gene > max_val:
                penalty += gene - max_val  # or some other penalty function
        return penalty

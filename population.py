import numpy as np 
import random
import math
from bisect import bisect_right
from battery import battery_degradation_cost
from loads import LoadManager

EPS = pow(10,-30)
min_f = pow(10,10)
<<<<<<< HEAD
CHARGING_LEVELS = 3

class GAPopulation:
    @staticmethod
    def mutation(self,individual):
        individual = individual['battery_schedule']
        n = len(individual)
        pos = random.sample(range(n), 2) 
        best_cost = float('inf')
        best_value = -1
        
        for pos1 in pos:
            for value in range(-CHARGING_LEVELS,CHARGING_LEVELS+1):
                new_individual = individual[:pos1] + [value] + individual[pos1+1:]
                cost = self.get_fitness(new_individual)
                if cost < best_cost:
                    best_cost = cost
                    best_value = value
            
            individual = individual[:pos1] + [best_value] + individual[pos1+1:]
            creature = {'battery_schedule':individual,'shed_l_schedule':individual['shed_l_schedule'],'shift_l_schedule':individual['shift_l_schedule']}
        
        return creature
    
        
    @staticmethod
    def get_fitness(self,creature):
        grid_load = self.load_manager.get_grid_load(creature)
        shed_loads = [i if creature['shed_l_schedule'][i] == 1 else 0 for i in range(len(creature['shed_l_schedule']))]
        diesel_period = creature['diesel'][1]
        
        bd_cost = battery_degradation_cost(creature['battery_schedule'])
        
        return self.calculator.get_total_cost(grid_load,shed_loads,diesel_period) + bd_cost

=======

class GAPopulation:
    @staticmethod
    @staticmethod
    def mutation(self, chromosome, mutation_rate):
        mutated_chromosome = dict(chromosome)
        keys = list(chromosome.keys())

        for key in keys:
            gene_range = None

            # Set the gene range based on the key/series
            if key == 'battery_schedule':
                gene_range = (-self.CHARGING_LEVELS, self.CHARGING_LEVELS)  # Example range for series1
            elif key == 'shed_l_schedule':
                gene_range = (0,1)  # Example range for series3

            if gene_range is not None:
                for i in range(len(mutated_chromosome[key])):
                    if random.random() < mutation_rate:
                        # Mutate the gene at index i
                        mutated_gene = random.randint(gene_range[0], gene_range[1])
                        mutated_chromosome[key][i] = mutated_gene

        return mutated_chromosome

        
    @staticmethod
    def get_fitness(self,creature):
        
        operating_cost = self.calculator.get_total_cost(creature)
        bd_cost = battery_degradation_cost(creature['battery_schedule'])
        
        return operating_cost+ bd_cost
    
>>>>>>> main_sl
    @staticmethod
    def crossover(self,chromosome1,chromosome2):
        min_cost = float('inf')
        keys = list(chromosome1.keys())
        #print(keys)
<<<<<<< HEAD
        #key = keys[random.randint(0,len(keys)-1)]
        key = keys[0]
        # print(self.get_fitness(self,chromosome1))
        # print(self.get_fitness(self,chromosome2))
        
=======
        key = keys[random.randint(0,len(keys)-1)]
        #key = keys[0]
>>>>>>> main_sl
        crossover_point=0
        for i in range(0,len(chromosome1[key])):
            test_creature = dict(chromosome1)
            test_creature[key] = chromosome1[key][:i] + chromosome2[key][i:]
            cost1 = self.get_fitness(self,test_creature)
            if cost1   < min_cost:
                min_cost = cost1 
                crossover_point = i
        offspring1 = dict(chromosome1)
        offspring1[key] = chromosome1[key][:crossover_point] + chromosome2[key][crossover_point:]
        #print(self.get_fitness(self,chromosome1),self.get_fitness(self,chromosome2),self.get_fitness(self,offspring1))
        return offspring1
    
    def build_probability(self):
        global min_f
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den =0
        for c in self.creatures:
            f = GAPopulation.get_fitness(self,c)
            min_f = min(f,min_f)
            self.fitness.append(f)
            prob =  1/math.sqrt(math.sqrt(max(100,f-min_f)))
            #prob = 100000-f
            #print("f",f,prob)    
            probs.append(prob)
            prob_den += prob
        self.probs = list(map(lambda x:x/prob_den,probs))

        for i in range(1,len(self.probs)-1):
            self.probs[i] += self.probs[i-1]
            self.probs[-1] = 1+ EPS
       
        
    def get_stochastic(self):
        val = random.random() 
        idx = bisect_right(self.probs,val) 
        return self.creatures[idx]

<<<<<<< HEAD
    def __init__(self,T,M1,M2,calculator,load_manager,creatures=None):
=======
    def __init__(self,T,M1,M2,calculator,constraint_manager,creatures=None):
>>>>>>> main_sl
        self.creatures = creatures
        self.CHARGING_LEVELS=10
        self.T = T
        self.M1 = M1
        self.M2 = M2
        self.calculator = calculator
<<<<<<< HEAD
        self.load_manager = load_manager
        
=======
        self.constraint_manager = constraint_manager

>>>>>>> main_sl
        if creatures is not None:
            self.n = len(creatures)
            self.build_probability()

<<<<<<< HEAD
    def init_population(self,size):
        self.n = size
        self.creatures = []
        for _ in range(size): 
=======
    def init_population(self,size,CHARGING_LEVELS,shiftable_loads):
        self.n = size
        self.creatures = []
        while(len(self.creatures)<size):
>>>>>>> main_sl
            creature ={}
            creature['battery_schedule'] = np.round([max(min(random.gauss(0, self.CHARGING_LEVELS/2),self.CHARGING_LEVELS),-self.CHARGING_LEVELS) for _ in range(self.T)]).astype(int).tolist()
            creature['shift_l_schedule'] = [random.randint(shiftable_loads[i]['start'], shiftable_loads[i]['end']-shiftable_loads[i]['duration']) for i in range(self.M1)]
            creature['shed_l_schedule'] = [random.randint(0,1) for i in range(self.M2)]
<<<<<<< HEAD
           # creature['diesel'] = [random.randint(0,23), random.randint(0,10)]
            creature['diesel'] = [0,0]
=======
            if(self.constraint_manager.check_constraints(creature) == False):
                continue
>>>>>>> main_sl

            self.creatures.append(creature)
        self.build_probability()

    def next_generation(self,size):
        n_crs = []
<<<<<<< HEAD
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = GAPopulation.crossover(self,c1,c2)
            n_crs.append(offs)
        return GAPopulation(self.T,self.M1,self.M2,self.calculator,self.load_manager,n_crs)
=======
    
        while(len(n_crs)<size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = GAPopulation.crossover(self,c1,c2)
            if(self.constraint_manager.check_constraints(offs) == False):
                continue
            n_crs.append(offs)
        return GAPopulation(self.T,self.M1,self.M2,self.calculator,self.constraint_manager,n_crs)
>>>>>>> main_sl

    def get_best(self):
        best_val = self.fitness[0]
        best_idx=0
        for i in range(1,len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return (self.creatures[best_idx],best_val)

<<<<<<< HEAD
    def print_stats(self):
=======
    def print_stats(self,load_manager):
>>>>>>> main_sl
        global actual_building, actual_solar
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        print('Average Cost of Population  ' + str(avg_fitness)) 
        print(self.get_best())
        print("Daily - Electricity_cost of Best Creature:",self.get_fitness(self,self.get_best()[0])) 
<<<<<<< HEAD
=======
        #print("grid_load = ",load_manager.get_grid_load(self.get_best()[0]))
        #print("creature is ",self.get_best()[0])
>>>>>>> main_sl

    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)

    def set_charging_levels(self,cl):
        self.CHARGING_LEVELS=cl
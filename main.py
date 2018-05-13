from rush import Student, Frat, Rush
import random 
import numpy as np

NUM_STUDENTS = 3 #this should be changed 
NUM_FRATS = 2 #this can also be changed
NUM_SWAPS=2 #this should be changed 
STRATEGY = "gale"
CAPACITY_MEAN = 2 #11.88 for real
CAPACITY_VARIANCE = 0.2 #unclear, potentially also add floor/ceiling 

def generate_rush_params():
	frats = []
	students = []
	list_of_students = []
	list_of_frats = []
	for i in range(NUM_STUDENTS):
		students.append(Student("S%d"%i, []))
	for i in range(NUM_FRATS):
		random_capacity = np.rint(np.random.normal(CAPACITY_MEAN, CAPACITY_VARIANCE))
		random_acceptable = random.sample(students, len(students))
		frats.append(Frat("F%d"%i, random_capacity, random_acceptable))
	for s in students:
		s.acceptable = random.sample(frats, len(frats)) #randomize the student's preferences
	strategies = {}
	for f in frats:
		strategies[f] = STRATEGY
	return frats, students, strategies

def main():
	frats, students, strategies = generate_rush_params()
	rush = Rush(frats, students, num_swaps=NUM_SWAPS, strategies=strategies)
	print "BEFORE RUSH"
	print rush
	rush.apply_swaps()
	rush.bid_and_pledge()
	print "\nAFTER RUSH"
	print rush

if __name__ == "__main__":
	main()
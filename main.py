from rush import Student, Frat, Rush
import random 
import numpy as np
import sys

NUM_STUDENTS = 400 
NUM_FRATS = 25
NUM_SWAPS= 10 
STRATEGY = "gale"
CAPACITY_MEAN = 11.88 #11.88 for real
CAPACITY_VARIANCE = 5 
FRAT_DIVISIONS = 7
STUDENT_DIVISIONS = 40

#TODO - add latent parmaeter for type of student 

def generate_rush_params():
	frats = []
	students = []
	for i in range(NUM_STUDENTS):
		students.append(Student("S%d"%i, []))
	student_split = np.array_split(np.asarray(students), STUDENT_DIVISIONS)
	for i in range(NUM_FRATS):
		random_capacity = np.rint(np.random.normal(CAPACITY_MEAN, CAPACITY_VARIANCE))
		random_acceptable = []
		for s in student_split:
			random_acceptable.extend(random.sample(s, len(s)))
		# random_acceptable = random.sample(students, len(students)) #completely random
		frats.append(Frat("F%d"%i, random_capacity, random_acceptable))
	frat_split = np.array_split(np.asarray(frats), FRAT_DIVISIONS)
	for s in students:
		random_acceptable = []
		for f in frat_split:
			random_acceptable.extend(random.sample(f, len(f)))
		s.acceptable = random_acceptable
		# s.acceptable = random.sample(frats, len(frats)) #completely random
	strategies = {}
	for f in frats:
		strategies[f] = STRATEGY
	return frats, students, strategies

def main():
	frats, students, strategies = generate_rush_params()
	rush_no_swaps = Rush(frats, students, num_swaps=0, strategies=strategies)
	no_swap_outcomes = rush_no_swaps.get_gale_shapley(reset=True)
	rush = Rush(frats, students, num_swaps=NUM_SWAPS, strategies=strategies)
	print "BEFORE RUSH"
	print rush
	rush.apply_swaps()
	rush.bid_and_pledge()
	print "\nAFTER RUSH"
	print rush
	generate_metrics(rush, no_swap_outcomes)

def generate_metrics(rush, no_swap_outcomes):
	print("----------------\nMETRICS\n----------------\n")
	total_num_pledges = 0
	for f in rush.frats:
		num_pledges = len(f.pledges)
		total_num_pledges += len(f.pledges)
		ranks = []
		no_swap_ranks = []
		pledge_overlap = 0
		for p in f.pledges:
			ranks.append(f.acceptable.index(p) + 1)
			if p in no_swap_outcomes[f]:
				pledge_overlap += 1
		for p in no_swap_outcomes[f]:
			no_swap_ranks.append(f.acceptable.index(p) + 1)
		print("------------------------Fraternity: " + f.name + "------------------------")
		print("Capacity: " + str(f.capacity))
		print("Number of Students: " + str(num_pledges))
		print("Capacity Filled: " + str(100 * num_pledges/f.capacity if f.capacity else 0) + "%")
		print("Number of Students without Swaps: " + str(len(no_swap_outcomes[f])))
		print("Student Overlap: " + str(pledge_overlap))
		print("Student Overlap Pct.: " + str(100 * pledge_overlap / num_pledges if num_pledges else 0) + "%")
		print("Average No Swap Ranking of Matched Students: " + str(np.mean(no_swap_ranks)))
		print("Average Ranking of Matched Students: " + str(np.mean(ranks)))
	print("Total Number of Students Matched: " + str(total_num_pledges))

if __name__ == "__main__":
	main()
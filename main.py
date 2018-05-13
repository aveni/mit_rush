from rush import Student, Frat, Rush
import random 
import numpy as np

NUM_STUDENTS = 300 
NUM_FRATS = 25
NUM_SWAPS=20 
STRATEGY = "gale"
CAPACITY_MEAN = 12 #11.88 for real
CAPACITY_VARIANCE = 2 

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
	for f in rush.frats:
		ranks = []
		no_swap_ranks = []
		pledge_overlap = 0
		for p in f.pledges:
			ranks.append(f.acceptable.index(p) + 1)
			if p in no_swap_outcomes[f]:
				pledge_overlap += 1
		for p in no_swap_outcomes[f]:
			no_swap_ranks.append(f.acceptable.index(p) + 1)
		print("Fraternity: " + f.name)
		print("Number of Pledges: " + str(len(f.pledges)))
		print("Number of Pledges without Swaps: " + str(len(no_swap_outcomes[f])))
		print("Pledge Overlap: " + str(pledge_overlap))
		print("Pledge Overlap Pct.: " + str(100 * pledge_overlap / len(f.pledges)) + "%")
		print("Average No Swap Pledge Ranking: " + str(np.mean(no_swap_ranks)))
		print("Average Pledge Ranking: " + str(np.mean(ranks)))

if __name__ == "__main__":
	main()
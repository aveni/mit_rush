from rush import Student, Frat, Rush
import random 
# s1 = Student("S1", [])
# s2 = Student("S2", [])
# s3 = Student("S3", [])

# f1 = Frat("F1", 2, [s1, s2, s3])
# f2 = Frat("F2", 2, [s1, s2, s3])

# s1.acceptable = [f1, f2]
# s2.acceptable = [f1, f2]
# s3.acceptable = [f1, f2]

# frats = [f1, f2]
# strategies = {f1:"top", f2:"top"}
# students = [s1, s2, s3]

NUM_STUDENTS = 3 #this should be changed 
NUM_FRATS = 2 #this can also be changed
NUM_SWAPS=2 #this should be changed 
CAPACITY = 2 #min_capacity is 1, max_capacity is number of students 
STRATEGY = "gale"

def generate_rush_params():
	frats = []
	students = []
	list_of_students = []
	list_of_frats = []
	for i in range(NUM_STUDENTS):
		students.append(Student("S%d"%i, []))
	for i in range(NUM_FRATS):
		frats.append(Frat("F%d"%i, CAPACITY, random.sample(students, len(students))))
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
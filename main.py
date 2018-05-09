from rush import Student, Frat, Rush

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

num_students = 3
num_frats = 2
num_swaps=2
capacity = 2
strategy = "gale"

frats = []
students = []
for i in range(num_students):
	students.append(Student("S%d"%i, []))
for i in range(num_frats):
	frats.append(Frat("F%d"%i, capacity, students))
for s in students:
	s.acceptable = frats
strategies = {}
for f in frats:
	strategies[f] = strategy


rush = Rush(frats, students, num_swaps=num_swaps, strategies=strategies)
print "BEFORE RUSH"
print rush

rush.apply_swaps()
rush.bid_and_pledge()

print "\nAFTER RUSH"
print rush
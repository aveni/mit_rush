import numpy as np

class Frat:
	def __init__(self, name, capacity, acceptable):
		self.name = name
		self.capacity = capacity
		self.acceptable = acceptable
		self.pledges = []

	def __repr__(self):
		string = "%s (%d): %s" % (self.name, self.capacity, self.acceptable[0].name if len(self.acceptable)>0 else "None")

		for s in self.acceptable[1:]:
			string += (" > " + s.name)
		string += "\t|\t%s" % str([p.name for p in self.pledges])
		return string


class Student:
	def __init__(self, name, acceptable):
		self.name = name
		self.acceptable = acceptable
		self.frat = None		

	def favorite(self, bids):
		if len(bids) == 0:
			return None
		else:
			ix = np.argmax(np.isin(self.acceptable, bids))
			return self.acceptable[ix]

	def __repr__(self):
		string = "%s: %s" % (self.name, self.acceptable[0].name if len(self.acceptable)>0 else "None")

		for f in self.acceptable[1:]:
			string += (" > " + f.name)
		string += "\t|\t%s" % (str(self.frat.name) if self.frat else "None")
		return string



# ASSUMPTION: ONLY 1 SWAP PER KID ALLOWED
class Rush:
	def __init__(self, frats, students, num_swaps, strategies={}):
		self.frats = frats
		self.students = students
		self.num_swaps = num_swaps
		self.strategies = strategies

	def get_gale_shapley(self, reset=True):
		counter = {}
		for f in self.frats:
			counter[f] = 0

		finished = False
		while not finished:
			finished = True
			for f in self.frats:
				if (len(f.pledges) < f.capacity) and counter[f] < len(f.acceptable):
					finished = False
					proposal = f.acceptable[counter[f]]
					if (f in proposal.acceptable and ((proposal.frat is None) or (proposal.acceptable.index(f) < proposal.acceptable.index(proposal.frat)))):
						if proposal.frat:
							proposal.frat.pledges.remove(proposal)
						proposal.frat = f
						f.pledges.append(proposal)
					counter[f] += 1

		# Save GS result
		output = {}
		for f in self.frats:
			output[f] = f.pledges
		
		# Reset frat and student outcomes
		if reset:
			for f in self.frats:
				f.pledges = []
			for s in self.students:
				s.frat = None
				
		return output

	def bid_and_pledge(self):
		self.get_gale_shapley(reset=False)

	def apply_swaps(self):
		self.swap_dict = {}
		for f in self.frats:
			strat = self.strategies[f]
			if strat == "top":
				self.swap_dict[f] = self.get_swap_top(f)
			if strat == "gale":
				self.swap_dict[f] = self.get_swap_gale_shapley(f)
			if strat == "gale-smart":
				self.swap_dict[f] = self.get_swap_smart_gale_shapley(f)


		print "SWAPS"
		for f in self.frats:
			print f.name, [s.name for s in self.swap_dict[f]]

		# In-order swapping means outcome is deterministic
		# Equivalent to adding 1+epsilon utility to a frat who performs a swap
		for s in self.students:
			new_acceptable = s.acceptable[:]
			for i in range (1, len(s.acceptable)):
				if s in self.swap_dict[s.acceptable[i]]:
					ix = new_acceptable.index(s.acceptable[i])
					temp = new_acceptable[ix-1]
					new_acceptable[ix-1] = new_acceptable[ix]
					new_acceptable[ix] = temp
			if s in self.swap_dict[s.acceptable[0]]:
				new_acceptable.remove(s.acceptable[0])
				new_acceptable = [s.acceptable[0]] + new_acceptable
			s.acceptable = new_acceptable

	def get_swap_top(self, frat):
		return frat.acceptable[:self.num_swaps]

	def get_swap_gale_shapley(self, frat):
		return self.get_gale_shapley()[frat][:self.num_swaps]

	def get_swap_smart_gale_shapley(self, frat):
		gs = self.get_gale_shapley()[frat][:self.num_swaps]
		for pledge in gs:
			ix = pledge.acceptable.index(frat)
			if ix != len(pledge.acceptable)-1:
				if pledge not in pledge.acceptable[ix+1].acceptable:
					gs.remove(pledge)
		return gs

	def __repr__(self):
		string = ""
		string += "----------------\nFrats\n----------------\n"
		for f in self.frats:
			string += (str(f)+"\n")
		string += "----------------\nStudents\n----------------\n"
		for s in self.students:
			string += (str(s)+"\n")
		return string

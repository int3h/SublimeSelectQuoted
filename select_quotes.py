import sublime, sublime_plugin

class SelectQuoted(sublime_plugin.TextCommand):
	def run(self, edit, around=False):
		selections = self.view.sel()
		newSel = []

		for originalRegion in selections:
			# If point a proceeds point b, reverse it to make calculations easier
			region = originalRegion if originalRegion.a <= originalRegion.b else sublime.Region(originalRegion.b, originalRegion.a)

			newRegion = self.getStringRegion(region, around)

			if newRegion is None:
				newSel.append(originalRegion)
			else:
				# Un-reverse region if we reversed it at the start
				newRegion = newRegion if originalRegion.a <= originalRegion.b else sublime.Region(newRegion.b, newRegion.a)
				newSel.append(newRegion)

		selections.clear()
		for reg in newSel:
			selections.add(reg)


	def getStringRegion(self, region, around=False):
		"""
		If region resides within a single string, return a Region which encompasses the whole
		string. Otherwise, returns the original region.
		"""
		# Shrink the end by one unit, keeping a <= b, because we really care about the character
		# right before the end cursor, not after.
		region = sublime.Region(region.a, max(region.a, region.b - 1))

		# Mark sure the entire selected region lies within a quoted string
		for pos in range(region.a, region.b + 1):
			if self.view.score_selector(pos, "string.quoted") <= 0:
				return None

		# Turn on 'round' implicitly if...
		# The start of the selection is a quote
		if self.view.score_selector(region.a, "punctuation.definition.string") > 0:
			around = True
		# The end of the selection is a quote
		if self.view.score_selector(region.b, "punctuation.definition.string") > 0:
			around = True
		# The selected region is abutted by quotes on either side
		if (self.view.score_selector(region.a - 1, "punctuation.definition.string") > 0 and
		    self.view.score_selector(region.b + 1, "punctuation.definition.string") > 0):
			around = True

		# Predicates for if we should continue expanding the selection foreward/back
		if around:
			# We should only stop when we're on a quote, but the next character isn't a quote
			shouldExpandA = lambda a:((not (self.view.score_selector(a, "punctuation.definition.string") > 0 and not self.view.score_selector(a - 1, "punctuation.definition.string") > 0)) and (self.view.score_selector(a - 1, "string.quoted") > 1))
			shouldExpandB = lambda b:((not (self.view.score_selector(b - 1, "punctuation.definition.string") > 0 and not self.view.score_selector(b, "punctuation.definition.string") > 0)) and (self.view.score_selector(b, "string.quoted") > 1))
		else:
			# We should only stop as soon as we see a quote
			shouldExpandA = lambda a:((not self.view.score_selector(a - 1, "punctuation.definition.string") > 0) and (self.view.score_selector(a - 1, "string.quoted") > 1))
			shouldExpandB = lambda b:((not self.view.score_selector(b, "punctuation.definition.string") > 0) and (self.view.score_selector(b, "string.quoted") > 1))

		# Expand the selection by expanding the start, then the end
		expandedRegion = sublime.Region(region.a, region.b)
		expandedA = region.a
		expandedB = region.b
		while shouldExpandA(expandedA):
			expandedA = expandedA - 1
		while shouldExpandB(expandedB):
			expandedB = expandedB + 1

		return sublime.Region(expandedA, expandedB)


	def description(self, around=False):
		if around:
			return "Expand Selection to Quotes"
		else:
			return "Expand Selection to Quoted"
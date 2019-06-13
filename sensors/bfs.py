
def find_shortest_path(graph, start, end, path=[]):
	# print(start)
	path = path + [start]
	if start == end:
		return path
	if start not in graph:
		return None
	shortest = None
	for node in graph[start]:
		if node not in path:
			newpath = find_shortest_path(graph, node, end, path)
			if newpath:
				if not shortest or len(newpath) < len(shortest):
					shortest = newpath
	return shortest


# using dict to represent graph of tag locations
graph = {	0: [1, 2],
			1: [0, 49],
			30: [31],
			31: [30, 32],
			32: [31, 33],
			33: [32, 34],
			34: [33, 35],
			35: [34, 36],
			36: [35, 37],
			37: [36, 38],
			38: [37, 39],
			39: [38, 40],
			40: [39, 45],
			45: [40, 46],
			46: [45, 47],
			47: [46, 48],
			48: [47, 49],
			49: [48, 1]
		}


print("0 to 49: ", find_shortest_path(graph, 0, 49))
print("49 to 31: ", find_shortest_path(graph, 49, 31))
print("31 to 49: ", find_shortest_path(graph, 31, 49))
print("1 to 40: ", find_shortest_path(graph, 1, 40))

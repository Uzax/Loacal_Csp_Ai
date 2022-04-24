import copy


class GraphColorCSP (object):
    def __init__(self, variables, colors, adjacency):
        self.variables = variables
        self.colors = colors
        self.adjacency = adjacency

    def diff_satisfied(self, var1, color1, var2, color2):
        if var2 not in self.variables:  # ADDED
            return False

        neig = self.adjacency[var1]
        if var2 not in neig:
            return True

        if var2 in neig and color1 != color2:
            return True

        return False

    def is_goal(self, assignment):

        for e in self.variables:  # Check for Complete
            if e not in assignment:
                return False

        for e in self.variables:
            current_color = assignment[e]
            current_neighbor = self.adjacency[e]
            for i in current_neighbor:
                neighbor_color = assignment[i]
                if current_color == neighbor_color:
                    return False

        return True

    def check_partial_assignment(self, assignment):
        for e in assignment:
            current_color = assignment[e]
            current_neighbor = self.adjacency[e]

            for i in current_neighbor:
                if i not in assignment:
                    continue
                neighbor_color = assignment[i]
                if current_color == neighbor_color:
                    return False

        return True


def ac3(graphcolorcsp, arcs_queue=None, current_domains=None, assignment=None):
    if arcs_queue is None:
        arcs_queue = set()
        for e in graphcolorcsp.variables:
            negh = graphcolorcsp.adjacency[e]
            for i in negh:
                arcs_queue.add((e, i))
    else:
        arcs_queue = set(arcs_queue)

    if current_domains is None:
        current_domains = {}

        for e in graphcolorcsp.variables:
            current_domains[e] = list(graphcolorcsp.colors)

    while arcs_queue:
        (Xi, Xj) = arcs_queue.pop()
        if revise(graphcolorcsp, Xi, Xj, current_domains):
            if not current_domains[Xi]:
                return False, current_domains

            for Xk in graphcolorcsp.adjacency[Xi]:
                if Xk == Xj:
                    continue
                if assignment is not None and Xk in assignment:
                    continue

                arcs_queue.add((Xk, Xi))

    return True, current_domains


def revise(graphcolorcsp, xi, xj, current_domains):
    revised = False

    to_be_removed = []
    for x in current_domains[xi]:
        no_value = True
        for y in current_domains[xj]:
            if graphcolorcsp.diff_satisfied(xi, x, xj, y):  # check the cons
                no_value = False
                break

        if no_value:
            to_be_removed.append(x)
            revised = True

    if revised:
        tmp = current_domains[xi]
        for i in tmp.copy():
            if i in to_be_removed:
                tmp.remove(i)

        current_domains[xi] = tmp

    return revised


def backtracking(graphcolorcsp):
    current_domains = {}

    for e in graphcolorcsp.variables:
        current_domains[e] = list(graphcolorcsp.colors)

    return backtracking_helper(graphcolorcsp, current_domains=current_domains)


def backtracking_helper(graphcolorcsp, assignment={}, current_domains=None):
    if len(assignment) == len(graphcolorcsp.variables):
        return assignment
    var, values = select_unsigned_variable(graphcolorcsp, assignment)

    for i in values:
        copy_assignment = copy.deepcopy(assignment)
        copy_assignment[var] = i
        if graphcolorcsp.check_partial_assignment(copy_assignment):
            assignment[var] = i
            inferences, reduced_domain = ac3(
                graphcolorcsp, current_domains=current_domains, assignment=assignment)
            if inferences:
                domain_copy = copy.deepcopy(current_domains)
                result = backtracking_helper(
                    graphcolorcsp, assignment, domain_copy)

                if result is not None:
                    return result
                #current_domains = reduced_domain

            del assignment[var]

    return None


def select_unsigned_variable(graphcolorcsp, assignment):
    variables = []
    for i in list(graphcolorcsp.variables):
        if i not in assignment:
            variables.append([i])

    for i in range(len(variables)):
        colors = order_domain_value(graphcolorcsp, assignment, variables[i][0])
        variables[i].append(colors)
        variables[i].append(len(colors))

    variables.sort(key=lambda x: x[2])

    return variables[0][0], variables[0][1]


def order_domain_value(graphcolorcsp, assignment, var):
    colors = list(graphcolorcsp.colors)

    neighbor = graphcolorcsp.adjacency[var]

    for i in neighbor:
        if i in assignment:
            neighbor_color = assignment[i]
            if neighbor_color in colors:
                colors.remove(neighbor_color)

    return colors

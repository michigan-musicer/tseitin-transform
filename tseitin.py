def run_tseitin(dnf, next_var_start=None, print_formatted_cnf=True):
    cnf = []
    
    n = len(dnf)
    # start next_var_idx at the next possible unique variable number
    # if this parameter is not specified, start at the number after the highest number
    if next_var_start is not None:
       next_var_idx = next_var_start
    else:
        next_var_idx = max([abs(variable) for clause in dnf for variable in clause]) + 1

    # number clauses y1, y2... yn
    clause_idxs = list(range(next_var_idx, next_var_idx + n))
    next_var_idx = max(clause_idxs) + 1

    # ...then number pairs of clauses z1, z2 ... z{n-1}
    clause_pair_idxs = range(next_var_idx, next_var_idx + n - 1)

    # convert clauses
    for (idx, clause) in zip(clause_idxs, dnf):
        # print(clause, type(clause))
        cnf += [[-idx, variable] for variable in clause]
        cnf += [[-variable for variable in clause] + [idx]]
    
    if len(dnf) > 1:
        # edge case on clause pair conversion
        first_edge = clause_idxs[0]
        second_edge = clause_idxs[1]
        pair_idx_edge = clause_pair_idxs[0] 
        cnf += [[-first_edge, pair_idx_edge], [-second_edge, pair_idx_edge], [-pair_idx_edge, first_edge, second_edge]]
        # convert pairs of clauses
        for (pair_idx, first, second) in zip(clause_pair_idxs[1:], clause_pair_idxs[:-1], clause_idxs[2:]):
            cnf += [[-first, pair_idx], [-second, pair_idx], [-pair_idx, first, second]]
        # including this means "i want this expression to be sat", which isn't necessarily the goal
        # cnf += [[max(clause_pair_idxs)]]

    if print_formatted_cnf:
        for clause in cnf:
            to_str = ''
            for var in clause:
                to_str += str(var) + ' '
            to_str += '0'
            print(to_str)

    return cnf
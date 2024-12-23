import re

def solve_linear_system_integer_solutions(a1, b1, c1, a2, b2, c2):
    '''
    Solve a 2D system of linear equations, but only return valid 
    integer solutions to the system. If no solutions exist, infinite
    solutions exist, or a floating point number solution exists 
    then return None
    '''
    # Compute the determinant
    det = a1*b2 - a2*b1
    if det == 0:
        # no solution or infinite solutions
        return None

    num_a = c1*b2 - c2*b1
    num_b = a1*c2 - a2*c1

    # Check divisibility
    if num_a % det == 0 and num_b % det == 0:
        a = num_a // det
        b = num_b // det
        return a, b
    else:
        a = num_a / det
        b = num_b / det
        return None
    
def find_token_cost(input_file, prize_pos_offset = 0):
    result = 0
    with open(input_file) as f:
        while True:
            a, b, prize = f.readline(), f.readline(), f.readline()
            if not a or not b or not prize:
                break
            a1, a2  = re.findall('X\+(\d+), Y\+(\d+)', a)[0]
            b1, b2 = re.findall('X\+(\d+), Y\+(\d+)', b)[0]
            c1, c2 = re.findall('X=(\d+), Y=(\d+)', prize)[0]
            a1, a2, b1, b2, c1, c2 = map(int, (a1, a2, b1, b2, c1, c2))
            c1, c2 = c1 + prize_pos_offset, c2 + prize_pos_offset
            solution = solve_linear_system_integer_solutions(a1, b1, c1, a2, b2, c2)
            if solution:
                result += solution[0] * 3
                result += solution[1] * 1
            f.readline()
    return result
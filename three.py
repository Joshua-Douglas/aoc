import re

MUL_COMMAND_PATTERN = re.compile(r"(?i)mul\((\d{1,3}),(\d{1,3})\)")

def extract_mul_command_input(input_string):
    matches = MUL_COMMAND_PATTERN.findall(input_string)
    return [(int(num1), int(num2)) for num1, num2 in matches]

def decorrupt_memory(memory_filepath):
    memory_str = ''
    with open(memory_filepath) as f:
        memory_str = f.read()

    return sum((a*b for (a,b) in extract_mul_command_input(memory_str)))
    
if __name__ == "__main__":
    from dataclasses import dataclass
    from typing import List, Tuple
    @dataclass
    class Tst:
        input: str
        output: List[Tuple[int, int]]
        sum: int

    TEST_CASES = (
        Tst('asdf', list(), 0),
        Tst('mul()', list(), 0),
        Tst('mul(1,1)', [(1, 1)], 1),
        Tst('mul(2,1)', [(2, 1)], 2),
        Tst('mul(1,2)', [(1, 2)], 2),
        Tst('mul(1, 2)', list(), 0),
        Tst('Mul(1,1)', [(1,1)], 1),
        Tst('muL(1,1)', [(1,1)], 1),
        Tst('mul(1,2 )', list(), 0),
        Tst(' mul(1,1)', [(1,1)], 1),
        Tst('mul(1,1) mul(2,3) MUL(4,5)', [(1,1), (2,3), (4,5)], 27),
        Tst('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))', [(2, 4), (5, 5), (11, 8), (8, 5)], 161)
    ) 
    for case in TEST_CASES:
        result = extract_mul_command_input(case.input)
        result_sum = sum((a*b for (a,b) in result))
        if result != case.output:
            print(f"Test case failed for {case.input}: {case.output}. Actual output: {result}")
        if result_sum != case.sum:
            print(f"Test case failed for {case.input}: Expected sum {case.sum}, Actual sum: {result_sum}")

    # 165225049
    print(decorrupt_memory('three.txt'))
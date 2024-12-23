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

def decorrupt_do_memory(memory_filepath):
    '''
    Conditionally enable and disable the mul() commands using the
    don't() and do() commands. The memory_str begins enabled and 
    each encountered don't() command will disable until the next
    do() command.

    Return the sum of all found mul() commands.

    e.g. xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    xmul(2,4)&mul[3,7]!^ -> Enabled
    _mul(5,5)+mul(32,64](mul(11,8)un -> Disabled
    ?mul(8,5)) -> Enabled
    '''
    memory_str = ''
    with open(memory_filepath) as f:
        memory_str = f.read()

    result = 0
    for idx, potential_do in enumerate(memory_str.split("don't()")):
        # handle case where multiple do()s are between a single don't()
        potential_cmds = potential_do.split("do()")
        # First command starts enabled. Remaining will start disabled
        if idx != 0: del potential_cmds[0]
        for do_cmd in potential_cmds:
            result += sum((a*b for (a,b) in extract_mul_command_input(do_cmd)))
    return result          

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
    # 108830766
    print(decorrupt_do_memory('three.txt'))
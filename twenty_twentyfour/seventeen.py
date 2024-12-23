from typing import Iterable
import random

class Program:
    def __init__(self, A: int, B: int, C: int, inst: Iterable[int]):
        self.A = A
        self.B = B
        self.C = C
        self.ptr = 0
        self.inst = inst
        self.out = ''

    def cmb_op(self, value):
        match value:
            case 0 | 1 | 2 | 3: return value
            case 4: return self.A
            case 5: return self.B
            case 6: return self.C
            case _: raise ValueError(f"unknown combo operand {value}")
    
    def cycle(self, opcode: int, operand: int):
        match opcode:
            case 0: self.A //= 2**self.cmb_op(operand)
            case 1: self.B ^= operand
            case 2: self.B = self.cmb_op(operand) % 8
            case 3: self.ptr = (operand - 2) if self.A != 0 else self.ptr
            case 4: self.B ^= self.C
            case 5: self.out += f',{self.cmb_op(operand) % 8}'
            case 6: self.B = self.A // 2**self.cmb_op(operand)
            case 7: self.C = self.A // 2**self.cmb_op(operand)
            case _: raise ValueError(f"unknown opcode {opcode}")
        self.ptr += 2

    def run(self):
        while 0 <= self.ptr < len(self.inst) - 1:
            opcode = self.inst[self.ptr]
            operand = self.inst[self.ptr + 1]
            self.cycle(opcode, operand)
        return self.out[1:]
    
    def reset_program(self):
        self.ptr = 0
        self.A, self.B, self.C = 0, 0, 0
        self.out = ''

    def computescore(self):
        '''Output similarity score, when compared against current instruction set'''
        output = [int(o) for o in self.out[1:].split(',')]
        if len(output) != len(self.inst):
            return 100
        
        matches = 0
        for a, b in zip(output, self.inst):
            if a == b:
                matches += 1
        return 16 - matches
    
    def solve_part_two(self):
        """
        Solution heavily inspired from this reddit thread (otherwise I never would
        have thought of it): 
        https://www.reddit.com/r/adventofcode/comments/1hg6orl/2024_day_17_part_2_did_anyone_else_solve_part_2/
        
        We use a genetic-algorithm-like approach to find a value of A such that
        the program outputs its own instructions (Part Two of the puzzle).

        This method:
        1. Initializes a population of random A values in the range [2^45, 2^48-1].
        2. Evaluates each candidate's 'score' based on how closely the program's
            output matches its own instructions (see computescore()).
        3. Repeatedly refines the population by:
            - Mutation: flipping one random bit (2% chance).
            - Crossover: splicing two binary strings of A values at a random index.
        4. Sorts candidates by score, keeps best solutions, and replaces the rest.
        5. Terminates after multiple generations with no improvement, returning
            the best A found.

        Why these crossover and mutation strategies?
        - Mutation flips exactly one random bit in A, offering small, localized
            changes that can fix or tweak an otherwise promising candidate.
        - Crossover creates a 'child' by slicing two parent bit patterns at
            a random point; this allows larger, more diverse combinations of
            features from the parent solutions.
        - Together, these genetic operators balance exploration (mutation)
            with exploitation (crossover of already partially correct solutions),
            guiding the search toward a candidate A that causes the program to
            replicate its own instructions.
        """
        lo = 2**45
        hi = 2**48-1

        poolsize = 10000
        pool = []
        for _ in range(poolsize):
            a = random.randint(lo, hi)
            self.reset_program()
            self.A = random.randint(lo, hi)
            out = self.run()
            score = self.computescore()
            pool.append([score, a, out])
        pool.sort()
        
        def crossover(a, b):
            ba = bin(a)
            bb = bin(b)
            if len(ba) != len(bb):
                return a
            else:
                s = random.randint(0, len(ba)-1)
                r = ba[:s] + bb[s:]
                if len(r) != len(ba):
                    raise IndexError
                return int(r, 2)
        
        acheck = set()
        for s, a, o in pool:
            acheck.add(a)

        best_result = None
        best_result_cntr = 0
        while best_result_cntr < 8:    
            for i in range(poolsize//2, poolsize):
                if random.random() < 0.02:
                    s, a, o = pool[i]                
                    self.reset_program()
                    self.A = a ^ (1 << random.randint(0, 47))
                    o = self.run()
                    s = self.computescore()
                    pool[i] = [s, a, o]
                    continue

                while a in acheck:
                    p0 = random.randint(0, poolsize//2-1)
                    p1 = random.randint(0, poolsize//2-1)
                    a = crossover(pool[p0][1], pool[p1][1])
                acheck.add(a)
                self.reset_program()
                self.A = a
                o = self.run()
                s = self.computescore()
                pool[i] = [s, a, o]
                
            pool.sort()

            cur_best_score = pool[0][1]
            if best_result == cur_best_score:
                best_result_cntr += 1
            else:
                best_result_cntr = 0
            best_result = cur_best_score
        return best_result
    
#!/usr/bin/env python

# author: Danillo Souza <danillo012@gmail.com>
# 2013-01-18

import string
from random import randint, choice
from optparse import OptionParser

(GEN_SIZE, COMMUNITY_SIZE, ITER_LIMIT) = (0,0,0)
SPECIAL_CHARS = ' .!?:'
CHARS_AVAILABLE = list(''.join([string.ascii_lowercase, string.ascii_uppercase, SPECIAL_CHARS]))


def initialize():
        return ''.join([choice(CHARS_AVAILABLE) for i in range(GEN_SIZE)])

def fitness(target, source):
        """
        Calculates fitness based on Levenshtein Distance. (perfect = 0)
        """
        if len(target) < len(source): 
                return lev_distance(source, target)
        if not len(source): 
                return len(target)

        previous_row = range(len(source) + 1)

        for x, c1 in enumerate(target):
                current_row = [x + 1]

                for y, c2 in enumerate(source):
                        current_row.append(min(previous_row[y + 1] + 1, current_row[y] + 1, previous_row[y] + (c1 != c2)))

                previous_row = current_row

        return previous_row[-1]

def mutagen(gen):
        qtd = randint(1,4)

        for i in range(qtd):
                tmp = list(gen)
                tmp[randint(0,GEN_SIZE-1)] = choice(CHARS_AVAILABLE)
                gen = ''.join(tmp)

        return gen

def circle_of_life(search="foo"):
        community = {initialize():None for i in range(COMMUNITY_SIZE)}
        winner = None
        i = 0 
        while not winner:
                i += 1
                # calculate fitness of each gen (perfect = 0)
                for gen in community.keys():                        
                        if community[gen] != 0:
                                community[gen] = fitness(gen, search)
                                community[gen]

                                print ("Gen[%d] %s : %d" % (i, gen, community[gen]))

                                mutant = mutagen(gen)
                                mutant_fitness = fitness(mutant, search)
                                
                                if community[gen] > mutant_fitness:
                                        del community[gen]
                                        community[mutant] = mutant_fitness
                        
                        else:
                                winner = gen

        print ("\nGen["+str(i)+"]Winner: %s" % winner)


if __name__ == '__main__':
        
        parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")

        parser.add_option('-s', '--string', dest='string', help="The result you're hoping to find.", default='foo')
        parser.add_option('-c', '--community-size', dest='community_size', help="The size of the evolving community.", default=10)

        (options, args) = parser.parse_args()

        GEN_SIZE = len(options.string)
        COMMUNITY_SIZE = int(options.community_size)

        circle_of_life(options.string)
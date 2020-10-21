import retro
import numpy as numpy  # For image-matrix/vector operations
import cv2  # For image reduction
import neat
import pickle

import argparse

#env = retro.make(game='Airstriker-Genesis', state='Level1-1', record=True)
oned_image = []

parser = argparse.ArgumentParser()
parser.add_argument('--game', default='Airstriker-Genesis', help='the name or path for the game to run')
parser.add_argument('--state', help='the initial state file to load, minus the extension')
parser.add_argument('--scenario', '-s', default='scenario', help='the scenario file to load, minus the extension')
parser.add_argument('--record', '-r', action='store_true', help='record bk2 movies')
parser.add_argument('--verbose', '-v', action='count', default=1, help='increase verbosity (can be specified multiple times)')
parser.add_argument('--quiet', '-q', action='count', default=0, help='decrease verbosity (can be specified multiple times)')
parser.add_argument('--obs-type', '-o', default='image', choices=['image', 'ram'], help='the observation type, either `image` (default) or `ram`')
parser.add_argument('--players', '-p', type=int, default=1, help='number of players/agents (default: 1)')
args = parser.parse_args()

env = retro.make(args.game, args.state or retro.State.DEFAULT, scenario=args.scenario, record=args.record, players=args.players)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:

        ob = env.reset  # First image
        random_action = env.action_space.sample()
        inx, iny, inc = env.observation_space.shape  # inc = color
        # image reduction for faster processing
        inx = int(inx / 8)
        iny = int(iny / 8)
        # 20 Networks
        net = neat.nn.RecurrentNetwork.create(genome, config)
        current_max_fitness = 0
        fitness_current = 0
        frame = 0
        counter = 0

        done = False

        while not done:
            env.render()  # Optional
            frame += 1

            ob = cv2.resize(ob, (inx, iny))  # Ob is the current frame
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)  # Colors are not important for learning
            ob = np.reshape(ob, (inx, iny))

            oned_image = np.ndarray.flatten(ob)
            neuralnet_output = net.activate(oned_image)  # Give an output for current frame from neural network
            ob, rew, done, info = env.step(neuralnet_output)  # Try given output from network in the game

            fitness_current += rew
            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1
                # count the frames until it successful

            # Train mario for max 250 frames
            if done or counter == 250:
                done = True
                print(genome_id, fitness_current)

            genome.fitness = fitness_current


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')
p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
# Save the process after each 10 frames
p.add_reporter(neat.Checkpointer(10))

winner = p.run(eval_genomes)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
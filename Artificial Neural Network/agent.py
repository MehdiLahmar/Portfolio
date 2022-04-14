import torch
import random
import numpy as np
from Game import SnakeGameAI, Direction, Point
from collections import deque
from model import Linear_QNet, QTrainer
from graph import Plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.nb_games = 0
        self.randomness = 0
        self.discount_rate = 0
        self.memory = deque(maxlen= MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr = LEARNING_RATE, gamma = self.discount_rate)

    def Get_State(self, game):
        head = game.snake[0]
        point_up = Point(head.x, head.y - 20)
        point_right = Point(head.x - 20, head.y)
        point_down = Point(head.x, head.y + 20)
        point_left = Point(head.x + 20, head.y)

        dir_up = game.direction == Direction.UP
        dir_right = game.direction == Direction.RIGHT
        dir_down = game.direction == Direction.DOWN
        dir_left = game.direction == Direction.LEFT

        state = [
            #Danger devant
            (dir_up and game.Collision(point_up)) or
            (dir_right and game.Collision(point_right)) or
            (dir_down and game.Collision(point_down)) or
            (dir_left and game.Collision(point_left)),

            #Danger à gauche
            (dir_up and game.Collision(point_left)) or
            (dir_right and game.Collision(point_up)) or
            (dir_down and game.Collision(point_right)) or
            (dir_left and game.Collision(point_down)),

            #Danger à droite
            (dir_up and game.Collision(point_right)) or
            (dir_right and game.Collision(point_down)) or
            (dir_down and game.Collision(point_left)) or
            (dir_left and game.Collision(point_up)),

            #Nourriture
            game.nourriture.x > head.x,
            game.nourriture.x < head.x,
            game.nourriture.y > head.y,
            game.nourriture.y < head.y,

            #Direction du serpent
            game.direction == Direction.UP,
            game.direction == Direction.RIGHT,
            game.direction == Direction.LEFT,
            game.direction == Direction.DOWN
        ]

        return(np.array(state, dtype=int))


    def Remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def Train_Long_Memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def Train_Short_Memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def Get_Action(self, state):
        self.randomness = 80 - self.nb_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.randomness:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return(final_move)

def Train():
    plot_score = []
    plot_mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        state_old = agent.Get_State(game)
        final_move = agent.Get_Action(state_old)
        reward, done, score = game.step(final_move)
        state_new = agent.Get_State(game)
        agent.Train_Short_Memory(state_old, final_move, reward, state_new, done)

        agent.Remember(state_old, final_move, reward, state_new, done)

        if done:
            #train long memory
            game.reset()
            agent.nb_games = agent.nb_games + 1
            agent.Train_Long_Memory()

            if score > record:
                record = score
                agent.model.Save()

            print("Game: ", agent.nb_games, "Score: ", score, "Record: ", record)

            plot_score.append(score)
            total_score += score
            mean_score = total_score/agent.nb_games
            plot_mean_score.append(mean_score)
            Plot(plot_score, plot_mean_score)

if __name__ == '__main__':
    Train()
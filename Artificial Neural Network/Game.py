# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random
from collections import namedtuple
from enum import Enum
import numpy as np

pygame.init()
Point = namedtuple('Point', 'x, y')
BLOC = 20
BLUE = (255, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
SPEED = 200

# reset
# reward
# play(action)
# game iteration
# collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h

        #Affichage
        self.ecran = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        # init game state
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOC, self.h),
                      Point(self.head.x - (BLOC * 2), self.h)
                      ]

        self.direction = Direction.RIGHT
        self.score = 0
        self.nourriture = None
        self.Ajouter_Nourriture()
        self.game_over = False
        self.frame_iteration = 0

    def Ajouter_Nourriture(self):
        x = random.randint(0, (self.w - BLOC) // BLOC) * BLOC
        y = random.randint(1, (self.h - BLOC) // BLOC) * BLOC
        self.nourriture = Point(x, y)

        #Vérifier si la nourriture est sur le serpent
        if self.nourriture in self.snake:
            self.Ajouter_Nourriture()

    def step(self, action):
        self.frame_iteration = self.frame_iteration + 1

        #Récupérer l'input de l'utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        #Faire bouger le serpent
        self.move(action)

        #Voir si une condition de game over est vérifiée
        reward = 0
        if self.head in self.snake[1:]:
            self.game_over = True
        elif self.head.x > (int(self.w // BLOC) * BLOC) - BLOC:
            self.game_over = True
        elif self.head.x < 0:
            self.game_over = True
        elif self.head.y > (int(self.h // BLOC) * BLOC) - BLOC:
            self.game_over = True
        elif self.head.y < BLOC:
            self.game_over = True

        if self.game_over == True or self.frame_iteration > 100 * len(self.snake):
            reward = -10
            #pygame.quit()
            return reward, self.game_over, self.score

        #Mettre à jour le score
        if self.head == self.nourriture:
            reward = 10
            self.score = self.score + 1
            self.Ajouter_Nourriture()
            self.snake.append(Point(self.snake[-1].x, self.snake[-1].y))

        self.Update_ecran()
        pygame.display.flip()
        self.clock.tick(SPEED)
        return(reward, self.game_over, self.score)

    def Collision(self, point):
        if point in self.snake[1:]:
            return(True)
        elif point.x > (int(self.w // BLOC) * BLOC) - BLOC:
            return(True)
        elif point.x < 0:
            return(True)
        elif point.y > (int(self.h // BLOC) * BLOC) - BLOC:
            return(True)
        elif point.y < BLOC:
            return(True)
        else:
            return (False)

    def move(self, action):

        dir = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = dir.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = dir[index]
        elif np.array_equal(action, [0, 1, 0]):
            new_index = (index + 1) % 4
            new_dir = dir[new_index]
        elif np.array_equal(action, [0, 0, 1]):
            new_index = (index - 1) % 4
            new_dir = dir[new_index]

        self.direction = new_dir

        if self.direction == Direction.RIGHT:
            self.snake.insert(0, Point(self.snake[0].x + BLOC, self.snake[0].y))
        elif self.direction == Direction.LEFT:
            self.snake.insert(0, Point(self.snake[0].x - BLOC, self.snake[0].y))
        elif self.direction == Direction.UP:
            self.snake.insert(0, Point(self.snake[0].x, self.snake[0].y - BLOC))
        elif self.direction == Direction.DOWN:
            self.snake.insert(0, Point(self.snake[0].x, self.snake[0].y + BLOC))

        self.head = self.snake[0]
        self.snake.pop()

    def Update_ecran(self):
        self.ecran.fill((0, 0, 0))

        for bloc in self.snake:
            pygame.draw.rect(self.ecran, BLUE, pygame.Rect(bloc.x, bloc.y, BLOC, BLOC))

        pygame.draw.rect(self.ecran, RED, pygame.Rect(self.nourriture.x, self.nourriture.y, BLOC, BLOC))

        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Score: ' + str(self.score), True, WHITE)
        self.ecran.blit(text, (0, 0))
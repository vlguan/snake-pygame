import gymnasium as gym
from gymnasium import spaces

import numpy as np
import pygame
import sys
import time
import random


class SnakeEnv(gym.Env):
    metadata = {"render_modes": "human"}

    def __init__(self, render_mode=None):
        super(SnakeEnv, self).__init__()
        max_snake_length = 200
        self.difficulty = 75
        self.frame_size_x = 720
        self.frame_size_y = 480

        pygame.init()
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        pygame.display.set_caption('Snake Game')

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.green = pygame.Color(0, 255, 0)

        self.fps_controller = pygame.time.Clock()

        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.reward = 0
        self.food_ate = 0
        # Define action and observation space
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Tuple((
            spaces.Box(low=0, high=self.frame_size_x, shape=(2,), dtype=int),  # Food position
            spaces.Box(low=0, high=self.frame_size_x, shape=(2,), dtype=int),  # Snake position
            spaces.Box(low=0, high=self.frame_size_x, shape=(max_snake_length, 2), dtype=int),  # Snake body
            spaces.Box(low=-self.frame_size_x, high=self.frame_size_x, shape=(2,), dtype=int) #relative food pos
        ))
    def step(self, action):
        if action == 0:
            self.change_to = 'UP'
        if action == 1:
            self.change_to = 'DOWN'
        if action == 2:
            self.change_to = 'LEFT'
        if action == 3:
            self.change_to = 'RIGHT'

        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_ate +=1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        done = False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10 or self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            self.score -= 10
            done = True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.score -= 10
                done = True
        relative_food_pos = [self.food_pos[0] - self.snake_pos[0], self.food_pos[1] - self.snake_pos[1]]
        distance = np.linalg.norm(np.array(self.snake_pos) - np.array(self.food_pos), ord=2)
        self.reward = self.score - (distance/100)*5

        return (self.food_pos, self.snake_pos, self.snake_body, relative_food_pos), self.reward, done, {'score': self.score, 'distance': distance, 'food_ate': self.food_ate}

    def reset(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.food_ate = 0
        return (self.food_pos, self.snake_pos, self.snake_body)

    def render(self, mode='human'):
        if mode == 'human':
            self.game_window.fill(self.black)
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
            pygame.display.flip()
            self.fps_controller.tick(self.difficulty)
            pygame.event.pump()
    def close(self):
        pygame.display.quit()
        pygame.quit()

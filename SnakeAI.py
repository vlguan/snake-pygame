import gymnasium as gym
from mymodule.SnakeEnv import SnakeEnv
from gymnasium.envs.registration import register
import torch
import csv

# Open the CSV file in write mode
csv_file = open('log_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write the header row
header = ['Episode', 'Score', 'Distance']
csv_writer.writerow(header)

save_path = 'model.pth'
register(
     id="SnakeGame-v0",
     entry_point="mymodule:SnakeEnv",
     max_episode_steps=1000,
)
print('before loop')
env = gym.make('SnakeGame-v0')
observation = env.reset()
life = 0
print('before loop')
try:
    while True:
        
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        env.render()
        if done:
            life += 1
            observation = env.reset()
            data_row = [life, reward, info]
            csv_writer.writerow(data_row)
except KeyboardInterrupt:
    env.close()
    csv_file.close()
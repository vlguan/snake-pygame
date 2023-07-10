from gymnasium.envs.registration import register
from .SnakeEnv import SnakeEnv
register(
     id="SnakeGame-v0",
     entry_point="mymodule:SnakeEnv",
     max_episode_steps=1000,
)
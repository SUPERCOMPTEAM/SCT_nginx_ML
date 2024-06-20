import random
from typing import Optional, Union, List, Tuple

import gym
import numpy as np
from gym.core import RenderFrame, ActType, ObsType
from gym.spaces import Discrete, Box, Sequence
from gym import Env

from models import Upstream


class NginxEnv(Env):
    upstream: Upstream

    def _init_upstream(self):
        self.upstream = Upstream(self.server_count, self.request_limit, self.server_count)

    def __init__(self):
        self.server_count = 5
        self.request_limit = 100
        self._init_upstream()

        self.action_space = Box(low=0, high=1, shape=(self.server_count,))
        self.observation_space = Box(-100, 100, shape=(self.server_count*3,))
        self.state = self.upstream.step(self.action_space.sample()).state
        self._max_episode_steps = 20

    def step(self, action):
        self._max_episode_steps -= 1

        callback = self.upstream.step(action)

        reward = callback.reward

        if self._max_episode_steps == 0:
            done = True
        else:
            done = False

        self.state = callback.state

        return self.state, reward, done, {}

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        self._init_upstream()
        self.state = self.upstream.step(self.action_space.sample()).state
        self._max_episode_steps = 20

        return self.state

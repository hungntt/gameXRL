import gym
from render_browser import render_browser

env = gym.make('Pong-v0')

@render_browser
def test_policy(policy):
    # Your function/code here.
    # env = gym.make('Breakout-v0')
    obs = env.reset()

    while True:
        yield env.render(mode='rgb_array')
        for _ in range(1000):
            # load image on browser
            image = env.render()
            # ... run policy ...
            action = policy
            # auto-pause -- pygame
            env.step(action)
            # obs, rew, _, _ = env.step(action)
test_policy(env.action_space.sample())

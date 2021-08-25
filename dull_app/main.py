import gym
from render import render_browser


@render_browser
def random_policy():
    env = gym.make('Pong-v0')
    env.reset()

    for _ in range(10):
        yield env.render(mode='rgb_array')
        action = env.action_space.sample()
        env.step(action)


if __name__ == '__main__':
    random_policy()

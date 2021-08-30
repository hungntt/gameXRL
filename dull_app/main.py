import gym
from render import render_browser

game_name = 'Pong-v0'


@render_browser
def random_policy():
    env = gym.make(game_name)
    env.reset()

    for _ in range(10):
        yield env.render(mode='rgb_array')
        # load model here
        # policy model
        action = env.action_space.sample()
        # get next obs
        env.step(action)


if __name__ == '__main__':
    random_policy()

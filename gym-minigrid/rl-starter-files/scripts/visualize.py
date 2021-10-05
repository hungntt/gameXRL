import argparse
import numpy
import base64
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import utils
from utils import device

# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True,
                    help="name of the environment to be run (REQUIRED)")
parser.add_argument("--model", required=True,
                    help="name of the trained model (REQUIRED)")
parser.add_argument("--seed", type=int, default=0,
                    help="random seed (default: 0)")
parser.add_argument("--shift", type=int, default=0,
                    help="number of times the environment is reset at the beginning (default: 0)")
parser.add_argument("--argmax", action="store_true", default=False,
                    help="select the action with highest probability (default: False)")
parser.add_argument("--pause", type=float, default=0.1,
                    help="pause duration between two consequent actions of the agent (default: 0.1)")
parser.add_argument("--gif", type=str, default=None,
                    help="store output as gif with the given filename")
parser.add_argument("--episodes", type=int, default=1000000,
                    help="number of episodes to visualize")
parser.add_argument("--memory", action="store_true", default=False,
                    help="add a LSTM to the model")
parser.add_argument("--text", action="store_true", default=False,
                    help="add a GRU to the model")

args = parser.parse_args()

# Set seed for all randomness sources

utils.seed(args.seed)

# Set device

print(f"Device: {device}\n")

# Load environment

env = utils.make_env(args.env, args.seed)
for _ in range(args.shift):
    env.reset()
print("Environment loaded\n")

# Load agent

model_dir = utils.get_model_dir(args.model)
agent = utils.Agent(env.observation_space, env.action_space, model_dir,
                    argmax=args.argmax, use_memory=args.memory, use_text=args.text)
print("Agent loaded\n")

# Run the agent

if args.gif:
    from array2gif import write_gif

    frames = []

# Create a window to view the environment
env.render('human')


def encode_img_to_base64(arr_image):
    image = arr_image[:, :, ::-1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

    plt.close(fig)
    return pngImageB64String


for episode in range(args.episodes):
    obs = env.reset()
    i = 1
    while True:
        env.render('human')
        array_img = numpy.moveaxis(env.render("rgb_array"), 2, 0)
        if args.gif:
            frames.append(array_img)

        action = agent.get_action(obs)
        obs, reward, done, _ = env.step(action)
        # print ( encode_img_to_base64(env.render("rgb_array")) )
        agent.analyze_feedback(reward, done)

        # save to db
        state = dict()
        # print (action)
        state['gym_id'] = 1
        state['game_id'] = 6
        state['state'] = ""
        state['action'] = action.item()
        state['reward'] = reward
        ndone = 0
        if done:
            ndone = 1
        state['done'] = ndone
        state['image'] = encode_img_to_base64(env.render("rgb_array"))
        import sys

        sys.path.append('/home/silver/gameXRL-master')
        from db.api import API

        API().create_observation(state)

        if done or env.window.closed:
            break

    if env.window.closed:
        break

if args.gif:
    print("Saving gif... ", end="")
    write_gif(numpy.array(frames), args.gif + ".gif", fps=1 / args.pause)
    print("Done.")

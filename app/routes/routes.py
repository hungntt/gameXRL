import base64
import io

import cv2
import gym
from flask import render_template, request, flash, redirect, Response
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from app import app
from app.routes.forms import GameForm, CommentForm
from db.api import create_game, create_comment


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render index page and Add new comment
    """
    image = plot_png()
    form = CommentForm(request.form)
    if request.method == 'POST':
        # Save the comment to database
        create_comment(form.data)
        flash('New comment created successfully.')
        return redirect('/')

    return render_template('index.html', form=form, image=image)


# @app.route('/games', methods=['POST'])
# def new_game():
#     """
#     Add new game
#     """
#     form = GameForm(request.form)
#
#     if request.method == 'POST' and form.validate():
#         # Save the game to database
#         create_game(form)
#         flash('New game created successfully.')
#         return redirect('/')
#
#     return render_template('new_game.html', form=form)


def plot_png():
    env, image, action, observation, reward, done, info = env_action()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

    return pngImageB64String


def env_action():
    game_name = 'Pong-v0'
    env = gym.make(game_name)
    env.reset()
    # load model here
    # policy model
    action = env.action_space.sample()
    # get next obs
    observation, reward, done, info = env.step(action)
    image = env.render(mode='rgb_array')
    return env, image, action, observation, reward, done, info


if __name__ == '__main__':
    app.run()

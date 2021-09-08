import cv2
import gym
from flask import render_template, request, flash, redirect, Response
from app import app
from app.routes.forms import GameForm, CommentForm
from db.api import create_game, create_comment


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render index page and Add new comment
    """

    form = CommentForm(request.form)
    if request.method == 'POST':
        # Save the comment to database
        create_comment(form.data)
        flash('New comment created successfully.')
        return redirect('/')

    return render_template('index.html', form=form)


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

def frame_gen(env_func, *args, **kwargs):
    get_frame = env_func(*args, **kwargs)
    while True:
        frame = next(get_frame, None)
        if frame is None:
            break
        _, frame = cv2.imencode('.png', frame)
        frame = frame.tobytes()
        yield b'--frame\r\n' + b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n'


def render_browser(env_func):
    def wrapper(*args, **kwargs):
        @app.route('/render_feed')
        def render_feed():
            return Response(frame_gen(env_func, *args, **kwargs), mimetype='multipart/x-mixed-replace; boundary=frame')

        print("Starting rendering, check `server_ip:5000`.")
        app.run(port='5000', debug=False)

    return wrapper


def init_env():
    game_name = 'Pong-v0'
    env = gym.make(game_name)
    env.reset()
    return env


@render_browser
def random_policy():
    env = init_env()

    for _ in range(10):
        yield env.render(mode='rgb_array')
        # load model here
        # policy model
        action = env.action_space.sample()
        # get next obs
        env.step(action)


if __name__ == '__main__':
    random_policy()

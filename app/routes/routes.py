import base64
import io
import re
from flask import render_template, request, flash, redirect

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from app import app
from app.routes.forms import CommentForm
from db.api import API

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', )
def index():
    """
    Render index page
    """
    api = API()
    game_ids = api.get_all_games_id_of_a_gym(gym_id=1)
    return render_template('index.html', game_ids=game_ids)


@app.route('/game/<int:game_id>')
def show_game(game_id):
    api = API()
    observations = api.select_observations_from_a_game(game_id)
    api.close_connection()
    return render_template('show_game.html', game_id=game_id, observations=observations)


@app.route('/game/<int:game_id>/<int:fobs_id>/<int:tobs_id>')
def show_games_from_to_obs_id(game_id, fobs_id, tobs_id):
    api = API()
    observations = api.select_observations_from_a_game_from_id_to_id(game_id, fobs_id, tobs_id)
    api.close_connection()
    return render_template('show_game.html', game_id=game_id, observations=observations)


@app.route('/obs/<int:obs_id>')
def show_an_observation_from_an_obs_id(obs_id):
    api = API()
    observation = api.select_an_observation_from_an_obs_id(obs_id)
    api.close_connection()
    return render_template('show_game.html', observations=observation)


@app.route('/comment/<int:obs_id>', methods=['GET', 'POST'])
def comment_to_an_obs_id(obs_id):
    api = API()
    observation = api.select_an_observation_from_an_obs_id(obs_id)
    form = CommentForm(request.form)
    if request.method == 'POST':
        api.comment_to_an_obs_id(obs_id, form.data.get('comment'))
        flash('New comment created/updated successfully.')
        api.close_connection()
        return redirect(f'/obs/{obs_id}')
    return render_template('comment.html', form=form, observations=observation)


def plot_png(image):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

    return pngImageB64String


if __name__ == '__main__':
    app.run()

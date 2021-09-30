import base64
import io

from flask import render_template, request, flash, redirect
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from app import app
from app.routes.forms import CommentForm, CommentBatchForm
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


@app.route('/obs/<int:fobs_id>/<int:tobs_id>')
def show_from_to_obs_id(fobs_id, tobs_id):
    api = API()
    observations = api.select_observations_from_id_to_id(fobs_id, tobs_id)
    api.close_connection()
    return render_template('show_game.html', observations=observations)


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
        try:
            api.comment_to_an_obs_id(obs_id, form.data.get('comment'))
            flash('New comment created/updated successfully.')
        except Exception as e:
            flash(e)
        api.close_connection()
        return redirect(f'/obs/{obs_id}')
    return render_template('comment.html', form=form, observations=observation)


@app.route('/comment_batch', methods=['GET', 'POST'])
def comment_many_obs():
    api = API()
    form = CommentBatchForm(request.form)
    if request.method == 'POST':
        try:
            start_obs_id = form.data.get('start_obs_id')
            end_obs_id = form.data.get('end_obs_id')
            if start_obs_id >= end_obs_id:
                flash(u'Start obs id must be smaller than End obs id', 'error')
                return redirect(f'/comment_batch')
            api.comment_to_many_obs_id(start_obs_id, end_obs_id, form.data.get('comment'))
            flash('New comment batches created/updated successfully.')
            return redirect(f'/obs/{start_obs_id}/{end_obs_id}')
        except Exception as e:
            flash(e, 'error')
        api.close_connection()
    return render_template('comment_batch.html', form=form)


@app.route('/statistics')
def show_statistics():
    api = API()
    commented_obs = list()
    all_obs = list()
    commented_obs_percents = list()

    game_ids = api.get_all_games_id_of_a_gym(gym_id=1)

    for game_id in game_ids:
        game_id = game_id[0]
        commented_obs.append(api.get_lens_commented_observations(game_id=game_id))
        all_obs.append(api.get_lens_observations(game_id=game_id))
        commented_obs_percents.append(int(commented_obs[len(commented_obs) - 1] / all_obs[len(all_obs) - 1] * 100))
    range_obs = len(commented_obs_percents)
    return render_template('statistics.html',
                           game_ids=game_ids,
                           range_obs=range_obs,
                           commented_obs=commented_obs,
                           all_obs=all_obs,
                           commented_obs_percents=commented_obs_percents)


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
    app.run(host='0.0.0.0', port=2402)

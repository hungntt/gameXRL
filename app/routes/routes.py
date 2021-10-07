from flask import render_template, request, flash, redirect, url_for

from app import app
from app.routes.forms import CommentForm, CommentBatchForm
from db.api import API
from utils import main_parser

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', )
def index():
    """
    Render index page
    """
    pong_game_ids = pong_api.get_all_games_id_of_a_gym(gym_id=1)
    minigrid_game_ids = minigrid_api.get_all_games_id_of_a_gym(gym_id=1)

    return render_template('index.html', pong_game_ids=pong_game_ids, minigrid_game_ids=minigrid_game_ids)


@app.route('/<string:gym_code>/game/<int:game_id>')
def show_game(gym_code, game_id):
    observations = None
    if gym_code == 'pong':
        observations = pong_api.select_observations_from_a_game(game_id)
    elif gym_code == 'minigrid':
        observations = minigrid_api.select_observations_from_a_game(game_id)
    return render_template('show_game.html', game_id=game_id, observations=observations, gym_code=gym_code)


@app.route('/<string:gym_code>/game/<int:game_id>/<int:fobs_id>/<int:tobs_id>')
def show_games_from_to_obs_id(gym_code, game_id, fobs_id, tobs_id):
    observations = None
    if gym_code == 'pong':
        observations = pong_api.select_observations_from_a_game_from_id_to_id(game_id, fobs_id, tobs_id)
    elif gym_code == 'minigrid':
        observations = minigrid_api.select_observations_from_a_game_from_id_to_id(game_id, fobs_id, tobs_id)
    return render_template('show_game.html', gym_code=gym_code, game_id=game_id, observations=observations)


@app.route('/<string:gym_code>/obs/<int:fobs_id>/<int:tobs_id>')
def show_from_to_obs_id(gym_code, fobs_id, tobs_id):
    observations = None
    if gym_code == 'pong':
        observations = pong_api.select_observations_from_id_to_id(fobs_id, tobs_id)
    elif gym_code == 'minigrid':
        observations = minigrid_api.select_observations_from_id_to_id(fobs_id, tobs_id)
    return render_template('show_game.html', gym_code=gym_code, observations=observations)


@app.route('/<string:gym_code>/obs/<int:obs_id>')
def show_an_observation_from_an_obs_id(gym_code, obs_id):
    observation = None
    if gym_code == 'pong':
        observation = pong_api.select_an_observation_from_an_obs_id(obs_id)
    elif gym_code == 'minigrid':
        observation = minigrid_api.select_an_observation_from_an_obs_id(obs_id)

    return render_template('show_game.html', gym_code=gym_code, observations=observation)


@app.route('/<string:gym_code>/comment/<int:obs_id>', methods=['GET', 'POST'])
def comment_to_an_obs_id(gym_code, obs_id):
    observation = None
    form = CommentForm(request.form)
    if gym_code == 'pong':
        observation = pong_api.select_an_observation_from_an_obs_id(obs_id)
        if request.method == 'POST':
            pong_api.comment_to_an_obs_id(obs_id, form.data.get('comment'))
            flash('New comment created/updated successfully.')
            # pong_api.close_connection()
            return redirect(url_for('show_an_observation_from_an_obs_id', gym_code=gym_code, obs_id=obs_id))
        # pong_api.close_connection()
    elif gym_code == 'minigrid':
        observation = minigrid_api.select_an_observation_from_an_obs_id(obs_id)
        if request.method == 'POST':
            minigrid_api.comment_to_an_obs_id(obs_id, form.data.get('comment'))
            flash('New comment created/updated successfully.')
            # minigrid_api.close_connection()
            return redirect(url_for('show_an_observation_from_an_obs_id', gym_code=gym_code, obs_id=obs_id))
        # minigrid_api.close_connection()

    return render_template('comment.html', form=form, gym_code=gym_code, observations=observation)


@app.route('/<string:gym_code>/comment_batch', methods=['GET', 'POST'])
def comment_many_obs(gym_code):
    form = CommentBatchForm(request.form)
    if gym_code == 'pong':
        if request.method == 'POST':
            try:
                start_obs_id = form.data.get('start_obs_id')
                end_obs_id = form.data.get('end_obs_id')
                if int(start_obs_id) >= int(end_obs_id):
                    flash(u'Start obs id must be smaller than End obs id', 'error')
                    return render_template(comment_many_obs(gym_code=gym_code))
                pong_api.comment_to_many_obs_id(start_obs_id, end_obs_id, form.data.get('comment'))
                flash('New comment batches created/updated successfully.')
                return redirect(url_for('show_from_to_obs_id', gym_code=gym_code,
                                        fobs_id=start_obs_id, tobs_id=end_obs_id))
            except Exception as e:
                flash(e, 'error')
            # pong_api.close_connection()
    if gym_code == 'minigrid':
        if request.method == 'POST':
            try:
                start_obs_id = form.data.get('start_obs_id')
                end_obs_id = form.data.get('end_obs_id')
                if int(start_obs_id) >= int(end_obs_id):
                    flash(u'Start obs id must be smaller than End obs id', 'error')
                    return redirect(url_for('comment_many_obs', gym_code=gym_code))
                minigrid_api.comment_to_many_obs_id(start_obs_id, end_obs_id, form.data.get('comment'))
                flash('New comment batches created/updated successfully.')
                return redirect(url_for('show_from_to_obs_id', gym_code=gym_code,
                                        fobs_id=start_obs_id, tobs_id=end_obs_id))
            except Exception as e:
                flash(e, 'error')
            # minigrid_api.close_connection()
    return render_template('comment_batch.html', gym_code=gym_code, form=form)


@app.route('/statistics')
def show_statistics():
    pong_commented_obs, minigrid_commented_obs = list(), list()
    pong_all_obs, minigrid_all_obs = list(), list()
    pong_commented_obs_percents, minigrid_commented_obs_percents = list(), list()

    pong_game_ids = pong_api.get_all_games_id_of_a_gym(gym_id=1)
    minigrid_game_ids = minigrid_api.get_all_games_id_of_a_gym(gym_id=1)

    for pong_game_id in pong_game_ids:
        pong_game_id = pong_game_id[0]
        pong_commented_obs.append(pong_api.get_lens_commented_observations(game_id=pong_game_id))
        pong_all_obs.append(pong_api.get_lens_observations(game_id=pong_game_id))
        pong_commented_obs_percents.append(int(pong_commented_obs[len(pong_commented_obs) - 1]
                                               / pong_all_obs[len(pong_all_obs) - 1] * 100))
    pong_range_obs = len(pong_commented_obs_percents)

    for minigrid_game_id in minigrid_game_ids:
        minigrid_game_id = minigrid_game_id[0]
        minigrid_commented_obs.append(minigrid_api.get_lens_commented_observations(game_id=minigrid_game_id))
        minigrid_all_obs.append(minigrid_api.get_lens_observations(game_id=minigrid_game_id))
        minigrid_commented_obs_percents.append(int(minigrid_commented_obs[len(minigrid_commented_obs) - 1]
                                                   / minigrid_all_obs[len(minigrid_all_obs) - 1] * 100))
    minigrid_range_obs = len(minigrid_commented_obs_percents)

    return render_template('statistics.html',
                           pong_game_ids=pong_game_ids,
                           pong_range_obs=pong_range_obs,
                           pong_commented_obs=pong_commented_obs,
                           pong_all_obs=pong_all_obs,
                           pong_commented_obs_percents=pong_commented_obs_percents,
                           minigrid_game_ids=minigrid_game_ids,
                           minigrid_range_obs=minigrid_range_obs,
                           minigrid_commented_obs=minigrid_commented_obs,
                           minigrid_all_obs=minigrid_all_obs,
                           minigrid_commented_obs_percents=minigrid_commented_obs_percents)


if __name__ == '__main__':
    args_parser = main_parser()
    pong_api = API(cnx_type=args_parser.cnx_type, db='xrl')
    minigrid_api = API(cnx_type=args_parser.cnx_type, db='minigrid')

    if args_parser.app_type == 'remote':
        app.run()
    else:
        app.run(host='0.0.0.0', port=2402)

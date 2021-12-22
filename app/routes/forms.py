from wtforms import widgets, Form, StringField, TextAreaField, SelectMultipleField, SubmitField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GameForm(Form):
    game_code = StringField('game_code')


class CommentForm(Form):
    comment = TextAreaField('Comment')


class CommentFormWithID(Form):
    obs_id = StringField('Observation ID')
    comment = TextAreaField('Comment')
    comment_submit = SubmitField('Submit')


class CommentMultipleSingles(Form):
    start_obs_id = StringField('Start observation')
    end_obs_id = StringField('End observation')
    comment = TextAreaField('Comment')
    multiple_singles_submit = SubmitField('Submit')


class CommentBatch(Form):
    start_obs_id = StringField('Start observation')
    end_obs_id = StringField('End observation')
    comment = TextAreaField('Comment')
    batch_submit = SubmitField('Submit')

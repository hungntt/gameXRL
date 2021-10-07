from wtforms import widgets, Form, StringField, TextAreaField, SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GameForm(Form):
    game_code = StringField('game_code')


class CommentForm(Form):
    comment = TextAreaField('Comment')


class CommentBatchForm(Form):
    start_obs_id = StringField('Start observation')
    end_obs_id = StringField('End observation')
    comment = TextAreaField('Comment')

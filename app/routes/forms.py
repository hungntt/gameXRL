from wtforms import Form, StringField, TextAreaField


class GameForm(Form):
    game_code = StringField('game_code')


class CommentForm(Form):
    comment = TextAreaField('Comment')

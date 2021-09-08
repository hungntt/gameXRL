from wtforms import Form, StringField


class GameForm(Form):
    game_code = StringField('game_code')


class CommentForm(Form):
    comment = StringField('comment')

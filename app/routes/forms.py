from wtforms import Form, StringField, TextAreaField
# from wtforms import Form, BooleanField, StringField, PasswordField, validators

class GameForm(Form):
    game_code = StringField('game_code')


class CommentForm(Form):
    comment = TextAreaField('Comment')

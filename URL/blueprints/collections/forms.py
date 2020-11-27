from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateCollection(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=80)])
    submit = SubmitField("Submit")

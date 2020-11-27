from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, URL


class CreateLink(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=80)])
    base = StringField("Url", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")
    collections = SelectField("Collection", coerce=int)

    def set_collections(self, collections):
        choices = [(col.id, str(col.name)) for col in collections]
        self.collections.choices = choices

from wtforms import Form, StringField, SubmitField, validators

class ScraperForm(Form):
   first_page = StringField("First page",[validators.URL(message=(u"That's not a valid URL.")), validators.InputRequired(message=(u"Please enter a value."))])
   last_page = StringField("Last page",[validators.URL(message=(u"That's not a valid URL.")), validators.Optional()])
   next_button = StringField("Next button", [validators.InputRequired(message=(u"PLease enter a value."))])
   series_name = StringField("Series name", [validators.Optional()])
   URL_beginning = StringField("URL beginning", [validators.Optional()])
   save_path = StringField("Save path", [validators.InputRequired(message=(u"Please enter a value."))])
   submit = SubmitField("Run code")
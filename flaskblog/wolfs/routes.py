import os
import json
import wolframalpha

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog.wolfs.forms import WolfAlphaForm


wolfs = Blueprint('wolfs', __name__)

with open('/etc/apiconfig.json') as configfile:
    config = json.load(configfile)




@wolfs.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', form=WolfAlphaForm())


@wolfs.route('/questions', methods=['GET', 'POST'])
def send_questions():
    form = WolfAlphaForm()
    if form.validate_on_submit():
        APP_ID = config.get('APP_ID')
        client = wolframalpha.Client(APP_ID)
        res = client.query(form.question.data)
        check = res.success

        if check == 'true':
            try :
                answer = next(res.results).text
                return render_template('answer.html', answer=answer, res=form.question.data)
            except Exception as e:
                flash('No answer found love! - Try formatting the question differently', 'warning')
        else:
            flash('No answer found love! - Try formatting the question differently', 'warning')
    return render_template('home.html', title='Question Hub', form=form)

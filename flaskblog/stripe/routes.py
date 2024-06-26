import os
import json
from flask import Flask
from flask import render_template, request, Blueprint, jsonify, url_for,redirect,abort
import stripe


main = Blueprint('main', __name__)

with open('/etc/config.json') as config_file:
	apiconfig = json.load(config_file)

app = Flask(__name__)


app.config['STRIPE_PUBLIC_KEY'] = apiconfig.get('STRIPE_PUBLIC_KEY')
app.config['STRIPE_SECRET_KEY'] = apiconfig.get('STRIPE_SECRET_KEY')


stripe.api_key = app.config['STRIPE_SECRET_KEY']

STRIPE_PRICE_ID = apiconfig.get('STRIPE_PRICE_ID')


@main.route('/donate')
def index():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1HMKyhAFnk4XTvTMYyKrfvmC',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('main.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.index', _external=True),
    )
    
    return render_template(
        'stripe.html', 
        checkout_session_id=session['id'], 
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )




@main.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1HMKyhAFnk4XTvTMYyKrfvmC',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('main.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }



@main.route('/thanks')
def thanks():
    return render_template('thanks.html')



@main.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_8e64hd0pqGVGSQ1t15nV6S7KYYroWHoZ'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}
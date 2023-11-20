from flask import Flask, request, jsonify , render_template
import stripe

#########################stripe config#####################
import configparser
config = configparser.ConfigParser()
config.read('config/setting.ini')
# Access values from the INI file
secret_key = config['KEYS']['SECRET_KEY']
publish_key = config['KEYS']['PUBLISH_KEY']
endpoint_secret = config['KEYS']['ENDPOINT_KEY']

stripe_keys = {
  'secret_key': secret_key,
  'publishable_key': publish_key
}
stripe.api_key = stripe_keys['secret_key']

###########################################################

app = Flask(__name__)

server_address = 'http://127.0.0.1:5000'


@app.route('/get_link', methods = ['GET', 'POST'])
def get_link():
    # Retrieve data from the request's JSON payload
    data = request.json
    username = data.get('username')
    lounge_id = data.get('lounge_id')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    price = data.get('price')
    item = data.get('item')
    currency = data.get('currency')

    prod_id = stripe.Product.create(name=item)
    price_id = stripe.Price.create(
        currency=currency,
        unit_amount=price,
        product=prod_id["id"],
    )

    success_url = f"{server_address}/payment_success?username={username}&lounge_id={lounge_id}&from_date={from_date}&to_date={to_date}"

    cancel_url = f'{server_address}/payment_fail?username={username}&lounge_id={lounge_id}&from_date={from_date}&to_date={to_date}'

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id["id"],
                "quantity": 1,
            }
        ],
        metadata={
            'item_name': 'LOUNGE A',
            'reservation_from': '2023-12-10 10:00:00',
        },
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    redirect_url = session.url
    return jsonify({'data': redirect_url})





@app.route('/payment_success', methods = ['GET', 'POST'])
def payment_success():

    username = request.args.get('username')
    lounge_id = request.args.get('lounge_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    #add transaction to the database

    return render_template('pay_success.html', username=username, lounge_id=lounge_id, from_date=from_date, to_date=to_date)



@app.route('/payment_fail', methods = ['GET', 'POST'])
def payment_fail():
    
    username = request.args.get('username')
    lounge_id = request.args.get('lounge_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    #add transaction to the database

    return render_template('pay_fail.html')



@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data

    sig_header = request.headers['STRIPE_SIGNATURE']



    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_failed':
      session = event['data']['object']


    elif event['type'] == 'checkout.session.async_payment_succeeded':
      session = event['data']['object']
      data = session['metadata']
      with open('example.txt','w') as file:

          file.write(str(data))

    elif event['type'] == 'checkout.session.completed':
      session = event['data']['object']
      data = session['metadata']
      with open('example.txt','w') as file:

        file.write(str(data))

    elif event['type'] == 'checkout.session.expired':
      session = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


if __name__ == "__main__":
    app.run()
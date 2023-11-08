from flask import Flask, request, jsonify , render_template
import stripe
from config.settings import strip_key


app = Flask(__name__)
stripe.api_key = strip_key


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

    success_url = f"http://127.0.0.1:5000/payment_success?username={username}&lounge_id={lounge_id}&from_date={from_date}&to_date={to_date}"

    cancel_url = f'http://127.0.0.1:5000/payment_fail?username={username}&lounge_id={lounge_id}&from_date={from_date}&to_date={to_date}'

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id["id"],
                "quantity": 1,
            }
        ],
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






if __name__ == "__main__":
    app.run()
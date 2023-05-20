from flask import Flask, request, jsonify

from recommendation import recommend_events_based_on_similarity, recommend_coupons_based_on_friends
from services.couponService import get_friends_coupons
from services.eventService import insert_event, get_all_events
from services.userService import insert_user, get_user
from validator import validate_user_schema, validate_event_schema, validate_coupon_schema

app = Flask(__name__)

@app.route('/create_user', methods=['POST'])
def create_user():
    """ function to create users """
    try:
        # Get the JSON data from the request body and validate it
        users_json = request.get_json()
        is_valid, message = validate_user_schema(users_json)

        if not is_valid:
            return jsonify({'error': message}), 400

        # Insert the user data into the users collection
        insert_user(user=users_json)

        # Return a success response with a JSON message
        return jsonify({'message': 'User created successfully.'})

    except Exception as e:
        # If there are any errors, return an error response with the error message
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    """Function to get users"""
    try:
        # Query the users collection to retrieve all users
        users = get_users()

        # Return the users as a JSON response
        return jsonify({'users': users})

    except Exception as e:
        # If there are any errors, return an error response with the error message
        return jsonify({'error': str(e)}), 500

@app.route('/create_event', methods=['POST'])
def create_event():
    """ function to create events """

    try:
        # Get the JSON data from the request body
        event_json = request.get_json()

        # Validate EventSchema schema
        is_valid, message = validate_event_schema(event_json)

        if not is_valid:
            return jsonify({'error': message}), 400

        # Insert the event data into the events collection
        insert_event(event=event_json)

        # Return a success response with a JSON message
        return jsonify({'message': 'Event created successfully.'})

    except Exception as err:
        # If there is any error, return an error response with the error message
        return jsonify({'error': str(err)}), 500

@app.route('/events', methods=['GET'])
def get_users():
    """Function to get events"""
    try:
        # Query the users collection to retrieve all events
        events = get_all_events()

        # Return the users as a JSON response
        return jsonify({'events': events})

    except Exception as e:
        # If there are any errors, return an error response with the error message
        return jsonify({'error': str(e)}), 500


@app.route('/coupons', methods=['GET'])
def get_coupons():
    """Function to get coupons"""
    try:
        # Retrieve the coupons from the database
        coupons = get_coupons()

        # Return the coupons as a JSON response
        return jsonify({'coupons': coupons})

    except Exception as e:
        # If there are any errors, return an error response with the error message
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations_similarity', methods=['GET'])
def get_recommendations_based_on_similarity():
    """ function to return coupon containing events based on the
     similarity users have with that event  """

    try:
        # Get the user with the specified username from the query parameters
        username = request.args.get('username')
        user = get_user(username)

        # Get all events from the events collection
        all_events = get_all_events()

        # Get the recommended events for the user
        coupon_data = recommend_events_based_on_similarity(all_events, user)

        # Validate CouponSchema schema
        is_valid, message = validate_coupon_schema(coupon_data)

        if not is_valid:
            return jsonify({'error': message}), 400

        # Return the coupon data as JSON
        return jsonify({'recommendation based on similarity': str(coupon_data)}), 200

    except Exception as err:
        # If there is any error, return an error response
        return jsonify({'error': str(err)}), 500


@app.route('/recommendations_friends', methods=['GET'])
def get_recommendations_based_on_friends():
    """ function to return the coupon's on user friends """

    try:
        # Get the user's friends' IDs
        username = request.args.get('username')
        user = get_user(username)
        friend_coupons = get_friends_coupons(user['friends'])

        coupon = recommend_coupons_based_on_friends(friend_coupons, user)

        # Validate CouponSchema schema
        is_valid, message = validate_coupon_schema(coupon)

        if not is_valid:
            return jsonify({'error': message}), 400

        # insert_coupon(coupon)
        return jsonify("recommendation based on your friends:", str(coupon)), 200

    except Exception as err:
        # If there is any error, return an error re
        return jsonify({'error': str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)

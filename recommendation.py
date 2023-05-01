def recommend_events_based_on_similarity(all_events, user, limit: int = 1):
    # Calculate the similarity score between the user and each event
    event_scores = []
    for event in all_events:
        score = 0
        if event['country'] == user['country']:
            score += 1
        if abs((event['begin_timestamp'] > user['registration_date'])):
            score += 1
        if abs((event['end_timestamp'] > user['registration_date'])):
            score += 1
        event_scores.append((event, score))

    # Sort the events by similarity score in descending order
    event_scores.sort(key=lambda x: x[1], reverse=True)

    # Generate the coupons for the recommended events
    selections = []
    for event, score in event_scores[:limit]:
        selection = {
            'event_id': event['id'],
            'odds': score / 3 * 100  # Convert the score to a percentage
        }
        selections.append(selection)

    coupon = {
        'selections': selections,
        'username': user['username']
    }

    return coupon


def recommend_coupons_based_on_friends(friend_coupons, user):
    # Use a list comprehension to extract all the event selections from the friend_coupons
    selections = [select for coupons in friend_coupons for coupon in coupons for select in coupon['selections']]

    # Create a new coupon with all the selections and the user's username
    coupon = {'selections': selections, 'username': user['username']}

    return coupon

import datetime

import networkx as nx


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
            'odds': score / 3 * 100,  # Convert the score to a percentage,
            'timestamp': datetime.datetime.now().isoformat()
        }
        selections.append(selection)

    coupon = {
        'selections': selections,
        'username': user['username'],
        'timestamp': datetime.datetime.now().isoformat()
    }

    return coupon


def recommend_coupons_based_on_friends(friend_coupons, user):
    # Use a list comprehension to extract all the event selections from the friend_coupons
    selections = [select for coupons in friend_coupons for coupon in coupons for select in coupon['selections']]

    # Create a new coupon with all the selections and the user's username
    coupon = {'selections': selections, 'username': user['username'], 'timestamp': datetime.datetime.now().isoformat()}

    return coupon


def createGraph(coupons):
    G = nx.Graph()

    for coupon in coupons:
        G.add_node(coupon['id'], selections=coupon['selections'])

    return G


def haveSimilarSelections(selections1, selections2, threshold=0.5):
    common_event_count = 0

    for selection1 in selections1:
        for selection2 in selections2:
            if selection1['event_id'] == selection2['event_id']:
                common_event_count += 1

    similarity_percentage = common_event_count / len(selections1)

    # Check if the similarity percentage exceeds the threshold
    if similarity_percentage >= threshold:
        return True
    else:
        return False


def findSimilarCoupons(coupons, coupon_id, threshold=0.5, limit=3):
    G = createGraph(coupons)

    if coupon_id in G.nodes:
        coupon_data = G.nodes[coupon_id]
        coupon_selections = coupon_data['selections']

        for node, data in G.nodes(data=True):
            if node != coupon_id and haveSimilarSelections(coupon_selections, data['selections'], threshold):
                G.add_edge(coupon_id, node)
                limit = limit - 1
            if limit == 0:
                break

    return list(G.neighbors(coupon_id))




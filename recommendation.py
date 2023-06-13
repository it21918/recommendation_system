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

def createGraph(coupons):
    G = nx.Graph()

    for coupon in coupons:
        for event in coupon['selections']:
            G.add_node(event["event_id"])

    return G

def popularEvents(coupons):
    G = createGraph(coupons)

    for i, coupon in enumerate(coupons):
        selections = coupon.get("selections", [])
        for j in range(len(selections)):
            event_id = selections[j].get("event_id")

            if not G.has_node(event_id):  # Check if node exists in the graph
                G.add_node(event_id)  # Add event as a node in the graph

            # Create edges between events from the same coupon
            for k in range(j + 1, len(selections)):
                other_event_id = selections[k].get("event_id")
                if event_id != other_event_id and not G.has_edge(event_id,
                                                                 other_event_id):  # Check if edge already exists
                    G.add_edge(event_id, other_event_id)

            # Create edges between events from different coupons
            for other_coupon in coupons[i + 1:]:
                other_selections = other_coupon.get("selections", [])
                for other_selection in other_selections:
                    other_event_id = other_selection.get("event_id")
                    if event_id != other_event_id and not G.has_edge(event_id,
                                                                     other_event_id):  # Check if edge already exists
                        G.add_edge(event_id, other_event_id)

    # Perform graph analysis to determine popularity
    # Calculate degree centrality for each node
    degree_centrality = nx.degree_centrality(G)

    # Sort events based on degree centrality to find popular ones
    popular_events = sorted(degree_centrality, key=degree_centrality.get, reverse=True)

    return popular_events


def recommend_coupon_from_popular_coupons(events, limit, user):
    return {
        'selections': events[:limit],
        'username': user['username']
    }

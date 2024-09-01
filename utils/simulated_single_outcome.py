import random

def get_match_outcome(rating1, rating2):
    # Define the weight options
    weight_options = [
        (2, 1),    # Option 1: weight (i,j) as 2 and (j,i) as 1
        (1.5, 1.5),# Option 2: weight (i,j) as 1.5 and (j,i) as 1.5
        (1, 2)     # Option 3: weight (i,j) as 1 and (j,i) as 2
    ]

    # Weight distributions based on rating differences
    w = [
        [0.84, 0.09, 0.07],  # > 400 difference
        [0.79, 0.11, 0.10],  # > 300 difference
        [0.70, 0.13, 0.17],  # > 200 difference
        [0.60, 0.15, 0.25],  # > 100 difference
        [0.47, 0.17, 0.36],  # > 0 difference
        [0.42, 0.17, 0.42]   # equal ratings
    ]

    rating_diff = rating1 - rating2

    # Determine the weight options based on the rating difference
    if rating_diff > 400:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[0], k=1)[0]
    elif rating_diff > 300:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[1], k=1)[0]
    elif rating_diff > 200:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[2], k=1)[0]
    elif rating_diff > 100:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[3], k=1)[0]
    elif rating_diff > 0:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[4], k=1)[0]
    elif rating_diff == 0:
        weight_ij, weight_ji = random.choices(weight_options, weights=w[5], k=1)[0]
    elif rating_diff > -100:
        weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[4]), k=1)[0]
    elif rating_diff > -200:
        weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[3]), k=1)[0]
    elif rating_diff > -300:
        weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[2]), k=1)[0]
    elif rating_diff > -400:
        weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[1]), k=1)[0]
    else:
        weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[0]), k=1)[0]

    # Determine the outcome based on the selected weight
    if weight_ij == 2:
        return print(f"player 1: {rating1}")
    elif weight_ij == 1.5:
        return "Draw"
    else:
        return print(f"player 2: {rating2}")

# outcome = get_match_outcome(1500, 1500)

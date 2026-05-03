def calculate_xp(data):
    # data = [(id, username, chapter, xp)]
    return sum([row[3] for row in data])


def get_level(xp):
    if xp < 100:
        return 1
    elif xp < 250:
        return 2
    elif xp < 500:
        return 3
    else:
        return 4

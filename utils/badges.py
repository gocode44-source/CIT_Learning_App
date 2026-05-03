def get_badges(completed_count, total):
    badges = []

    if completed_count >= 1:
        badges.append("🥉 Beginner")

    if completed_count >= 3:
        badges.append("🥈 Learner")

    if completed_count >= 5:
        badges.append("🥇 Achiever")

    if completed_count == total:
        badges.append("👑 Master")

    return badges

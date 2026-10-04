from Repositories.review_repository import insert_review, count_by_rating, count_by_month

COMMENT_MAX_LENGTH = 500
NAME_MAX_LENGTH = 100
NOTES = range(1, 6)

def create_review(payload):
    if payload.get("website"):
        return True, None

    rating = payload.get("rating")
    comment = (payload.get("comment") or "").strip()
    name = (payload.get("name") or "").strip() or None

    if not isinstance(rating, int) or isinstance(rating, bool) or rating not in NOTES:
        return None, "La note doit être un entier entre 1 et 5"
    if not comment:
        return None, "Le commentaire est requis"
    if len(comment) > COMMENT_MAX_LENGTH:
        return None, "Le commentaire est trop long"
    if name and len(name) > NAME_MAX_LENGTH:
        return None, "Le nom est trop long"

    insert_review(name, rating, comment)
    return True, None

def get_stats():
    distribution = {str(note): 0 for note in NOTES}
    for rating, count in count_by_rating():
        distribution[str(rating)] = count

    total = sum(distribution.values())
    somme_notes = sum(int(note) * count for note, count in distribution.items())
    moyenne = round(somme_notes / total, 2) if total else None

    timeline = [{"month": month, "count": count} for month, count in count_by_month()]

    return {
        "count": total,
        "average": moyenne,
        "distribution": distribution,
        "timeline": timeline
    }

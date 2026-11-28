def save_result(client, kind, title, data):
    """Saves a row in the logged-in user's own account (RLS sets user_id automatically)."""
    try:
        client.table("saved_results").insert(
            {"kind": kind, "title": title, "data": data}
        ).execute()
        return True, "Saved!"
    except Exception as e:
        return False, "Could not save: " + str(e)[:100]


def list_results(client, kind=None, limit=50):
    """Returns only this user's rows. RLS never returns another user's rows."""
    try:
        q = (
            client.table("saved_results")
            .select("id,kind,title,data,created_at")
            .order("created_at", desc=True)
            .limit(limit)
        )
        if kind:
            q = q.eq("kind", kind)
        return q.execute().data
    except Exception:
        return []


def delete_result(client, row_id):
    try:
        client.table("saved_results").delete().eq("id", row_id).execute()
        return True
    except Exception:
        return False

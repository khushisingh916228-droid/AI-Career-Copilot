import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def new_client():
    """Har user session ke liye ALAG client. Shared client se users ke session mix ho jate."""
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def _friendly(e):
    msg = str(e).lower()
    if "already registered" in msg or "already been registered" in msg:
        return "Ye email already registered hai. Login karo."
    if "invalid login" in msg:
        return "Email ya password galat hai."
    if "password" in msg and ("weak" in msg or "at least" in msg or "should" in msg):
        return "Password kamzor hai (kam se kam 8 characters, letters aur digits)."
    if "rate limit" in msg:
        return "Bahut zyada koshish ho gayi, thodi der baad try karo."
    if "invalid" in msg and "email" in msg:
        return "Email sahi format mein daalo."
    return "Kuch error aaya: " + str(e)[:100]


def sign_up(email, password):
    """Returns (ok, message, client)"""
    client = new_client()
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.session is None:
            return False, "Account ban gaya, par email confirm karna padega.", client
        return True, "Account ban gaya!", client
    except Exception as e:
        return False, _friendly(e), client


def sign_in(email, password):
    """Returns (ok, message, client)"""
    client = new_client()
    try:
        client.auth.sign_in_with_password({"email": email, "password": password})
        return True, "Login ho gaya!", client
    except Exception as e:
        return False, _friendly(e), client


def sign_out(client):
    try:
        client.auth.sign_out()
    except Exception:
        pass

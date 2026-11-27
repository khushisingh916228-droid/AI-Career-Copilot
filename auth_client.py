import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def new_client():
    """A separate client for every user session. A shared client would mix up sessions between users."""
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def _friendly(e):
    msg = str(e).lower()
    if "already registered" in msg or "already been registered" in msg:
        return "This email is already registered. Please log in."
    if "invalid login" in msg:
        return "Incorrect email or password."
    if "password" in msg and ("weak" in msg or "at least" in msg or "should" in msg):
        return "Password is too weak (use at least 8 characters with letters and digits)."
    if "rate limit" in msg:
        return "Too many attempts. Please try again later."
    if "invalid" in msg and "email" in msg:
        return "Please enter a valid email address."
    return "Something went wrong: " + str(e)[:100]


def sign_up(email, password):
    """Returns (ok, message, client)"""
    client = new_client()
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.session is None:
            return False, "Account created, but you need to confirm your email.", client
        return True, "Account created!", client
    except Exception as e:
        return False, _friendly(e), client


def sign_in(email, password):
    """Returns (ok, message, client)"""
    client = new_client()
    try:
        client.auth.sign_in_with_password({"email": email, "password": password})
        return True, "Logged in!", client
    except Exception as e:
        return False, _friendly(e), client


def sign_out(client):
    try:
        client.auth.sign_out()
    except Exception:
        pass

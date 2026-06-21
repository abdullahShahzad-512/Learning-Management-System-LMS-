import os
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

@click.command("seed-admin")
@with_appcontext
def seed_admin():
    """Create the initial super admin account from .env credentials."""
    username = os.environ.get("ADMIN_USERNAME")
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")

    if not all([username, email, password]):
        click.echo("Missing ADMIN_USERNAME, ADMIN_EMAIL, or ADMIN_PASSWORD in .env")
        return

    existing_email = User.query.filter_by(email=email).first()
    existing_username = User.query.filter_by(username=username).first()
    if existing_email or existing_username:
        existing = existing_email or existing_username
        click.echo(f"Admin already exists: {existing.username} ({existing.email})")
        return

    admin = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()
    click.echo(f"✅ Super admin created: {username} ({email})")
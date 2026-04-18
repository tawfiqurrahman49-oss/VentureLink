from flask import render_template
from flask_login import login_required, current_user
from app.matches import matches_bp
from app.models import Match


@matches_bp.route('/')
@login_required
def list():
    matches = Match.query.filter(
        (Match.user_a_id == current_user.id) |
        (Match.user_b_id == current_user.id)
    ).order_by(Match.created_at.desc()).all()

    paired = []
    for match in matches:
        other = match.user_b if match.user_a_id == current_user.id else match.user_a
        if other.profile:
            paired.append({'match': match, 'user': other, 'profile': other.profile})

    return render_template('matches/list.html', paired=paired)

from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, Claim, Policy

claims_bp = Blueprint('claims', __name__)


@claims_bp.route('/claims')
@login_required
def claims_list():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    claims = Claim.query.filter_by(customer_id=current_user.customer.id).order_by(Claim.submitted_at.desc()).all() if current_user.customer else []
    return render_template('claims.html', claims=claims)


@claims_bp.route('/submit-claim', methods=['GET', 'POST'])
@login_required
def submit_claim():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    policies = Policy.query.filter_by(customer_id=current_user.customer.id).all() if current_user.customer else []
    if request.method == 'POST':
        policy_id = request.form.get('policy_id', type=int)
        claim_amount = request.form.get('claim_amount', type=float)
        claim_reason = request.form.get('claim_reason', '').strip()
        incident_date = request.form.get('incident_date')
        if not policy_id or not claim_amount or not claim_reason or not incident_date:
            flash('Please fill in all required claim fields.', 'danger')
            return render_template('submit_claim.html', policies=policies)
        policy = Policy.query.filter_by(id=policy_id, customer_id=current_user.customer.id).first()
        if not policy:
            flash('Selected policy is not valid for your account.', 'danger')
            return render_template('submit_claim.html', policies=policies)
        claim = Claim(
            customer_id=current_user.customer.id,
            policy_id=policy.id,
            claim_amount=claim_amount,
            claim_reason=claim_reason,
            incident_date=datetime.strptime(incident_date, '%Y-%m-%d').date(),
            status='Pending',
        )
        db.session.add(claim)
        db.session.commit()
        flash('Claim submitted successfully.', 'success')
        return redirect(url_for('claims.claims_list'))
    return render_template('submit_claim.html', policies=policies)

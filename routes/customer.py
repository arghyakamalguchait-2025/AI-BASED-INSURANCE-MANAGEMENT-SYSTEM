from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, Customer, Policy, Claim, User

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    customer = current_user.customer
    policies = Policy.query.filter_by(customer_id=customer.id).all() if customer else []
    claims = Claim.query.filter_by(customer_id=customer.id).all() if customer else []
    active_policies = [p for p in policies if p.status.lower() == 'active']
    pending_claims = [c for c in claims if c.status.lower() == 'pending']
    approved_claims = [c for c in claims if c.status.lower() == 'approved']
    monthly_premium = sum(p.premium_amount for p in active_policies)
    expiring = [p for p in policies if 0 <= (p.expiry_date - datetime.utcnow().date()).days <= 30]
    return render_template(
        'dashboard.html',
        customer=customer,
        policies=policies,
        active_policies=active_policies,
        pending_claims=pending_claims,
        approved_claims=approved_claims,
        monthly_premium=monthly_premium,
        expiring=expiring,
        total_policies=len(policies),
    )


@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    user = current_user
    if request.method == 'POST':
        user.full_name = request.form.get('full_name', user.full_name).strip()
        user.phone = request.form.get('phone', user.phone).strip()
        customer = user.customer or Customer(user_id=user.id)
        customer.address = request.form.get('address', customer.address or '')
        customer.city = request.form.get('city', customer.city or '')
        customer.state = request.form.get('state', customer.state or '')
        db.session.add(customer)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
    return render_template('profile.html', user=user, customer=user.customer)


@customer_bp.route('/policies')
@login_required
def policies():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    policies = Policy.query.join(Customer).filter(Customer.user_id == current_user.id).all()
    return render_template('policies.html', policies=policies)

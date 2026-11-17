from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from models import db, User, Customer, Policy, Claim, InsurancePlan

admin_bp = Blueprint('admin', __name__)


def admin_required():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return False
    return True


@admin_bp.route('/admin-dashboard')
@login_required
def dashboard():
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    customers = User.query.filter_by(role='customer').all()
    plans = InsurancePlan.query.all()
    policies = Policy.query.all()
    claims = Claim.query.all()
    return render_template(
        'admin_dashboard.html',
        customers=customers,
        plans=plans,
        policies=policies,
        claims=claims,
        total_customers=len(customers),
        total_plans=len(plans),
        total_policies=len(policies),
        active_policies=sum(1 for p in policies if p.status.lower() == 'active'),
        expired_policies=sum(1 for p in policies if p.status.lower() == 'expired'),
        pending_claims=sum(1 for c in claims if c.status.lower() == 'pending'),
        approved_claims=sum(1 for c in claims if c.status.lower() == 'approved'),
        rejected_claims=sum(1 for c in claims if c.status.lower() == 'rejected'),
    )


@admin_bp.route('/admin/customers')
@login_required
def customers():
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    customers = User.query.filter_by(role='customer').all()
    return render_template('admin_customers.html', customers=customers)


@admin_bp.route('/admin/policies')
@login_required
def policies():
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    items = Policy.query.all()
    return render_template('admin_policies.html', policies=items)


@admin_bp.route('/admin/claims')
@login_required
def claims():
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    items = Claim.query.order_by(Claim.submitted_at.desc()).all()
    return render_template('admin_claims.html', claims=items)


@admin_bp.route('/admin/claims/<int:claim_id>/approve', methods=['POST'])
@login_required
def approve_claim(claim_id):
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'Approved'
    claim.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash('Claim approved successfully.', 'success')
    return redirect(url_for('admin.claims'))


@admin_bp.route('/admin/claims/<int:claim_id>/reject', methods=['POST'])
@login_required
def reject_claim(claim_id):
    if not admin_required():
        flash('Admin access required.', 'danger')
        return redirect(url_for('auth.admin_login'))
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'Rejected'
    claim.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash('Claim rejected successfully.', 'success')
    return redirect(url_for('admin.claims'))

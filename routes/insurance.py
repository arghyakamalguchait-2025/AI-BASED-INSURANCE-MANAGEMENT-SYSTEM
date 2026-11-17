from datetime import date, timedelta
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, InsurancePlan, Customer, Policy
from ai.recommendation_engine import recommend_plans
from ai.premium_engine import calculate_premium

insurance_bp = Blueprint('insurance', __name__)


@insurance_bp.route('/plans')
def plans():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    query = InsurancePlan.query.filter_by(is_active=True)
    if category and category != 'all':
        query = query.filter(InsurancePlan.category == category)
    if search:
        query = query.filter(InsurancePlan.plan_name.ilike(f'%{search}%'))
    plans = query.order_by(InsurancePlan.monthly_premium.asc()).all()
    return render_template('plans.html', plans=plans, active_category=category, search_term=search)


@insurance_bp.route('/calculator', methods=['GET','POST'])
def calculator():
    result = None
    if request.method == 'POST':
        category = request.form.get('insurance_type')
        age = request.form.get('age', type=int)
        coverage_amount = request.form.get('coverage_amount', type=float)
        duration = request.form.get('duration', type=int)
        if category and age and coverage_amount and duration:
            if age < 18 or age > 80:
                flash('Age must be between 18 and 80.', 'danger')
            elif coverage_amount <= 0 or duration <= 0:
                flash('Coverage amount and duration must be positive.', 'danger')
            else:
                result = calculate_premium(category, age, coverage_amount, duration)
    return render_template('calculator.html', result=result)


@insurance_bp.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    result = None
    if request.method == 'POST':
        age = request.form.get('age', type=int)
        category = request.form.get('insurance_category')
        budget = request.form.get('monthly_budget', type=float)
        coverage_preference = request.form.get('coverage_preference')
        if age and category and budget and coverage_preference:
            result = recommend_plans(age, category, budget, coverage_preference)
    return render_template('recommendations.html', result=result)


@insurance_bp.route('/compare')
def compare():
    plan_ids = request.args.getlist('plan_id')
    selected = []
    if plan_ids:
        selected = InsurancePlan.query.filter(InsurancePlan.id.in_([int(pid) for pid in plan_ids if pid])).all()
    plans = InsurancePlan.query.filter_by(is_active=True).all()
    return render_template('compare.html', selected=selected, plans=plans)


@insurance_bp.route('/apply-plan/<int:plan_id>', methods=['POST'])
@login_required
def apply_plan(plan_id):
    if current_user.role != 'customer':
        flash('Only customers can apply for insurance.', 'danger')
        return redirect(url_for('auth.login'))

    plan = InsurancePlan.query.get_or_404(plan_id)
    customer = current_user.customer
    if not customer:
        flash('Complete your profile before applying for a plan.', 'danger')
        return redirect(url_for('customer.profile'))

    existing = Policy.query.filter_by(customer_id=customer.id, plan_id=plan.id).first()
    if existing:
        flash('You already hold this plan.', 'warning')
        return redirect(url_for('insurance.plans'))

    policy_number = f'INS-{random.randint(10000, 99999)}-{plan.id}'
    start_date = date.today()
    expiry_date = start_date + timedelta(days=365 * plan.duration_years)
    policy = Policy(
        customer_id=customer.id,
        plan_id=plan.id,
        policy_number=policy_number,
        coverage_amount=plan.coverage_amount,
        premium_amount=plan.monthly_premium,
        start_date=start_date,
        expiry_date=expiry_date,
        status='Active',
    )
    db.session.add(policy)
    db.session.commit()
    flash('Policy applied successfully.', 'success')
    return redirect(url_for('customer.dashboard'))

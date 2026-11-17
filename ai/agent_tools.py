from datetime import datetime

from flask import flash
from werkzeug.exceptions import BadRequest

from models import InsurancePlan, Policy, Claim, db


def validated_category(category):
    valid = {'life insurance', 'health insurance', 'vehicle insurance'}
    key = (category or '').strip().lower()
    if key not in valid:
        raise ValueError('Category must be Life Insurance, Health Insurance, or Vehicle Insurance.')
    return {
        'life insurance': 'Life Insurance',
        'health insurance': 'Health Insurance',
        'vehicle insurance': 'Vehicle Insurance',
    }[key]


def search_insurance_plans(category=None):
    query = InsurancePlan.query.filter_by(is_active=True)
    if category:
        query = query.filter(db.func.lower(InsurancePlan.category) == str(category).strip().lower())
    return query.order_by(InsurancePlan.monthly_premium.asc()).all()


def recommend_insurance(age, category, budget, coverage_preference):
    if age is None or budget is None:
        raise ValueError('Age and budget are required.')
    age = int(age)
    budget = float(budget)
    category_name = validated_category(category)
    preference_map = {'basic': 0.7, 'standard': 1.0, 'premium': 1.3}
    preference = (coverage_preference or 'standard').lower()
    factor = preference_map.get(preference, 1.0)
    plans = search_insurance_plans(category_name)
    suitable = []
    for plan in plans:
        if plan.monthly_premium <= budget * 1.15 and plan.coverage_amount >= 250000 * factor:
            suitable.append(plan)
    if not suitable:
        return {
            'message': 'No plan matches your current settings. Try increasing the monthly budget or choosing a lower coverage preference.',
            'plans': [],
        }
    suitable.sort(key=lambda p: abs(p.monthly_premium - budget))
    recommend = suitable[0]
    return {
        'recommended_plan': recommend.plan_name,
        'category': recommend.category,
        'estimated_monthly_premium': recommend.monthly_premium,
        'coverage_amount': recommend.coverage_amount,
        'duration': recommend.duration_years,
        'benefits': recommend.benefits,
        'explanation': (
            f'This plan matches your selected {recommend.category.lower()} category and monthly budget of ₹{budget:.0f}. '
            f'It is a suitable fictional recommendation based on your age and preferred coverage level.'
        ),
        'plans': suitable[:3],
    }


def calculate_premium_tool(category, age, coverage_amount, duration):
    from ai.premium_engine import calculate_premium

    return calculate_premium(category, age, coverage_amount, duration)


def compare_insurance_plans(plan_ids):
    if not plan_ids:
        raise ValueError('Please select at least one plan for comparison.')
    ids = [int(pid) for pid in plan_ids if str(pid).strip()]
    plans = InsurancePlan.query.filter(InsurancePlan.id.in_(ids)).all()
    if not plans:
        raise ValueError('No valid plans were found for comparison.')
    return plans


def get_my_policies(authenticated_user):
    if not authenticated_user or not getattr(authenticated_user, 'id', None):
        raise ValueError('Authentication required.')
    customer = authenticated_user.customer
    if not customer:
        return []
    return Policy.query.filter_by(customer_id=customer.id).order_by(Policy.start_date.desc()).all()


def get_my_claims(authenticated_user):
    if not authenticated_user or not getattr(authenticated_user, 'id', None):
        raise ValueError('Authentication required.')
    customer = authenticated_user.customer
    if not customer:
        return []
    return Claim.query.filter_by(customer_id=customer.id).order_by(Claim.submitted_at.desc()).all()


def get_expiring_policies(authenticated_user):
    policies = get_my_policies(authenticated_user)
    today = datetime.utcnow().date()
    expiring = []
    for policy in policies:
        delta = (policy.expiry_date - today).days
        if 0 <= delta <= 30:
            expiring.append(policy)
    return expiring


def prepare_claim_submission(authenticated_user, policy_id, amount, reason):
    if not authenticated_user:
        raise ValueError('Authentication required.')
    customer = authenticated_user.customer
    if not customer:
        raise ValueError('Customer profile missing.')
    policy = Policy.query.filter_by(id=int(policy_id), customer_id=customer.id).first()
    if not policy:
        raise ValueError('Policy not found for this customer.')
    if amount is None or float(amount) <= 0:
        raise ValueError('Claim amount must be positive.')
    if not reason or len(reason.strip()) < 5:
        raise ValueError('Claim reason is required.')
    return {
        'customer_id': customer.id,
        'policy_id': policy.id,
        'policy_number': policy.policy_number,
        'claim_amount': float(amount),
        'claim_reason': reason.strip(),
        'status': 'Pending',
    }


def submit_confirmed_claim(authenticated_user, confirmed_claim_data):
    if not authenticated_user:
        raise ValueError('Authentication required.')
    if not confirmed_claim_data:
        raise ValueError('No claim data to submit.')
    data = confirmed_claim_data
    customer = authenticated_user.customer
    policy = Policy.query.filter_by(id=int(data['policy_id']), customer_id=customer.id).first()
    if not policy:
        raise ValueError('Policy not found for this customer.')
    claim = Claim(
        customer_id=customer.id,
        policy_id=policy.id,
        claim_amount=float(data['claim_amount']),
        claim_reason=data['claim_reason'],
        incident_date=datetime.utcnow().date(),
        status='Pending',
    )
    db.session.add(claim)
    db.session.commit()
    return claim

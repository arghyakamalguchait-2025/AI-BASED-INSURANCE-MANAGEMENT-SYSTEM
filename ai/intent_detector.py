import re


def detect_intent(message):
    text = (message or '').lower()
    patterns = {
        'insurance_definition': ['what is insurance', 'define insurance', 'insurance means'],
        'life_insurance': ['life insurance', 'term insurance'],
        'health_insurance': ['health insurance', 'medical insurance'],
        'vehicle_insurance': ['vehicle insurance', 'car insurance', 'auto insurance'],
        'premium': ['premium', 'monthly premium'],
        'coverage': ['coverage', 'sum assured'],
        'deductible': ['deductible', 'deductible amount'],
        'claim': ['claim', 'file a claim'],
        'calculate_premium': ['calculate premium', 'premium estimate', 'estimate premium'],
        'compare_plans': ['compare plans', 'compare insurance', 'which plan is better'],
        'renew_policy': ['renew policy', 'policy renewal'],
        'recommendation': ['recommend plan', 'recommend insurance', 'best plan for me'],
        'show_policies': ['show my policies', 'my active policies', 'what policies do i have'],
        'show_claims': ['show my claims', 'check my claim status', 'claim status'],
        'expiring_policies': ['policies expiring soon', 'expire soon', 'expiring policies'],
        'submit_claim': ['submit claim', 'file claim'],
    }
    for intent, keywords in patterns.items():
        if any(keyword in text for keyword in keywords):
            return intent
    if 'hello' in text or 'hi' in text:
        return 'greeting'
    if 'thank' in text:
        return 'thank_you'
    return 'general'

from ai.intent_detector import detect_intent


FAQs = {
    'insurance_definition': 'Insurance is a financial protection plan that helps cover future risks and unexpected expenses.',
    'life_insurance': 'Life insurance provides financial support to your family in case of your death or illness, depending on the plan.',
    'health_insurance': 'Health insurance helps cover medical expenses like hospital bills, medicines, and specialist consultations.',
    'vehicle_insurance': 'Vehicle insurance protects your car or bike against accidents, damage, and road-related risks.',
    'premium': 'A premium is the amount paid regularly to keep the insurance policy active.',
    'coverage': 'Coverage is the total amount an insurance plan can pay for covered events.',
    'deductible': 'A deductible is the amount one pays before the insurer contributes to the claim.',
    'claim': 'A claim is a formal request to receive insurance benefits for a covered event.',
    'submit_claim': 'You can submit a claim from your dashboard by selecting an owned policy and submitting the claim amount and reason.',
    'calculate_premium': 'Use the premium calculator in the app to estimate a fictional insurance premium based on category, age, coverage, and duration.',
    'compare_plans': 'Compare plans using the plan comparison page to review premium, coverage, duration, and benefits.',
    'renew_policy': 'Policy renewal is usually handled in the policy management area; in this demo, policies can be tracked in your dashboard.',
    'greeting': 'Hello! I am InsureBot AI. I can help explain plans, estimate premiums, and guide you through your insurance needs.',
    'thank_you': 'You are welcome! I am here to help with insurance information and policy support.',
}


def rule_based_response(message, intent=None):
    intent_name = intent or detect_intent(message)
    return FAQs.get(intent_name, 'I can help with insurance policies, premium estimates, and claim guidance. Ask me about life, health, or vehicle insurance.')

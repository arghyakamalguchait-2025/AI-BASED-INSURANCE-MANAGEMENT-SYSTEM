def calculate_premium(category, age, coverage_amount, duration):
    base_rates = {'Life Insurance': 0.003, 'Health Insurance': 0.008, 'Vehicle Insurance': 0.015}
    category_name = category.strip()
    if category_name not in base_rates:
        raise ValueError('Invalid insurance category.')
    age = int(age)
    coverage_amount = float(coverage_amount)
    duration = int(duration)
    age_factor = 1 + max(age - 25, 0) * 0.01
    annual_premium = coverage_amount * base_rates[category_name] * age_factor
    monthly_premium = annual_premium / 12
    total_premium = annual_premium * duration
    return {
        'category': category_name,
        'estimated_monthly_premium': round(monthly_premium, 2),
        'estimated_annual_premium': round(annual_premium, 2),
        'estimated_total_premium': round(total_premium, 2),
        'coverage_amount': round(coverage_amount, 2),
        'duration': duration,
    }

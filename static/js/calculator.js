document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form && form.querySelector('input[name="coverage_amount"]')) {
        form.addEventListener('submit', function () {
            const age = Number(form.querySelector('input[name="age"]').value);
            const coverage = Number(form.querySelector('input[name="coverage_amount"]').value);
            const duration = Number(form.querySelector('input[name="duration"]').value);
            if (age < 18 || age > 80) {
                alert('Age must be between 18 and 80.');
                return false;
            }
            if (coverage <= 0 || duration <= 0) {
                alert('Coverage and duration must be positive numbers.');
                return false;
            }
        });
    }
});

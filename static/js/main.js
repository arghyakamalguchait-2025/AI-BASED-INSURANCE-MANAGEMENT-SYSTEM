document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alertEl) {
        var closeBtn = alertEl.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                alertEl.remove();
            });
        }
    });
});

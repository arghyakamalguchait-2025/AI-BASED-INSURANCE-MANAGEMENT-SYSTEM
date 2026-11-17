document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach(function (card) {
        card.classList.add('shadow-sm');
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const counters = document.querySelectorAll('.counter');

    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const step = target / (duration / 30);
                let current = 0;

                const updateCounter = setInterval(function() {
                    current += step;
                    if (current >= target) {
                        current = target;
                        clearInterval(updateCounter);
                    }
                    counter.textContent = Math.floor(current) + (counter.getAttribute('data-target') === '100' ? '%' : '+');
                }, 30);

                observer.unobserve(counter);
            }
        });
    }, options);

    counters.forEach(counter => {
        observer.observe(counter);
    });
});

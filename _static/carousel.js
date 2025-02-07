document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for sphinx-design to initialize
    setTimeout(() => {
        initializeCarousels();
    }, 500);
});

function initializeCarousels() {
    const carousels = document.querySelectorAll('.sd-cards-carousel');

    carousels.forEach((carousel, index) => {
        // Ensure carousel is wrapped
        if (!carousel.parentElement.classList.contains('sd-cards-carousel-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'sd-cards-carousel-wrapper';
            carousel.parentNode.insertBefore(wrapper, carousel);
            wrapper.appendChild(carousel);
        }
        
        // Create navigation buttons
        const prevButton = document.createElement('button');
        prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
        prevButton.className = 'carousel-nav-button carousel-prev';
        
        const nextButton = document.createElement('button');
        nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
        nextButton.className = 'carousel-nav-button carousel-next';
        
        // Add buttons to carousel
        carousel.parentElement.appendChild(prevButton);
        carousel.parentElement.appendChild(nextButton);
        
        // Navigation logic
        prevButton.addEventListener('click', () => {
            const cardWidth = carousel.offsetWidth;
            carousel.scrollBy({
                left: -cardWidth,
                behavior: 'smooth'
            });
        });
        
        nextButton.addEventListener('click', () => {
            const cardWidth = carousel.offsetWidth;
            carousel.scrollBy({
                left: cardWidth,
                behavior: 'smooth'
            });
        });
        
        // Update button states
        const updateButtons = () => {
            prevButton.classList.toggle('disabled', carousel.scrollLeft <= 0);
            nextButton.classList.toggle('disabled', 
                carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth - 5); // 5px buffer
        };
        
        // Add event listeners
        carousel.addEventListener('scroll', updateButtons);
        window.addEventListener('resize', () => {
            updateButtons();
            // Ensure proper scroll position on resize
            const currentIndex = Math.round(carousel.scrollLeft / carousel.offsetWidth);
            carousel.scrollTo({
                left: currentIndex * carousel.offsetWidth,
                behavior: 'auto'
            });
        });
        
        // Initialize button states
        updateButtons();
    });
}
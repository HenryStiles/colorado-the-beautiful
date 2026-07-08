document.addEventListener('DOMContentLoaded', () => {
  // Interactive 3D Card Flipping
  const cards = document.querySelectorAll('.card');

  cards.forEach(card => {
    // Flip card on click
    card.addEventListener('click', (e) => {
      // If clicking inside description scrollbar or similar, avoid toggling if needed. 
      // But standard clicks toggle.
      card.classList.toggle('flipped');
      
      // Update ARIA expanded state
      const isFlipped = card.classList.contains('flipped');
      card.setAttribute('aria-expanded', isFlipped);
    });

    // Flip card on Enter or Space press when focused
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault(); // Prevent page scrolling on Space
        card.classList.toggle('flipped');
        const isFlipped = card.classList.contains('flipped');
        card.setAttribute('aria-expanded', isFlipped);
      }
    });
  });

  // Filter System
  const filterButtons = document.querySelectorAll('.filter-btn');
  const cardContainers = document.querySelectorAll('.card-container');

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove active class from all buttons and add to clicked
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');

      const filterValue = button.getAttribute('data-filter');

      cardContainers.forEach(container => {
        const cardCategory = container.getAttribute('data-category');
        
        // Before filtering, if the card was flipped, flip it back so it looks clean
        const innerCard = container.querySelector('.card');
        if (innerCard.classList.contains('flipped')) {
          innerCard.classList.remove('flipped');
          innerCard.setAttribute('aria-expanded', 'false');
        }

        if (filterValue === 'all' || cardCategory === filterValue) {
          container.classList.remove('hidden');
        } else {
          container.classList.add('hidden');
        }
      });
    });
  });
});

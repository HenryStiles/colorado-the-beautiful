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
});

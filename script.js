document.addEventListener('DOMContentLoaded', () => {
  const cardContainers = document.querySelectorAll('.card-container');
  const modal = document.getElementById('photo-modal');
  const modalImg = document.getElementById('modal-img');
  const modalTitle = document.getElementById('modal-title');
  const modalLocationText = document.getElementById('modal-location-text');
  const modalSubmitter = document.getElementById('modal-submitter');
  const modalStory = document.getElementById('modal-story');
  const modalCounter = document.getElementById('modal-counter');
  const modalClose = document.getElementById('modal-close');
  const modalPrev = document.getElementById('modal-prev');
  const modalNext = document.getElementById('modal-next');

  let currentIndex = 0;
  let cardDataList = [];

  // Parse cards data
  cardContainers.forEach((cardContainer, idx) => {
    const title = cardContainer.getAttribute('data-title') || cardContainer.querySelector('.card-title')?.textContent || '';
    const submitter = cardContainer.getAttribute('data-submitter') || cardContainer.querySelector('.fact-value')?.textContent || '';
    const location = cardContainer.getAttribute('data-location') || cardContainer.querySelector('.card-location')?.textContent?.trim() || '';
    const photo = cardContainer.getAttribute('data-photo') || cardContainer.querySelector('.card-image')?.getAttribute('src') || '';
    const storyHtml = cardContainer.getAttribute('data-story') || cardContainer.querySelector('.card-back-desc')?.innerHTML || '';

    cardDataList.push({ title, submitter, location, photo, storyHtml });

    // Open Modal on Card Click
    cardContainer.addEventListener('click', (e) => {
      e.preventDefault();
      openModal(idx);
    });

    // Support Keyboard Navigation (Enter or Space to open modal)
    cardContainer.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal(idx);
      }
    });
  });

  function openModal(index) {
    if (!modal || cardDataList.length === 0) return;
    currentIndex = index;
    updateModalContent();

    // Check if running inside an iframe
    const isInIframe = window.self !== window.top;
    if (isInIframe) {
      const clickedCard = cardContainers[index];
      if (clickedCard) {
        const rect = clickedCard.getBoundingClientRect();
        // Calculate card's vertical position relative to the top of the iframe document
        const cardY = rect.top + window.scrollY;
        
        const modalContainer = modal.querySelector('.modal-container');
        if (modalContainer) {
          // Adjust overlay to expand to the full height of the iframe document
          modal.style.position = 'absolute';
          modal.style.height = document.documentElement.scrollHeight + 'px';
          modal.style.alignItems = 'flex-start';
          
          // Position the modal container near the clicked card
          const targetTop = Math.max(20, cardY - 150);
          modalContainer.style.marginTop = targetTop + 'px';
        }
      }
    } else {
      // Reset styles to default if not in an iframe
      modal.style.position = '';
      modal.style.height = '';
      modal.style.alignItems = '';
      const modalContainer = modal.querySelector('.modal-container');
      if (modalContainer) {
        modalContainer.style.marginTop = '';
      }
    }

    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
  }

  function updateModalContent() {
    const data = cardDataList[currentIndex];
    if (!data) return;

    modalImg.src = data.photo;
    modalImg.alt = data.title;
    modalTitle.textContent = data.title;
    modalLocationText.textContent = data.location;
    modalSubmitter.textContent = data.submitter;
    modalStory.innerHTML = `"${data.storyHtml}"`;
    modalCounter.textContent = `${currentIndex + 1} / ${cardDataList.length}`;
  }

  if (modalClose) modalClose.addEventListener('click', closeModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  if (modalPrev) {
    modalPrev.addEventListener('click', (e) => {
      e.stopPropagation();
      currentIndex = (currentIndex - 1 + cardDataList.length) % cardDataList.length;
      updateModalContent();
    });
  }

  if (modalNext) {
    modalNext.addEventListener('click', (e) => {
      e.stopPropagation();
      currentIndex = (currentIndex + 1) % cardDataList.length;
      updateModalContent();
    });
  }

  // Keyboard Shortcuts inside Modal
  document.addEventListener('keydown', (e) => {
    if (!modal || !modal.classList.contains('active')) return;
    if (e.key === 'Escape') closeModal();
    if (e.key === 'ArrowLeft') {
      currentIndex = (currentIndex - 1 + cardDataList.length) % cardDataList.length;
      updateModalContent();
    }
    if (e.key === 'ArrowRight') {
      currentIndex = (currentIndex + 1) % cardDataList.length;
      updateModalContent();
    }
  });
});

// Automatically send document height to parent window (WordPress) for dynamic iframe resizing
function sendHeightToParent() {
  const height = document.body.scrollHeight || document.documentElement.scrollHeight;
  window.parent.postMessage({ type: 'resize-iframe', height: height }, '*');
}

// Trigger height update on load, resize, and orientation change
window.addEventListener('load', sendHeightToParent);
window.addEventListener('resize', sendHeightToParent);

if (window.ResizeObserver) {
  const observer = new ResizeObserver(sendHeightToParent);
  observer.observe(document.body);
}

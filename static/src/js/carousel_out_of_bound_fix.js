/**odoo/module */
document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.querySelector('#myCarousel1756706871012');
  if (!carousel) return;
  const indicators = carousel.querySelectorAll('.carousel-indicators button');
  const items = carousel.querySelectorAll('.carousel-item');

  carousel.addEventListener('slid.bs.carousel', () => {
    // Remove active from all indicators
    indicators.forEach(btn => btn.classList.remove('active'));

    // Find the index of the active item
    const activeItem = carousel.querySelector('.carousel-item.active');
    const activeIndex = Array.from(items).indexOf(activeItem);

    // Add active to the correct indicator button
    if (indicators[activeIndex]) {
      indicators[activeIndex].classList.add('active');
    }
  });
});
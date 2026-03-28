// ─── CART QUANTITY ────────────────────────────────────────────
function updateQty(itemId, delta) {
  const input = document.getElementById('qty-' + itemId);
  if (!input) return;
  let val = parseInt(input.value) + delta;
  if (val < 1) val = 1;
  if (val > 99) val = 99;
  input.value = val;
}

function submitQtyUpdate(itemId) {
  document.getElementById('qty-form-' + itemId).submit();
}

// ─── PAYMENT OPTION SELECTION ────────────────────────────────
document.querySelectorAll('.payment-option').forEach(opt => {
  opt.addEventListener('click', function () {
    document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
    this.classList.add('selected');
    this.querySelector('input[type="radio"]').checked = true;
  });
});

// ─── AUTO-DISMISS ALERTS ─────────────────────────────────────
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(el => {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 3500);

// ─── SEARCH BAR CATEGORY ────────────────────────────────────
const searchForm = document.getElementById('nav-search-form');
if (searchForm) {
  searchForm.addEventListener('submit', function (e) {
    const q = this.querySelector('input[name="q"]').value.trim();
    if (!q) { e.preventDefault(); return; }
  });
}

// ─── STICKY NAVBAR SHADOW ────────────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  if (nav) {
    nav.style.boxShadow = window.scrollY > 10
      ? '0 4px 12px rgba(0,0,0,.4)'
      : '0 2px 8px rgba(0,0,0,.4)';
  }
});

// ─── PRODUCT IMAGE HOVER ─────────────────────────────────────
document.querySelectorAll('.product-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.querySelector('.btn-cart')?.classList.add('pulse');
  });
  card.addEventListener('mouseleave', () => {
    card.querySelector('.btn-cart')?.classList.remove('pulse');
  });
});

// ─── SMOOTH SCROLL TO TOP ─────────────────────────────────────
function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show scroll-to-top button
window.addEventListener('scroll', () => {
  const btn = document.getElementById('scroll-top-btn');
  if (btn) btn.style.display = window.scrollY > 400 ? 'block' : 'none';
});

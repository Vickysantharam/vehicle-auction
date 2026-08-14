// Notification helper
function showNotification(msg, type='success') {
  const n = document.createElement('div');
  n.className = `notification ${type}`;
  n.textContent = msg;
  document.body.appendChild(n);
  setTimeout(() => n.remove(), 4000);
}

// Login/Register card flip
function openRegister() {
  const card = document.getElementById('card');
  if (card) card.classList.add('flipped');
}
function openLogin() {
  const card = document.getElementById('card');
  if (card) card.classList.remove('flipped');
}

// Bid form AJAX
document.addEventListener('DOMContentLoaded', function() {
  const bidForm = document.getElementById('bid-form');
  if (bidForm) {
    bidForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const auctionId = this.dataset.auctionId;
      const bidAmount = document.getElementById('bid-amount').value;
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(`/bid/${auctionId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({ bid_amount: bidAmount })
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          showNotification('Bid placed successfully! $' + data.new_bid);
          document.getElementById('current-bid-display').textContent = '$' + parseFloat(data.new_bid).toLocaleString();
          document.getElementById('bid-amount').value = '';
          // Add to bid history
          const tbody = document.getElementById('bid-history-body');
          if (tbody) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>You</td><td>$${parseFloat(data.new_bid).toLocaleString()}</td><td>Just now</td>`;
            tbody.prepend(tr);
          }
        } else {
          showNotification(data.message, 'error');
        }
      })
      .catch(() => showNotification('Error placing bid', 'error'));
    });
  }

  // Post auction form AJAX
  const postForm = document.getElementById('post-auction-form');
  if (postForm) {
    postForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(this);
      fetch('/post-auction/', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            showNotification('Auction posted successfully!');
            setTimeout(() => window.location.href = '/my-auctions/', 2000);
          } else {
            showNotification(data.message || 'Error posting auction', 'error');
          }
        });
    });
  }

  // Image preview
  const imageInput = document.getElementById('image');
  if (imageInput) {
    imageInput.addEventListener('change', function(e) {
      const reader = new FileReader();
      reader.onload = function() {
        const img = document.getElementById('image-preview');
        if (img) { img.src = reader.result; img.style.display = 'block'; }
      };
      reader.readAsDataURL(e.target.files[0]);
    });
  }

  // Admin tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById(this.dataset.tab).classList.add('active');
    });
  });

  // Admin delete actions
  document.querySelectorAll('.delete-auction-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      if (!confirm('Delete this auction?')) return;
      const id = this.dataset.id;
      fetch(`/admin-panel/delete-auction/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      }).then(r => r.json()).then(d => {
        if (d.success) { this.closest('tr').remove(); showNotification('Auction deleted'); }
      });
    });
  });

  document.querySelectorAll('.delete-user-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      if (!confirm('Delete this user?')) return;
      const id = this.dataset.id;
      fetch(`/admin-panel/delete-user/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      }).then(r => r.json()).then(d => {
        if (d.success) { this.closest('tr').remove(); showNotification('User deleted'); }
      });
    });
  });

  document.querySelectorAll('.delete-bid-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      if (!confirm('Delete this bid?')) return;
      const id = this.dataset.id;
      fetch(`/admin-panel/delete-bid/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      }).then(r => r.json()).then(d => {
        if (d.success) { this.closest('tr').remove(); showNotification('Bid deleted'); }
      });
    });
  });

  document.querySelectorAll('.toggle-featured-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const id = this.dataset.id;
      fetch(`/admin-panel/toggle-featured/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
      }).then(r => r.json()).then(d => {
        if (d.success) {
          this.textContent = d.featured ? 'Unfeature' : 'Feature';
          showNotification(d.featured ? 'Marked as featured' : 'Removed from featured');
        }
      });
    });
  });

  // Auto-hide messages
  document.querySelectorAll('.messages li').forEach(li => {
    setTimeout(() => li.style.display='none', 5000);
  });

  // ScrollReveal
  if (typeof ScrollReveal !== 'undefined') {
    ScrollReveal().reveal('.logo', { duration: 800, origin: 'left', distance: '30px' });
    ScrollReveal().reveal('nav ul li', { duration: 800, origin: 'top', distance: '20px', interval: 100 });
    ScrollReveal().reveal('#hero .hero-content', { duration: 1000, origin: 'bottom', distance: '40px' });
    ScrollReveal().reveal('.auction-item', { duration: 700, origin: 'bottom', distance: '30px', interval: 100 });
    ScrollReveal().reveal('.step', { duration: 700, origin: 'bottom', distance: '30px', interval: 150 });
    ScrollReveal().reveal('.testimonial', { duration: 700, origin: 'bottom', distance: '30px', interval: 150 });
    ScrollReveal().reveal('.stat-card', { duration: 600, origin: 'bottom', distance: '20px', interval: 100 });
  }
});

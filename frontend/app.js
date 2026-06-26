const API = 'http://localhost:8001';

// CARRINHO — carrega do localStorage ao iniciar
let cart = JSON.parse(localStorage.getItem('drop_cart') || '[]');

function saveCart() {
  localStorage.setItem('drop_cart', JSON.stringify(cart));
}

// PRODUTOS
async function loadProducts() {
  const grid = document.getElementById('produtosGrid');
  try {
    const res = await fetch(`${API}/products/`);
    const products = await res.json();
    if (!products.length) { grid.innerHTML = '<p class="loading">Nenhum produto ainda.</p>'; return; }
    grid.innerHTML = products.map(p => `
      <div class="card" onclick="openModal(${JSON.stringify(p).replace(/"/g, '&quot;')})">
        <div class="card-image">
          ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}"/>` : `<div class="card-img-placeholder">DRØP</div>`}
        </div>
        <div class="card-info">
          <p class="card-name">${p.name}</p>
          <p class="card-price">R$ ${p.price.toFixed(2).replace('.', ',')}</p>
          <button class="card-add" onclick="event.stopPropagation(); openModal(${JSON.stringify(p).replace(/"/g, '&quot;')})">ADD TO BAG</button>
        </div>
      </div>
    `).join('');
  } catch (e) {
    grid.innerHTML = '<p class="loading">Erro ao carregar produtos.</p>';
  }
}

// MODAL
function openModal(p) {
  const imgSrc = p.image_product || p.image_url;
  const imgWrap = document.getElementById('modalImage');
  imgWrap.innerHTML = imgSrc
    ? `<img src="${imgSrc}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;"/>`
    : `<div class="modal-placeholder"></div>`;

  document.getElementById('modalName').textContent = p.name;
  document.getElementById('modalDesc').textContent = p.description;
  document.getElementById('modalPrice').textContent = `R$ ${p.price.toFixed(2).replace('.', ',')}`;
  document.getElementById('modalStock').textContent = `${p.stock} unidades disponíveis`;

  const sizesWrap = document.getElementById('modalSizes');
  const hint = document.getElementById('modalSizeHint');
  const addBtn = document.getElementById('modalAdd');
  let selectedSize = null;

  if (p.sizes && p.sizes.length > 0) {
    sizesWrap.innerHTML = p.sizes.map(s => `
      <button class="size-btn" data-size="${s}">${s}</button>
    `).join('');

    sizesWrap.querySelectorAll('.size-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sizesWrap.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedSize = btn.dataset.size;
        hint.textContent = `Tamanho: ${selectedSize}`;
        addBtn.disabled = false;
      });
    });

    addBtn.disabled = true;
    hint.textContent = 'Selecione um tamanho';
  } else {
    sizesWrap.innerHTML = '';
    hint.textContent = '';
    addBtn.disabled = false;
    selectedSize = 'ÚNICO';
  }

  addBtn.onclick = () => {
    addToCart(p, selectedSize);
    closeModal();
  };

  document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() { document.getElementById('modalOverlay').classList.remove('active'); }
document.getElementById('modalClose').onclick = closeModal;
document.getElementById('modalOverlay').onclick = (e) => { if (e.target === e.currentTarget) closeModal(); };

// CARRINHO
function addToCart(p, size) {
  const key = `${p.id}_${size}`;
  const existing = cart.find(i => i._key === key);
  if (existing) {
    existing.qty++;
    existing.quantity = existing.qty;
  } else {
    cart.push({
  ...p,
  image: p.image_url || p.image_product || '',  // ← adiciona isso
  qty: 1,
  quantity: 1,
  size,
  _key: key
});
  }
  saveCart();
  updateCart();
  openCart();
}

function updateCart() {
  const count = cart.reduce((s, i) => s + i.qty, 0);
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  document.getElementById('cartCount').textContent = count;
  document.getElementById('cartTotal').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
  document.getElementById('cartItems').innerHTML = cart.length ? cart.map(i => `
    <div class="cart-item">
      <div class="cart-item-info">
        <p class="cart-item-name">${i.name}${i.size && i.size !== 'ÚNICO' ? ` <span style="font-weight:400;color:#aaa">/ ${i.size}</span>` : ''}</p>
        <p class="cart-item-price">R$ ${(i.price * i.qty).toFixed(2).replace('.', ',')}</p>
      </div>
      <div class="cart-item-controls">
        <button onclick="changeQty('${i._key}', -1)">−</button>
        <span>${i.qty}</span>
        <button onclick="changeQty('${i._key}', 1)">+</button>
      </div>
    </div>
  `).join('') : '<p style="color:#999;font-size:.85rem;letter-spacing:2px;">Seu bag está vazio.</p>';
}

function changeQty(key, delta) {
  const item = cart.find(i => i._key === key);
  if (!item) return;
  item.qty += delta;
  item.quantity = item.qty;
  if (item.qty <= 0) cart = cart.filter(i => i._key !== key);
  saveCart();
  updateCart();
}

function openCart() {
  document.getElementById('cart').classList.add('active');
  document.getElementById('cartOverlay').classList.add('active');
}

function closeCart() {
  document.getElementById('cart').classList.remove('active');
  document.getElementById('cartOverlay').classList.remove('active');
}

document.getElementById('cartBtn').onclick = openCart;
document.getElementById('closeCart').onclick = closeCart;
document.getElementById('cartOverlay').onclick = closeCart;

// CHECKOUT
document.getElementById('checkoutBtn').onclick = () => {
  if (!cart.length) return;
  closeCart();
  window.location.href = 'checkout.html';
};

// Sincroniza UI com carrinho salvo ao carregar a página
updateCart();
loadProducts();
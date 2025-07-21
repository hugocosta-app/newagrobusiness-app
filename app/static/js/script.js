// New Agro Business - JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.classList.contains('show')) {
                alert.classList.remove('show');
                alert.classList.add('fade');
                setTimeout(function() {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processando...';
            }
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = button.getAttribute('data-confirm') || 'Tem certeza que deseja excluir?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[data-currency]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            let value = input.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            input.value = value;
        });
    });

    // Product search functionality (if exists)
    const productSearch = document.getElementById('product-search');
    if (productSearch) {
        let searchTimeout;
        productSearch.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value;
            
            if (query.length < 2) {
                document.getElementById('search-results').innerHTML = '';
                return;
            }
            
            searchTimeout = setTimeout(function() {
                fetch(`/orders/search_products?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        const resultsDiv = document.getElementById('search-results');
                        resultsDiv.innerHTML = '';
                        
                        data.forEach(function(product) {
                            const item = document.createElement('div');
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">${product.name}</h6>
                                    <small>R$ ${product.price.toFixed(2)}</small>
                                </div>
                            `;
                            item.addEventListener('click', function() {
                                addProductToOrder(product);
                                resultsDiv.innerHTML = '';
                                productSearch.value = '';
                            });
                            resultsDiv.appendChild(item);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            }, 300);
        });
    }
});

// Function to add product to order (if needed)
function addProductToOrder(product) {
    // This would be implemented based on the order form structure
    console.log('Adding product to order:', product);
}

// Function to format numbers as currency
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}


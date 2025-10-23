// Custom JavaScript for Flask Forms Demo

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask Forms Demo loaded successfully!');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Show file info
                const fileInfo = document.createElement('div');
                fileInfo.className = 'form-text';
                fileInfo.innerHTML = `
                    <strong>Selected file:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${(file.size / 1024).toFixed(1)} KB<br>
                    <strong>Type:</strong> ${file.type}
                `;
                
                // Remove existing file info
                const existingInfo = input.parentNode.querySelector('.file-info');
                if (existingInfo) {
                    existingInfo.remove();
                }
                
                fileInfo.className += ' file-info';
                input.parentNode.appendChild(fileInfo);
            }
        });
    });
    
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            
            // Remove existing strength indicator
            const existingIndicator = this.parentNode.querySelector('.password-strength');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            if (password.length > 0) {
                const indicator = document.createElement('div');
                indicator.className = 'password-strength form-text';
                indicator.innerHTML = `
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar ${strength.class}" role="progressbar" 
                             style="width: ${strength.percentage}%"></div>
                    </div>
                    <small>${strength.text}</small>
                `;
                this.parentNode.appendChild(indicator);
            }
        });
    });
    
    // Real-time form validation
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            // Clear validation state on input
            this.classList.remove('is-valid', 'is-invalid');
        });
    });
    
    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'form-text text-end';
            counter.innerHTML = `<span class="char-count">0</span>/${maxLength} characters`;
            
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                const count = this.value.length;
                const charCount = this.parentNode.querySelector('.char-count');
                charCount.textContent = count;
                
                if (count > maxLength * 0.9) {
                    charCount.classList.add('text-warning');
                } else {
                    charCount.classList.remove('text-warning');
                }
            });
        }
    });
    
    // Form submission loading state
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
                this.disabled = true;
                form.classList.add('form-loading');
            }
        });
    });
    
    // Dynamic form field management
    const addItemButtons = document.querySelectorAll('#add-item');
    addItemButtons.forEach(button => {
        button.addEventListener('click', function() {
            const container = document.getElementById('items-container');
            const fieldCount = container.children.length;
            
            if (fieldCount < 10) {
                const newField = document.createElement('div');
                newField.className = 'input-group mb-2 item-field';
                newField.innerHTML = `
                    <input type="text" class="form-control" name="items" placeholder="Enter item">
                    <button type="button" class="btn btn-outline-danger remove-item">Remove</button>
                `;
                container.appendChild(newField);
                
                if (fieldCount >= 9) {
                    this.disabled = true;
                }
            }
        });
    });
    
    // Remove item functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const container = document.getElementById('items-container');
            if (container.children.length > 1) {
                e.target.parentElement.remove();
                document.getElementById('add-item').disabled = false;
            } else {
                alert('At least one item is required');
            }
        }
    });
    
    // Search form enhancement
    const searchForms = document.querySelectorAll('form[action*="search"]');
    searchForms.forEach(form => {
        const queryInput = form.querySelector('input[name="query"]');
        if (queryInput) {
            queryInput.addEventListener('input', function() {
                // Debounce search
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    // Could implement live search here
                }, 300);
            });
        }
    });
    
    // Console logging for debugging
    console.log('All JavaScript functionality initialized');
});

// Password strength calculation
function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = [];
    
    if (password.length >= 8) score += 1;
    else feedback.push('at least 8 characters');
    
    if (/[a-z]/.test(password)) score += 1;
    else feedback.push('lowercase letters');
    
    if (/[A-Z]/.test(password)) score += 1;
    else feedback.push('uppercase letters');
    
    if (/[0-9]/.test(password)) score += 1;
    else feedback.push('numbers');
    
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    else feedback.push('special characters');
    
    const strength = {
        0: { class: 'bg-danger', percentage: 20, text: 'Very Weak' },
        1: { class: 'bg-danger', percentage: 40, text: 'Weak' },
        2: { class: 'bg-warning', percentage: 60, text: 'Fair' },
        3: { class: 'bg-info', percentage: 80, text: 'Good' },
        4: { class: 'bg-success', percentage: 100, text: 'Strong' },
        5: { class: 'bg-success', percentage: 100, text: 'Very Strong' }
    };
    
    return strength[score] || strength[0];
}

// Field validation
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    
    // Clear previous validation
    field.classList.remove('is-valid', 'is-invalid');
    
    // Basic validation rules
    if (field.hasAttribute('required') && !value) {
        field.classList.add('is-invalid');
        return false;
    }
    
    // Email validation
    if (fieldName === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    // Password validation
    if (fieldName === 'password' && value) {
        if (value.length < 8) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    // If we get here, field is valid
    if (value) {
        field.classList.add('is-valid');
    }
    
    return true;
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Export functions for global use
window.FlaskFormsDemo = {
    showNotification: showNotification,
    validateField: validateField,
    calculatePasswordStrength: calculatePasswordStrength
};

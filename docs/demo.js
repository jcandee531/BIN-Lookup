// Mock BIN data for demonstration
const MOCK_BIN_DATA = {
    "545454": {
        "issuerName": "Chase Bank",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "MASTERCARD",
        "lowAccountRange": "5454540000000000",
        "highAccountRange": "5454549999999999",
        "issuerCountry": "United States",
        "productSubType": "STANDARD"
    },
    "515555": {
        "issuerName": "Citibank",
        "countryCode": "US", 
        "productType": "CREDIT",
        "cardType": "MASTERCARD",
        "lowAccountRange": "5155550000000000",
        "highAccountRange": "5155559999999999",
        "issuerCountry": "United States",
        "productSubType": "WORLD"
    },
    "555555": {
        "issuerName": "Bank of America",
        "countryCode": "US",
        "productType": "CREDIT", 
        "cardType": "MASTERCARD",
        "lowAccountRange": "5555550000000000",
        "highAccountRange": "5555559999999999",
        "issuerCountry": "United States",
        "productSubType": "PLATINUM"
    },
    "424242": {
        "issuerName": "HSBC Bank",
        "countryCode": "GB",
        "productType": "DEBIT",
        "cardType": "VISA",
        "lowAccountRange": "4242420000000000", 
        "highAccountRange": "4242429999999999",
        "issuerCountry": "United Kingdom",
        "productSubType": "CLASSIC"
    },
    "411111": {
        "issuerName": "Wells Fargo",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "VISA",
        "lowAccountRange": "4111110000000000",
        "highAccountRange": "4111119999999999", 
        "issuerCountry": "United States",
        "productSubType": "SIGNATURE"
    },
    "378282": {
        "issuerName": "American Express",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "AMERICAN EXPRESS",
        "lowAccountRange": "378282000000000",
        "highAccountRange": "378282999999999",
        "issuerCountry": "United States",
        "productSubType": "GOLD"
    }
};

// Mock account ranges data
const MOCK_ACCOUNT_RANGES = [
    {
        "lowAccountRange": "5454540000000000",
        "highAccountRange": "5454549999999999", 
        "issuerName": "Chase Bank",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5155550000000000",
        "highAccountRange": "5155559999999999",
        "issuerName": "Citibank", 
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5555550000000000",
        "highAccountRange": "5555559999999999",
        "issuerName": "Bank of America",
        "countryCode": "US", 
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "4242420000000000",
        "highAccountRange": "4242429999999999",
        "issuerName": "HSBC Bank",
        "countryCode": "GB",
        "productType": "DEBIT"
    },
    {
        "lowAccountRange": "4111110000000000", 
        "highAccountRange": "4111119999999999",
        "issuerName": "Wells Fargo",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "378282000000000",
        "highAccountRange": "378282999999999",
        "issuerName": "American Express",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "6011000000000000",
        "highAccountRange": "6011999999999999", 
        "issuerName": "Discover Bank",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5432100000000000",
        "highAccountRange": "5432109999999999",
        "issuerName": "Capital One",
        "countryCode": "US",
        "productType": "CREDIT"
    }
];

// Utility functions
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showAlert(message, type = 'danger') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'exclamation-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function formatCardNumber(number) {
    if (!number) return '';
    return number.replace(/(\d{4})(?=\d)/g, '$1 ');
}

// Simulate API delay
function simulateApiDelay(min = 500, max = 1500) {
    return new Promise(resolve => {
        const delay = Math.random() * (max - min) + min;
        setTimeout(resolve, delay);
    });
}

// BIN input formatting and validation
document.getElementById('binNumber').addEventListener('input', function(e) {
    // Only allow digits
    this.value = this.value.replace(/[^0-9]/g, '');
    
    // Add visual feedback
    if (this.value.length >= 6) {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    } else {
        this.classList.remove('is-valid');
        if (this.value.length > 0) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
        }
    }
});

// Fill BIN number from sample buttons
function fillBIN(binNumber) {
    document.getElementById('binNumber').value = binNumber;
    document.getElementById('binNumber').dispatchEvent(new Event('input'));
}

// BIN Lookup Form Handler
document.getElementById('binLookupForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const binNumber = document.getElementById('binNumber').value.trim();
    
    if (!binNumber || binNumber.length < 6) {
        showAlert('Please enter a valid BIN number (6-8 digits)', 'warning');
        return;
    }

    showLoading();
    
    try {
        // Simulate API call delay
        await simulateApiDelay();
        
        // Get mock data
        const cleanBin = binNumber.substring(0, 6);
        let data;
        
        if (MOCK_BIN_DATA[cleanBin]) {
            data = MOCK_BIN_DATA[cleanBin];
        } else {
            // Generate mock data for unknown BINs
            const countries = ["US", "GB", "CA", "DE", "FR", "JP", "AU"];
            const productTypes = ["CREDIT", "DEBIT", "PREPAID"];
            const cardTypes = ["MASTERCARD", "VISA", "AMERICAN EXPRESS"];
            
            data = {
                "issuerName": `Demo Bank ${cleanBin.substring(0, 3)}`,
                "countryCode": countries[Math.floor(Math.random() * countries.length)],
                "productType": productTypes[Math.floor(Math.random() * productTypes.length)],
                "cardType": cardTypes[Math.floor(Math.random() * cardTypes.length)],
                "lowAccountRange": cleanBin + "0".repeat(16 - cleanBin.length),
                "highAccountRange": cleanBin + "9".repeat(16 - cleanBin.length),
                "issuerCountry": "Demo Country",
                "productSubType": "STANDARD"
            };
        }

        displayBINResults({
            success: true,
            data: data,
            bin_number: cleanBin,
            demo_mode: true
        });
        
        showAlert('BIN lookup completed successfully!', 'success');
        
    } catch (error) {
        showAlert('Demo error: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
});

// Display BIN lookup results
function displayBINResults(response) {
    const container = document.getElementById('resultsContainer');
    const data = response.data;

    let html = `
        <div class="card mt-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    BIN Information for ${formatCardNumber(response.bin_number)}
                </h5>
                ${response.demo_mode ? '<small class="d-block mt-1"><i class="fas fa-flask me-1"></i>Demo Data</small>' : ''}
            </div>
            <div class="card-body">
    `;

    if (data && Object.keys(data).length > 0) {
        html += '<div class="row">';
        
        // Display key information
        const fields = [
            { key: 'issuerName', label: 'Issuer', icon: 'fas fa-university' },
            { key: 'countryCode', label: 'Country', icon: 'fas fa-flag' },
            { key: 'productType', label: 'Product Type', icon: 'fas fa-credit-card' },
            { key: 'cardType', label: 'Card Type', icon: 'fas fa-tags' },
            { key: 'lowAccountRange', label: 'Low Range', icon: 'fas fa-sort-numeric-down' },
            { key: 'highAccountRange', label: 'High Range', icon: 'fas fa-sort-numeric-up' }
        ];

        fields.forEach(field => {
            if (data[field.key]) {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="d-flex align-items-center">
                            <i class="${field.icon} text-primary me-3 fa-lg"></i>
                            <div>
                                <small class="text-muted">${field.label}</small>
                                <div class="fw-semibold">${field.key.includes('Range') ? formatCardNumber(data[field.key]) : data[field.key]}</div>
                            </div>
                        </div>
                    </div>
                `;
            }
        });

        html += '</div>';

        // Display raw JSON for developers
        html += `
            <div class="mt-4">
                <button class="btn btn-outline-secondary btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#rawData">
                    <i class="fas fa-code me-2"></i>
                    Show Raw Data
                </button>
                <div class="collapse mt-3" id="rawData">
                    <pre class="bg-light p-3 rounded"><code>${JSON.stringify(data, null, 2)}</code></pre>
                </div>
            </div>
        `;
    } else {
        html += `
            <div class="text-center py-4">
                <i class="fas fa-exclamation-triangle text-warning fa-3x mb-3"></i>
                <h5>No Data Found</h5>
                <p class="text-muted">No information available for this BIN number.</p>
            </div>
        `;
    }

    html += '</div></div>';
    
    container.innerHTML = html;
    container.style.display = 'block';
    
    // Scroll to results
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Load Account Ranges
async function loadAccountRanges() {
    showLoading();
    
    try {
        await simulateApiDelay(300, 800);
        
        const data = {
            content: MOCK_ACCOUNT_RANGES.slice(0, 8),
            totalElements: MOCK_ACCOUNT_RANGES.length,
            totalPages: Math.ceil(MOCK_ACCOUNT_RANGES.length / 8),
            number: 0,
            numberOfElements: Math.min(8, MOCK_ACCOUNT_RANGES.length),
            first: true,
            last: MOCK_ACCOUNT_RANGES.length <= 8
        };
        
        displayAccountRanges(data);
        showAlert('Account ranges loaded successfully!', 'success');
        
    } catch (error) {
        showAlert('Failed to load account ranges: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// Display Account Ranges
function displayAccountRanges(data) {
    const container = document.getElementById('accountRangesContainer');
    
    if (!data || !data.content || data.content.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-inbox text-muted fa-3x mb-3"></i>
                <h6>No Account Ranges Found</h6>
                <p class="text-muted">No account range data available.</p>
            </div>
        `;
        return;
    }

    let html = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr>
                        <th><i class="fas fa-sort-numeric-down me-1"></i>Low Range</th>
                        <th><i class="fas fa-sort-numeric-up me-1"></i>High Range</th>
                        <th><i class="fas fa-university me-1"></i>Issuer</th>
                        <th><i class="fas fa-flag me-1"></i>Country</th>
                        <th><i class="fas fa-credit-card me-1"></i>Type</th>
                    </tr>
                </thead>
                <tbody>
    `;

    data.content.forEach(range => {
        html += `
            <tr>
                <td><code class="text-primary">${formatCardNumber(range.lowAccountRange || 'N/A')}</code></td>
                <td><code class="text-primary">${formatCardNumber(range.highAccountRange || 'N/A')}</code></td>
                <td>
                    <i class="fas fa-university text-muted me-2"></i>
                    ${range.issuerName || 'N/A'}
                </td>
                <td>
                    <i class="fas fa-flag text-muted me-2"></i>
                    ${range.countryCode || 'N/A'}
                </td>
                <td>
                    <span class="badge bg-primary">
                        <i class="fas fa-credit-card me-1"></i>
                        ${range.productType || 'N/A'}
                    </span>
                </td>
            </tr>
        `;
    });

    html += `
                </tbody>
            </table>
        </div>
    `;

    // Add pagination info
    if (data.totalElements) {
        html += `
            <div class="d-flex justify-content-between align-items-center mt-3">
                <small class="text-muted">
                    <i class="fas fa-info-circle me-1"></i>
                    Showing ${data.numberOfElements} of ${data.totalElements} results
                </small>
                <small class="text-muted">
                    <i class="fas fa-file-alt me-1"></i>
                    Page ${data.number + 1} of ${data.totalPages}
                </small>
            </div>
        `;
    }

    container.innerHTML = html;
}

// Search Form Handler
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const issuerName = document.getElementById('issuerName').value.trim().toLowerCase();
    const countryCode = document.getElementById('countryCode').value.trim().toUpperCase();
    const productType = document.getElementById('productType').value.toUpperCase();

    if (!issuerName && !countryCode && !productType) {
        showAlert('Please enter at least one search criteria', 'warning');
        return;
    }

    showLoading();
    
    try {
        await simulateApiDelay(400, 1000);
        
        // Filter mock data
        const filteredRanges = MOCK_ACCOUNT_RANGES.filter(range => {
            let match = true;
            
            if (issuerName && !range.issuerName.toLowerCase().includes(issuerName)) {
                match = false;
            }
            
            if (countryCode && countryCode !== range.countryCode) {
                match = false;
            }
                
            if (productType && productType !== range.productType) {
                match = false;
            }
            
            return match;
        });

        const data = {
            content: filteredRanges.slice(0, 10),
            totalElements: filteredRanges.length,
            totalPages: Math.ceil(filteredRanges.length / 10),
            number: 0,
            numberOfElements: Math.min(10, filteredRanges.length),
            first: true,
            last: filteredRanges.length <= 10
        };
        
        displaySearchResults(data);
        
        if (filteredRanges.length > 0) {
            showAlert(`Found ${filteredRanges.length} matching results!`, 'success');
        } else {
            showAlert('No results found for your search criteria', 'info');
        }
        
    } catch (error) {
        showAlert('Search failed: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
});

// Display Search Results
function displaySearchResults(data) {
    const container = document.getElementById('searchResultsContainer');
    
    if (!data || !data.content || data.content.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-search me-2"></i>
                No results found for your search criteria.
            </div>
        `;
        container.style.display = 'block';
        return;
    }

    let html = `
        <h6 class="mb-3">
            <i class="fas fa-search-plus me-2"></i>
            Search Results (${data.totalElements} found)
        </h6>
        <div class="row">
    `;

    data.content.forEach(result => {
        html += `
            <div class="col-md-6 mb-3">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <h6 class="card-title">
                            <i class="fas fa-university text-primary me-2"></i>
                            ${result.issuerName || 'Unknown Issuer'}
                        </h6>
                        <p class="card-text">
                            <small class="text-muted">Range:</small><br>
                            <code class="text-primary">${formatCardNumber(result.lowAccountRange)}</code><br>
                            <code class="text-primary">${formatCardNumber(result.highAccountRange)}</code>
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-secondary">
                                <i class="fas fa-flag me-1"></i>
                                ${result.countryCode || 'N/A'}
                            </span>
                            <span class="badge bg-primary">
                                <i class="fas fa-credit-card me-1"></i>
                                ${result.productType || 'N/A'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    
    container.innerHTML = html;
    container.style.display = 'block';
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize demo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎉 Mastercard BIN Lookup Demo Loaded!');
    console.log('📱 Try the sample BINs: 545454, 515555, 555555, 424242, 411111, 378282');
    
    // Show welcome message
    setTimeout(() => {
        showAlert('Welcome to the BIN Lookup Demo! Try entering a sample BIN number.', 'info');
    }, 1000);
});
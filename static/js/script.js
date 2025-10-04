const priceEl = document.getElementById('price');
const signalEl = document.getElementById('signal');
const lastUpdatedEl = document.getElementById('lastUpdated');
// ctx کو یہاں سے ہٹا دیں – اب یہ global نہیں رہے گا، local ہو جائے گا

let chart;

async function fetchData() {
    // Loading state
    if (priceEl) priceEl.textContent = 'Fetching...';
    if (signalEl) signalEl.textContent = 'Loading...';

    try {
        const res = await fetch('/api/data');
        if (!res.ok) throw new Error(`HTTP ${res.status}: Server error`);
        const data = await res.json();

        if (data.error) throw new Error(data.details || data.error);

        // Update price with flash
        if (data.price) {
            if (priceEl) {
                priceEl.textContent = `$${parseFloat(data.price).toLocaleString()}`;
                priceEl.classList.add('flash');
                setTimeout(() => priceEl.classList.remove('flash'), 700);
            }
        }

        // Update signal (map backend to UI)
        if (data.signal && signalEl) {
            let displaySignal = '';
            let signalClass = 'neutral'; // Default for HOLD
            switch (data.signal.toUpperCase()) {
                case 'LONG':
                    displaySignal = 'Long (Buy Signal)';
                    signalClass = 'buy';
                    break;
                case 'SHORT':
                    displaySignal = 'Short (Sell Signal)';
                    signalClass = 'sell';
                    break;
                case 'HOLD':
                    displaySignal = 'Hold (Neutral)';
                    signalClass = 'neutral';
                    break;
                default:
                    displaySignal = 'Unknown Signal';
            }
            signalEl.textContent = displaySignal;
            signalEl.className = `value ${signalClass}`;
        }

        // Update indicators (if element exists)
        const indicatorsEl = document.getElementById('indicators');
        if (indicatorsEl && data.rsi !== undefined) {
            indicatorsEl.innerHTML = `
                <small class="text-muted">
                    RSI: ${data.rsi || 'N/A'} | 
                    EMA Short: $${data.ema_short?.toLocaleString() || 'N/A'} | 
                    EMA Long: $${data.ema_long?.toLocaleString() || 'N/A'}
                </small>
            `;
        }

        // Update chart (use 'labels' from backend as 'timestamps')
        if (data.labels && data.prices) {
            updateChart(data.labels, data.prices, data.ema_short_series, data.ema_long_series);
        }

        // Update time
        if (lastUpdatedEl) {
            const now = new Date().toLocaleTimeString();
            lastUpdatedEl.textContent = now;
        }

        console.log('✅ Data updated successfully');
    } catch (err) {
        console.error('API error:', err);
        if (signalEl) signalEl.textContent = `Error: ${err.message}`;
        if (priceEl) priceEl.textContent = '$0.00 (Retry)';
        // Auto-retry after 10s on error
        setTimeout(fetchData, 10000);
    }
}

function updateChart(labels, prices, emaShort = [], emaLong = []) {
    // ctx اب یہاں سے global یا passed ہو، مگر پہلے چیک کریں
    const canvas = document.getElementById('priceChart');
    if (!canvas) {
        console.error('Canvas element not found!');
        return;
    }
    const ctx = canvas.getContext('2d'); // اب یہاں declare کریں

    if (chart) {
        // Update existing chart (efficient)
        chart.data.labels = labels;
        chart.data.datasets[0].data = prices;
        if (emaShort.length > 0) {
            if (chart.data.datasets.length < 3) {
                // Add EMA datasets if not present
                chart.data.datasets.push({
                    label: 'EMA Short (9)',
                    data: emaShort,
                    borderColor: 'green',
                    borderWidth: 1.5,
                    tension: 0.3,
                    fill: false,
                    pointRadius: 0
                });
                chart.data.datasets.push({
                    label: 'EMA Long (26)',
                    data: emaLong,
                    borderColor: 'orange',
                    borderWidth: 1.5,
                    tension: 0.3,
                    fill: false,
                    pointRadius: 0
                });
            } else {
                chart.data.datasets[1].data = emaShort;
                chart.data.datasets[2].data = emaLong;
            }
        }
        chart.update('none'); // Fast update
        return;
    }

    // Create new chart
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'BTC Price (USD)',
                data: prices,
                borderColor: '#00ffff',
                borderWidth: 2,
                tension: 0.3,
                fill: true,
                backgroundColor: 'rgba(0,255,255,0.1)',
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true, // Show legend for EMAs
                    labels: { color: '#00ffff' }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#00ffff' },
                    grid: { color: '#1f2937' }
                },
                y: {
                    ticks: {
                        color: '#00ffff',
                        callback: value => '$' + value.toLocaleString()
                    },
                    grid: { color: '#1f2937' }
                }
            },
            interaction: { intersect: false, mode: 'index' } // Better tooltip
        }
    });

    // Add EMA datasets after creation if available
    if (emaShort.length > 0) {
        chart.data.datasets.push({
            label: 'EMA Short (9)',
            data: emaShort,
            borderColor: 'green',
            borderWidth: 1.5,
            tension: 0.3,
            fill: false,
            pointRadius: 0
        });
        chart.data.datasets.push({
            label: 'EMA Long (26)',
            data: emaLong,
            borderColor: 'orange',
            borderWidth: 1.5,
            tension: 0.3,
            fill: false,
            pointRadius: 0
        });
        chart.update();
    }
}

// Init – یہاں ctx کی ضرورت نہیں، بس fetchData کال کریں
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Crypto Signal Tool...');

    // اب یہاں canvas چیک کریں (اختیاری، مگر اچھا practice)
    const canvas = document.getElementById('priceChart');
    if (!canvas) {
        console.error('Canvas element not found! Check HTML ID.');
    }

    fetchData();
    setInterval(fetchData, 30000); // Refresh every 30s
});
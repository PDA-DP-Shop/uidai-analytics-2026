const REFRESH_INTERVAL = 1000; // 1 Second
let charts = {}; // Store chart instances to update them

document.addEventListener('DOMContentLoaded', () => {
    // Initial Fetch
    fetchData();
    // Start Polling
    setInterval(fetchData, REFRESH_INTERVAL);
});

async function fetchData() {
    try {
        // Fetch from the live API
        const response = await fetch('/api/stats');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateDashboard(data) {
    // KPI Updates
    document.getElementById('totalRecords').innerText = data.summary.total_records.toLocaleString();
    document.getElementById('successRate').innerText = data.summary.success_rate + '%';
    document.getElementById('anomalyCount').innerText = data.anomalies.length;
    document.getElementById('lastUpdated').innerText = 'Last Updated: ' + data.summary.last_updated;

    // Charts
    renderTrendChart(data.monthly_trends);
    renderStatusChart(data.status_distribution);
    renderStateChart(data.state_wise_enrollment);

    // Anomaly Table
    renderAnomalyTable(data.anomalies);
}

function renderTrendChart(trends) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    const labels = Object.keys(trends);
    const data = Object.values(trends);

    if (charts['trend']) {
        charts['trend'].data.labels = labels;
        charts['trend'].data.datasets[0].data = data;
        charts['trend'].update('none'); // Update without animation reset
    } else {
        charts['trend'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Enrollments',
                    data: data,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                animation: { duration: 0 },
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}

function renderStatusChart(statusData) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    const labels = Object.keys(statusData);
    const data = Object.values(statusData);

    if (charts['status']) {
        charts['status'].data.labels = labels;
        charts['status'].data.datasets[0].data = data;
        charts['status'].update('none');
    } else {
        charts['status'] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#10b981', '#ef4444', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: {
                animation: { duration: 0 },
                plugins: {
                    legend: { position: 'right', labels: { color: '#94a3b8' } }
                }
            }
        });
    }
}

function renderStateChart(stateData) {
    const ctx = document.getElementById('stateChart').getContext('2d');
    const labels = Object.keys(stateData);
    const data = Object.values(stateData);

    if (charts['state']) {
        charts['state'].data.labels = labels;
        charts['state'].data.datasets[0].data = data;
        charts['state'].update('none');
    } else {
        charts['state'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Enrollments',
                    data: data,
                    backgroundColor: '#6366f1',
                    borderRadius: 4
                }]
            },
            options: {
                animation: { duration: 0 },
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}

function renderAnomalyTable(anomalies) {
    const tbody = document.querySelector('#anomalyTable tbody');
    // Change Header if needed (optional dynamic update)
    document.querySelector('#anomalyTable thead tr').innerHTML = `
        <th>State</th>
        <th>District</th>
        <th>Status</th>
        <th>Alert Type</th>
        <th>ML Confidence (%)</th>
    `;

    tbody.innerHTML = '';

    anomalies.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.State}</td>
            <td>${item.District}</td>
            <td>${item.total}</td>
            <td style="color: #ef4444;">${item.rejected}</td>
            <td style="font-weight:bold; color: #ef4444;">${item.rejection_rate}%</td>
        `;
        tbody.appendChild(row);
    });

    if (anomalies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Scanning for anomalies...</td></tr>';
    }
}

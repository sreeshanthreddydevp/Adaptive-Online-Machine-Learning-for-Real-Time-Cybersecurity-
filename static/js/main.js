/**
 * ==========================================================================
 * CYBER-ML CORE INTERACTIVE TELEMETRY INTERACTION SCRIPT
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", function () {
    // --- FORM VIEW MANAGEMENT INTERACTION ---
    window.showForm = function (formType) {
        const offlineForm = document.getElementById('offlineForm');
        const onlineForm = document.getElementById('onlineForm');
        const offlineBtn = document.getElementById('toggle-offline-btn');
        const onlineBtn = document.getElementById('toggle-online-btn');

        if (formType === 'offline') {
            offlineForm.classList.remove('d-none');
            onlineForm.classList.add('d-none');
            offlineBtn.classList.add('active');
            onlineBtn.classList.remove('active');
        } else {
            offlineForm.classList.add('d-none');
            onlineForm.classList.remove('d-none');
            offlineBtn.classList.remove('active');
            onlineBtn.classList.add('active');
        }
    };

    // --- DASHBOARD REALTIME DATA SIMULATION FRAMEWORK ---
    const threatLvlText = document.getElementById('threat-lvl');
    const threatBar = document.getElementById('threat-bar');
    const packetCounter = document.getElementById('packet-counter');

    if (threatLvlText && packetCounter) {
        setInterval(() => {
            // Generate stochastic variations for cybersecurity aesthetics
            let generatedThreat = (Math.random() * 4).toFixed(2);
            let packetRate = Math.floor(4000 + Math.random() * 1500);

            threatLvlText.innerText = `${generatedThreat}%`;
            threatBar.style.width = `${generatedThreat * 20}%`;
            packetCounter.innerText = packetRate.toLocaleString();
        }, 2500);
    }

    // --- CHART.JS ENTERPRISE ENGINE INITIALIZATION ---
    const socCtxLine = document.getElementById('socLineChart');
    if (socCtxLine) {
        new Chart(socCtxLine.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                datasets: [{
                    label: 'Analyzed Vectors (k)',
                    data: [32, 45, 61, 52, 78, 92],
                    borderColor: '#00f0ff',
                    backgroundColor: 'rgba(0, 240, 255, 0.05)',
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Blocked Anomalies',
                    data: [1, 4, 12, 5, 22, 18],
                    borderColor: '#ff0055',
                    backgroundColor: 'rgba(ff, 0, 55, 0.05)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#fff' } } },
                scales: {
                    x: { ticks: { color: '#9ca3af' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#9ca3af' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }

    const socCtxRadar = document.getElementById('socRadarChart');
    if (socCtxRadar) {
        new Chart(socCtxRadar.getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['DDM Sensitivity', 'EDDM Distance', 'F1 Balance', 'Accuracy Profile', 'Latency Ceiling'],
                datasets: [{
                    label: 'Passive-Aggressive Classifier',
                    data: [85, 90, 88, 94, 99],
                    borderColor: '#bd00ff',
                    backgroundColor: 'rgba(189, 0, 255, 0.2)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#fff' } } },
                scales: {
                    r: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        pointLabels: { color: '#9ca3af' },
                        ticks: { display: false }
                    }
                }
            }
        });
    }
});
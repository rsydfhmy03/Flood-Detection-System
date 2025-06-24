// Fuzzy Manual Calculator JavaScript
// File: static/js/fuzzy_manual.js

// Global variables
let chartData = {};

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Get chart data from template
    if (typeof window.chartData !== 'undefined') {
        chartData = window.chartData;
        initMembershipCharts();
    }
});

// Set input values from quick examples
function setInput(ketinggian, curahHujan) {
    document.getElementById('ketinggian').value = ketinggian;
    document.getElementById('curah_hujan').value = curahHujan;
}

// Show/Hide loading
function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

// Get status color helper
function getStatusColor(status) {
    const colors = {
        'Aman': {
            bg: 'bg-green-50',
            border: 'border-green-200',
            text: 'text-green-900',
            textLight: 'text-green-600'
        },
        'Siaga': {
            bg: 'bg-yellow-50',
            border: 'border-yellow-200',
            text: 'text-yellow-900',
            textLight: 'text-yellow-600'
        },
        'Banjir': {
            bg: 'bg-red-50',
            border: 'border-red-200',
            text: 'text-red-900',
            textLight: 'text-red-600'
        }
    };
    return colors[status] || colors['Aman'];
}

// Get rule color helper
function getRuleColor(output) {
    const colors = {
        'Aman': {
            bg: 'bg-green-50',
            border: 'border-green-200',
            text: 'text-green-800',
            textLight: 'text-green-600'
        },
        'Siaga': {
            bg: 'bg-yellow-50',
            border: 'border-yellow-200',
            text: 'text-yellow-800',
            textLight: 'text-yellow-600'
        },
        'Banjir': {
            bg: 'bg-red-50',
            border: 'border-red-200',
            text: 'text-red-800',
            textLight: 'text-red-600'
        }
    };
    return colors[output] || colors['Aman'];
}

function initMembershipCharts() {
    // Ensure chart data exists
    if (!chartData || !chartData.air || !chartData.hujan) {
        console.error('Chart data is missing or incomplete.');
        return;  // Prevent chart rendering if data is not available
    }

    // Initialize chart for Ketinggian Air
    const traceAirRendah = {
        x: chartData.air.x,
        y: chartData.air.rendah,
        type: 'scatter',
        mode: 'lines',
        name: 'Rendah',
        line: { color: '#22c55e', width: 3 },
        fill: 'tonexty'
    };

    const traceAirSedang = {
        x: chartData.air.x,
        y: chartData.air.sedang,
        type: 'scatter',
        mode: 'lines',
        name: 'Sedang',
        line: { color: '#f59e0b', width: 3 },
        fill: 'tonexty'
    };

    const traceAirTinggi = {
        x: chartData.air.x,
        y: chartData.air.tinggi,
        type: 'scatter',
        mode: 'lines',
        name: 'Tinggi',
        line: { color: '#ef4444', width: 3 },
        fill: 'tonexty'
    };

    const layoutAir = {
        title: {
            text: 'Ketinggian Air (cm)',
            font: { size: 14 }
        },
        xaxis: {
            title: 'Ketinggian (cm)',
            gridcolor: '#f3f4f6'
        },
        yaxis: {
            title: 'μ',
            range: [0, 1.1],
            gridcolor: '#f3f4f6'
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        margin: { l: 50, r: 20, t: 50, b: 50 },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        showlegend: false
    };

    // Create chart for Ketinggian Air
    Plotly.newPlot('membershipChartAir', [traceAirRendah, traceAirSedang, traceAirTinggi], layoutAir, {
        responsive: true,
        displayModeBar: false
    });

    // Initialize chart for Curah Hujan
    const traceHujanRendah = {
        x: chartData.hujan.x,
        y: chartData.hujan.rendah,
        type: 'scatter',
        mode: 'lines',
        name: 'Rendah',
        line: { color: '#22c55e', width: 3 },
        fill: 'tonexty'
    };

    const traceHujanSedang = {
        x: chartData.hujan.x,
        y: chartData.hujan.sedang,
        type: 'scatter',
        mode: 'lines',
        name: 'Sedang',
        line: { color: '#f59e0b', width: 3 },
        fill: 'tonexty'
    };

    const traceHujanTinggi = {
        x: chartData.hujan.x,
        y: chartData.hujan.tinggi,
        type: 'scatter',
        mode: 'lines',
        name: 'Tinggi',
        line: { color: '#ef4444', width: 3 },
        fill: 'tonexty'
    };

    const layoutHujan = {
        title: {
            text: 'Curah Hujan (mm)',
            font: { size: 14 }
        },
        xaxis: {
            title: 'Curah Hujan (mm)',
            gridcolor: '#f3f4f6'
        },
        yaxis: {
            title: 'μ',
            range: [0, 1.1],
            gridcolor: '#f3f4f6'
        },
        plot_bgcolor: '#ffffff',
        paper_bgcolor: '#ffffff',
        margin: { l: 50, r: 20, t: 50, b: 50 },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        showlegend: false
    };

    // Create chart for Curah Hujan
    Plotly.newPlot('membershipChartHujan', [traceHujanRendah, traceHujanSedang, traceHujanTinggi], layoutHujan, {
        responsive: true,
        displayModeBar: false
    });
}


// Update membership charts with current input values
function updateMembershipCharts(ketinggian, curahHujan, result) {
    // Add vertical line for current input values on Air chart
    const airChartUpdate = {
        shapes: [{
            type: 'line',
            x0: ketinggian,
            x1: ketinggian,
            y0: 0,
            y1: 1,
            line: {
                color: '#6366f1',
                width: 3,
                dash: 'dash'
            }
        }],
        annotations: [{
            x: ketinggian,
            y: 0.9,
            text: `${ketinggian} cm`,
            showarrow: true,
            arrowhead: 2,
            arrowcolor: '#6366f1',
            font: { color: '#6366f1', size: 12 }
        }]
    };

    // Add vertical line for current input values on Hujan chart
    const hujanChartUpdate = {
        shapes: [{
            type: 'line',
            x0: curahHujan,
            x1: curahHujan,
            y0: 0,
            y1: 1,
            line: {
                color: '#6366f1',
                width: 3,
                dash: 'dash'
            }
        }],
        annotations: [{
            x: curahHujan,
            y: 0.9,
            text: `${curahHujan} mm`,
            showarrow: true,
            arrowhead: 2,
            arrowcolor: '#6366f1',
            font: { color: '#6366f1', size: 12 }
        }]
    };

    // Update both charts
    Plotly.relayout('membershipChartAir', airChartUpdate);
    Plotly.relayout('membershipChartHujan', hujanChartUpdate);
}

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fuzzyForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const ketinggian = parseFloat(document.getElementById('ketinggian').value);
            const curahHujan = parseFloat(document.getElementById('curah_hujan').value);
            
            // Validation
            if (isNaN(ketinggian) || ketinggian < 0 || ketinggian > 100) {
                alert('Silakan masukkan ketinggian air antara 0-100 cm');
                return;
            }

            if (isNaN(curahHujan) || curahHujan < 0 || curahHujan > 300) {
                alert('Silakan masukkan curah hujan antara 0-300 mm');
                return;
            }

            // Show loading
            showLoading();
            
            // Calculate fuzzy
            fetch('/fuzzy/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    ketinggian: ketinggian,
                    curah_hujan: curahHujan
                })
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    displayResults(data.result);
                    updateMembershipCharts(ketinggian, curahHujan, data.result);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                hideLoading();
                console.error('Error:', error);
                alert('Terjadi kesalahan saat menghitung fuzzy logic');
            });
        });
    }
});

// Display calculation results
function displayResults(result) {
    // Show panels
    document.getElementById('currentStatus').classList.remove('hidden');
    document.getElementById('resultsPanel').classList.remove('hidden');
    
    // Current Status
    const statusColor = getStatusColor(result.step4_defuzzifikasi.final_status);
    document.getElementById('statusContent').innerHTML = `
        <div class="grid grid-cols-1 gap-4">
            <div class="text-center p-4 ${statusColor.bg} rounded-lg border ${statusColor.border}">
                <div class="text-3xl font-bold ${statusColor.text} mb-2">${result.step4_defuzzifikasi.final_status}</div>
                <div class="text-sm ${statusColor.textLight}">Status Banjir</div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="text-center p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <div class="text-xl font-bold text-blue-900">${result.input.ketinggian_air} cm</div>
                    <div class="text-xs text-blue-600">Ketinggian Air</div>
                </div>
                <div class="text-center p-3 bg-green-50 rounded-lg border border-green-200">
                    <div class="text-xl font-bold text-green-900">${result.input.curah_hujan} mm</div>
                    <div class="text-xs text-green-600">Curah Hujan</div>
                </div>
            </div>
            <div class="text-center p-3 bg-purple-50 rounded-lg border border-purple-200">
                <div class="text-xl font-bold text-purple-900">${result.step4_defuzzifikasi.centroid_value}</div>
                <div class="text-xs text-purple-600">Nilai Centroid</div>
            </div>
        </div>
    `;

    // Step 1: Fuzzifikasi
    document.getElementById('step1Content').innerHTML = `
        <div class="space-y-4">
            <div>
                <h4 class="font-medium text-gray-900 mb-2">Ketinggian Air (${result.input.ketinggian_air} cm):</h4>
                <div class="grid grid-cols-3 gap-2">
                    <div class="bg-green-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-green-800">μ Rendah</div>
                        <div class="text-lg font-bold text-green-900">${result.step1_fuzzifikasi.air.rendah}</div>
                    </div>
                    <div class="bg-yellow-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-yellow-800">μ Sedang</div>
                        <div class="text-lg font-bold text-yellow-900">${result.step1_fuzzifikasi.air.sedang}</div>
                    </div>
                    <div class="bg-red-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-red-800">μ Tinggi</div>
                        <div class="text-lg font-bold text-red-900">${result.step1_fuzzifikasi.air.tinggi}</div>
                    </div>
                </div>
            </div>
            
            <div>
                <h4 class="font-medium text-gray-900 mb-2">Curah Hujan (${result.input.curah_hujan} mm):</h4>
                <div class="grid grid-cols-3 gap-2">
                    <div class="bg-green-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-green-800">μ Rendah</div>
                        <div class="text-lg font-bold text-green-900">${result.step1_fuzzifikasi.hujan.rendah}</div>
                    </div>
                    <div class="bg-yellow-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-yellow-800">μ Sedang</div>
                        <div class="text-lg font-bold text-yellow-900">${result.step1_fuzzifikasi.hujan.sedang}</div>
                    </div>
                    <div class="bg-red-50 p-3 rounded-lg text-center">
                        <div class="text-sm text-red-800">μ Tinggi</div>
                        <div class="text-lg font-bold text-red-900">${result.step1_fuzzifikasi.hujan.tinggi}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Step 2: Inferensi
    let inferenceHTML = '<div class="space-y-2">';
    if (result.step2_inferensi.length > 0) {
        result.step2_inferensi.forEach((rule, index) => {
            const ruleColor = getRuleColor(rule.output);
            inferenceHTML += `
                <div class="${ruleColor.bg} p-3 rounded-lg border ${ruleColor.border}">
                    <div class="flex items-center justify-between">
                        <div class="flex-1">
                            <div class="text-sm font-medium ${ruleColor.text}">${rule.condition}</div>
                            <div class="text-xs ${ruleColor.textLight} mt-1">→ ${rule.conclusion}</div>
                        </div>
                        <div class="text-lg font-bold ${ruleColor.text}">${rule.strength}</div>
                    </div>
                </div>
            `;
        });
    } else {
        inferenceHTML += '<div class="text-gray-500 text-sm">Tidak ada aturan yang aktif</div>';
    }
    inferenceHTML += '</div>';
    document.getElementById('step2Content').innerHTML = inferenceHTML;

    // Step 3: Agregasi
    let agregasiHTML = '<div class="space-y-3">';
    const agregasi = result.step3_agregasi;
    
    if (agregasi.aman && agregasi.aman > 0) {
        agregasiHTML += `
            <div class="bg-green-50 p-4 rounded-lg border border-green-200">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="font-medium text-green-900">Status Aman</div>
                        <div class="text-sm text-green-600">Nilai keanggotaan maksimum</div>
                    </div>
                    <div class="text-xl font-bold text-green-900">${agregasi.aman}</div>
                </div>
            </div>
        `;
    }
    
    if (agregasi.siaga && agregasi.siaga > 0) {
        agregasiHTML += `
            <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="font-medium text-yellow-900">Status Siaga</div>
                        <div class="text-sm text-yellow-600">Nilai keanggotaan maksimum</div>
                    </div>
                    <div class="text-xl font-bold text-yellow-900">${agregasi.siaga}</div>
                </div>
            </div>
        `;
    }
    
    if (agregasi.banjir && agregasi.banjir > 0) {
        agregasiHTML += `
            <div class="bg-red-50 p-4 rounded-lg border border-red-200">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="font-medium text-red-900">Status Banjir</div>
                        <div class="text-sm text-red-600">Nilai keanggotaan maksimum</div>
                    </div>
                    <div class="text-xl font-bold text-red-900">${agregasi.banjir}</div>
                </div>
            </div>
        `;
    }
    
    if ((!agregasi.aman || agregasi.aman === 0) && 
        (!agregasi.siaga || agregasi.siaga === 0) && 
        (!agregasi.banjir || agregasi.banjir === 0)) {
        agregasiHTML += '<div class="text-gray-500 text-sm">Tidak ada nilai agregasi yang aktif</div>';
    }
    
    agregasiHTML += '</div>';
    document.getElementById('step3Content').innerHTML = agregasiHTML;

    // Step 4: Defuzzifikasi
    document.getElementById('step4Content').innerHTML = `
        <div class="space-y-4">
            <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <h4 class="font-medium text-purple-900 mb-2">Metode Centroid:</h4>
                <div class="text-sm text-purple-700 mb-3">
                    Menghitung titik pusat massa dari area gabungan semua membership functions output
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="text-center">
                        <div class="text-lg font-bold text-purple-900">${result.step4_defuzzifikasi.centroid_value}</div>
                        <div class="text-xs text-purple-600">Nilai Centroid</div>
                    </div>
                    <div class="text-center">
                        <div class="text-lg font-bold text-purple-900">${result.step4_defuzzifikasi.final_status}</div>
                        <div class="text-xs text-purple-600">Status Final</div>
                    </div>
                </div>
            </div>
            
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <h4 class="font-medium text-gray-900 mb-2">Interpretasi Hasil:</h4>
                <div class="text-sm text-gray-700">
                    ${getStatusInterpretation(result.step4_defuzzifikasi.final_status, result.step4_defuzzifikasi.centroid_value)}
                </div>
            </div>
        </div>
    `;

    // Final Summary
    const finalStatusColor = getStatusColor(result.step4_defuzzifikasi.final_status);
    document.getElementById('finalSummary').innerHTML = `
        <div class="space-y-4">
            <div class="text-center">
                <div class="text-2xl font-bold text-gray-900 mb-2">
                    Status Deteksi Banjir: 
                    <span class="${finalStatusColor.text}">${result.step4_defuzzifikasi.final_status}</span>
                </div>
                <div class="text-gray-600">
                    Berdasarkan ketinggian air ${result.input.ketinggian_air} cm dan curah hujan ${result.input.curah_hujan} mm
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-white p-4 rounded-lg border border-gray-200">
                    <div class="text-sm text-gray-600 mb-1">Confidence Score</div>
                    <div class="text-xl font-bold text-gray-900">${result.step4_defuzzifikasi.centroid_value}</div>
                </div>
                <div class="bg-white p-4 rounded-lg border border-gray-200">
                    <div class="text-sm text-gray-600 mb-1">Rules Activated</div>
                    <div class="text-xl font-bold text-gray-900">${result.step2_inferensi.length}</div>
                </div>
            </div>
            
            <div class="bg-white p-4 rounded-lg border border-gray-200">
                <h4 class="font-medium text-gray-900 mb-2">Rekomendasi:</h4>
                <div class="text-sm text-gray-700">
                    ${getRecommendation(result.step4_defuzzifikasi.final_status)}
                </div>
            </div>
        </div>
    `;

    // Scroll to results
    document.getElementById('resultsPanel').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

// Get status interpretation
function getStatusInterpretation(status, centroidValue) {
    switch(status) {
        case 'Aman':
            return `Kondisi normal dengan nilai confidence ${centroidValue}. Ketinggian air dan curah hujan masih dalam batas aman.`;
        case 'Siaga':
            return `Kondisi perlu diwaspadai dengan nilai confidence ${centroidValue}. Ketinggian air atau curah hujan mulai meningkat.`;
        case 'Banjir':
            return `Kondisi berbahaya dengan nilai confidence ${centroidValue}. Ketinggian air dan curah hujan sudah mencapai level kritis.`;
        default:
            return `Status tidak dikenali dengan nilai confidence ${centroidValue}.`;
    }
}

// Get recommendation based on status
function getRecommendation(status) {
    switch(status) {
        case 'Aman':
            return 'Lanjutkan monitoring rutin. Pastikan sistem drainase berfungsi dengan baik dan bersih dari sampah.';
        case 'Siaga':
            return 'Tingkatkan kewaspadaan. Siapkan langkah-langkah mitigasi seperti pompa air, karung pasir, dan jalur evakuasi. Informasikan kepada warga untuk bersiap-siap.';
        case 'Banjir':
            return 'Segera lakukan tindakan darurat! Aktifkan sistem peringatan dini, mulai evakuasi warga dari area berisiko tinggi, dan koordinasikan dengan tim penanganan bencana.';
        default:
            return 'Lakukan pengecekan ulang pada sistem dan data input.';
    }
}

// Export functions for external use
window.FuzzyManualCalculator = {
    setInput,
    showLoading,
    hideLoading,
    initMembershipCharts,
    updateMembershipCharts,
    displayResults
};
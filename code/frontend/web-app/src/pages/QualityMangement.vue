<template>
    <q-page class="dashboard q-pa-lg">

      <!-- header -->
      <div class="row q-mb-lg">
        <div class="col">
          <h1 class="text-h4 text-bold">Quality Management</h1>
          <p class="text-subtitle2">Track, manage and advance your goals.</p>
        </div>
      </div>

      <!-- KPI tiles -->
      <div class="row q-col-gutter-md q-mb-md">
        <template v-for="kpi in kpis" :key="kpi.label">
          <div class="col-12 col-sm-6 col-md-3">
            <q-card bordered flat class="kpi-card flex column items-start justify-between">
              <span class="text-body2">{{ kpi.label }}</span>
              <span class="text-h5 text-bold">{{ kpi.value }}</span>
            </q-card>
          </div>
        </template>
      </div>

      <!-- first two charts -->
      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Defects Reported by Assembly Line</div>
            <div class="card-content">
              <div class="chart-box"><canvas ref="assemblyBar"></canvas></div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Cost Predicted</div>
            <div class="card-content">
              <div class="square-box"><canvas ref="costDonut"></canvas></div>
            </div>
          </q-card>
        </div>
      </div>

      <!-- right-first-time & radar -->
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Right First Time (Last 12 months)</div>
            <div class="card-content">
              <div class="chart-box"><canvas ref="rftLine"></canvas></div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Count of Defects in Each Defect Type</div>
            <div class="card-content">
              <div class="square-box"><canvas ref="defectRadar"></canvas></div>
            </div>
          </q-card>
        </div>
      </div>

      <!-- rate of return & defect density -->
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Rate of Return</div>
            <div class="card-content">
              <div class="chart-box"><canvas ref="rorBar"></canvas></div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Defect Density</div>
            <div class="card-content">
              <div class="chart-box"><canvas ref="densityLine"></canvas></div>
            </div>
          </q-card>
        </div>
      </div>

      <!-- uptime / MTBF-MTTR -->
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">Uptime vs Downtime</div>
            <div class="card-content">
              <div class="square-box"><canvas ref="uptimeGauge"></canvas></div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-6">
          <q-card bordered flat class="card">
            <div class="card-header">MTBF vs MTTR</div>
            <div class="card-content">
              <div class="chart-box"><canvas ref="mtbfMttr"></canvas></div>
            </div>
          </q-card>
        </div>
      </div>

      <!-- small gauges -->
      <div class="row q-col-gutter-md q-mt-lg">
        <template v-for="g in smallGauges" :key="g.label">
          <div class="col-12 col-sm-6 col-md-2">
            <q-card bordered flat class="card text-center">
              <div class="card-header">{{ g.label }}</div>
              <div class="card-content">
                <div class="square-box"><canvas :ref="g.ref"></canvas></div>
              </div>
            </q-card>
          </div>
        </template>
      </div>

    </q-page>
  </template>

  <script>
  import { ref, onMounted } from 'vue'
  import Chart from 'chart.js/auto'
  import ChartDataLabels from 'chartjs-plugin-datalabels'
  Chart.register(ChartDataLabels)

  const gaugeDot = {
    id: 'gaugeDot',
    afterDraw (chart) {
      const { ctx, chartArea } = chart
      if (!chartArea) return
      const x = (chartArea.left + chartArea.right) / 2
      const y = chartArea.bottom - 8
      ctx.fillStyle = '#1B1F3B'
      ctx.beginPath()
      ctx.arc(x, y, 5, 0, Math.PI * 2)
      ctx.fill()
    }
  }
  Chart.register(gaugeDot)

  export default {
    name: 'QualityManagement',
    setup () {
      /* refs */
      const assemblyBar = ref(null)
      const costDonut  = ref(null)
      const rftLine    = ref(null)
      const defectRadar = ref(null)
      const rorBar     = ref(null)
      const densityLine = ref(null)
      const uptimeGauge = ref(null)
      const mtbfMttr   = ref(null)

      const smallRefs = {
        throughput: ref(null),
        oee: ref(null),
        capacity: ref(null),
        fpy: ref(null),
        scrap: ref(null)
      }

      /* top KPI tiles */
      const kpis = [
        { label: 'Total Production (units)', value: '2,420' },
        { label: 'Defective Production (%)', value: '0.20' },
        { label: 'Production Rate (units/hr)', value: '171.36' },
        { label: 'Production Rate (hr)', value: '1.22' }
      ]

      const smallGauges = [
        { label: 'Throughput', ref: 'throughput', min: 0, max: 12, val: 8 },
        { label: 'OEE', ref: 'oee', min: 0, max: 100, val: 75, unit: '%' },
        { label: 'Capacity utilisation', ref: 'capacity', min: 0, max: 100, val: 75, unit: '%' },
        { label: 'First Pass Yield', ref: 'fpy', min: 0, max: 100, val: 91, unit: '%' },
        { label: 'Scrap Rate', ref: 'scrap', min: 0, max: 30, val: 10, unit: '%' }
      ]

      onMounted(() => {
        /* assembly line bar */
        new Chart(assemblyBar.value, {
          type: 'bar',
          data: {
            labels: ['Torrie Mcgraff', 'Party Tifft', 'Alena Solazer'],
            datasets: [{ data: [10, 8, 5], backgroundColor: '#27ae60' }]
          },
          options: {
            indexAxis: 'y',
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              datalabels: { anchor: 'end', align: 'right', formatter: v => v }
            },
            scales: {
              x: { beginAtZero: true, grid: { borderDash: [4, 4] } },
              y: { grid: { display: false } }
            }
          }
        })

        /* cost predicted donut */
        new Chart(costDonut.value, {
          type: 'doughnut',
          data: {
            labels: [
              'Non Compliance product spec (Analytical)',
              'Non Compliance product spec (Stability)',
              'Critical',
              'Packaging',
              'Underfill'
            ],
            datasets: [{
              data: [18.8, 18.8, 37.5, 48, 15.6],
              backgroundColor: ['#B39DDB', '#4CAF50', '#E74C3C', '#F39C12', '#F1C40F']
            }]
          },
          options: {
            cutout: '55%',
            plugins: { legend: { position: 'right' } }
          }
        })

        /* right-first-time line */
        new Chart(rftLine.value, {
          type: 'line',
          data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            datasets: [{ data: [98,100,99.5,98,98.5,99,100,100.5,99.8,99.2,99,99.3], borderColor: '#E74C3C', tension: 0.4, fill: false }]
          },
          options: {
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { min: 96, max: 101, ticks: { callback: v => v + '%' }, grid: { borderDash: [4,4] } },
              x: { grid: { display: false } }
            }
          }
        })

        /* defect radar */
        new Chart(defectRadar.value, {
          type: 'radar',
          data: {
            labels: ['Damaged','Defective','Test Cycle','Other Causes','Operator Error','No Analysis','Electrically Defective'],
            datasets: [{
              data: [8,6,4,3,2,4,5],
              backgroundColor: 'rgba(255, 165, 0, 0.3)',
              borderColor: '#FFA726',
              pointBackgroundColor: '#FFA726'
            }]
          },
          options: {
            plugins: { legend: { display: false } },
            scales: { r: { beginAtZero: true, suggestedMax: 8, grid: { color: '#ccc' } } }
          }
        })

        /* rate of return bar */
        new Chart(rorBar.value, {
          type: 'bar',
          data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            datasets: [
              { label: 'Assembly A10', data: [100,99.2,99.5,99.4,99.6,99.4,99.5,99.6,99.4,99.5,99.6,99.4], backgroundColor: '#FDE68A' },
              { label: 'Assembly A15', data: [101,98.8,98.9,98.9,99,98.9,99,98.9,98.9,98.9,98.9,98.9], backgroundColor: '#F4A418' }
            ]
          },
          options: {
            maintainAspectRatio: false,
            scales: {
              y: { min: 96, max: 101, ticks: { callback: v => v + '%' }, grid: { borderDash: [4,4] } },
              x: { grid: { display: false } }
            }
          }
        })

        /* defect density line */
        new Chart(densityLine.value, {
          type: 'line',
          data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            datasets: [
              { label: 'Assembly A10', data: [101,100.5,100,99.5,100,100.3,99.8,99,98.5,100,100,99], borderColor: '#27AE60', tension: 0.4 },
              { label: 'Assembly A15', data: [98.5,97,97.5,97.8,97.9,98,97.5,96.5,96.6,97,97.4,97.1], borderColor: '#E74C3C', tension: 0.4 }
            ]
          },
          options: {
            maintainAspectRatio: false,
            scales: {
              y: { min: 96, max: 101, ticks: { callback: v => v + '%' }, grid: { borderDash: [4,4] } },
              x: { grid: { display: false } }
            }
          }
        })

        /* uptime gauge (donut) */
        new Chart(uptimeGauge.value, {
          type: 'doughnut',
          data: { datasets: [{ data: [12.5, 87.5], backgroundColor: ['#27AE60','#E74C3C'] }] },
          options: {
            rotation: -90,
            circumference: 180,
            cutout: '70%',
            plugins: {
              legend: { position: 'right', labels: { boxWidth: 12 } },
              datalabels: { display: false }
            }
          }
        })

        /* MTBF vs MTTR combo */
        new Chart(mtbfMttr.value, {
          data: {
            labels: ['Machine 1','Machine 3','Machine 5','Machine 7'],
            datasets: [
              { type: 'bar', label: 'MTBF', data: [900,700,480,820], backgroundColor: '#27AE60' },
              { type: 'line', label: 'MTTR', data: [600,500,480,600], borderColor: '#F3BA2F', tension: 0, pointRadius: 4 }
            ]
          },
          options: {
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, grid: { borderDash: [4,4] }, title: { display: true, text: 'MTTR' } } }
          }
        })

        /* mini gauges */
        smallGauges.forEach(g => {
          const refName = smallRefs[g.ref]
          new Chart(refName.value, {
            type: 'doughnut',
            data: {
              datasets: [{
                data: [g.val - g.min, g.max - g.val],
                backgroundColor: ctx => {
                  const { chartArea, ctx: c } = ctx.chart
                  if (!chartArea) return ['#ff5151','#eee']
                  const gGrad = c.createLinearGradient(chartArea.left, 0, chartArea.right, 0)
                  gGrad.addColorStop(0, '#ff5151')
                  gGrad.addColorStop(0.5, '#e5bf00')
                  gGrad.addColorStop(1, '#27ae60')
                  return [gGrad, '#eeeeee']
                }
              }]
            },
            options: {
              rotation: -90,
              circumference: 180,
              cutout: '70%',
              plugins: {
                legend: { display: false },
                datalabels: { display: false }
              }
            }
          })
        })
      })

      return {
        kpis,
        assemblyBar,
        costDonut,
        rftLine,
        defectRadar,
        rorBar,
        densityLine,
        uptimeGauge,
        mtbfMttr,
        smallGauges,
        ...smallRefs
      }
    }
  }
  </script>

  <style scoped>
  .dashboard { background: #fafafa; }
  .text-bold { font-weight: 700; }
  p.text-subtitle2 { color: #636e72; }

  .card, .kpi-card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .card-header { font-size: 1rem; font-weight: 600; border-bottom: 1px solid #ececec; padding-bottom: .5rem; }
  .card-content { margin-top: .5rem; flex: 1; display: flex; flex-direction: column; }

  .square-box { position: relative; width: 100%; aspect-ratio: 1/1; }
  .chart-box  { position: relative; width: 100%; height: 260px; }

  .square-box canvas,
  .chart-box  canvas { position: absolute; inset: 0; width: 100% !important; height: 100% !important; }
  </style>

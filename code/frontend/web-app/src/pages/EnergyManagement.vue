<template>
    <q-page class="compliance-dashboard q-pa-lg">
      <div class="row q-mb-lg">
        <div class="col">
          <h1 class="text-h4 text-bold">Compliance Management</h1>
          <p class="text-subtitle2">Track, manage and advance your compliance goals.</p>
        </div>
      </div>
      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Cost Predicted</div>
            <div class="card-content">
              <div class="chart-container">
                <canvas ref="costChart"></canvas>
              </div>
              <div class="chart-legend q-mt-sm">
                <div class="row items-center">
                  <q-icon name="lens" size="12px" class="text-warning" />
                  <span class="legend-text">Electricity – 83.5%</span>
                </div>
                <div class="row items-center q-mt-xs">
                  <q-icon name="lens" size="12px" class="text-positive" />
                  <span class="legend-text">Gas – 16.5%</span>
                </div>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Change in Cost</div>
            <div class="card-content">
              <div class="chart-container">
                <canvas ref="changeChart"></canvas>
              </div>
              <div class="change-label q-mt-md">
                <div class="text-h6 text-bold">5% <small>Increase on cost</small></div>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Usage Estimate</div>
            <div class="card-content">
              <div class="row justify-between items-center text-subtitle2">
                <span>Till now: 82.6 kWh</span>
                <span>Predicted: 82.6 kWh</span>
              </div>
              <div class="chart-container q-mt-sm">
                <canvas ref="usageChart"></canvas>
              </div>
            </div>
          </q-card>
        </div>
      </div>
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Active Appliances</div>
            <div class="card-content">
              <div v-for="app in appliances" :key="app.label" class="row items-center q-mb-sm">
                <div class="col-6 text-body2">{{ app.label }}</div>
                <div class="col-4">
                  <q-linear-progress :value="app.value / maxAppliance" rounded track-color="#e0e0e0" color="positive" />
                </div>
                <div class="col-2 text-body2">{{ app.value }} kWh</div>
              </div>
              <div class="text-caption q-mt-sm">
                Top 3 appliances make up 70.3% of the net usage.
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card text-center">
            <div class="card-header">Energy Intensity</div>
            <div class="card-content">
              <div class="gauge-container">
                <canvas ref="intensityGauge"></canvas>
              </div>
              <div class="text-h5 text-bold q-mt-md">60 kWh/Sqft</div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Carbon Footprint</div>
            <div class="card-content">
              <div class="row justify-between items-center text-subtitle2">
                <span>Emission</span>
              </div>
              <div class="bar-container q-mt-sm">
                <canvas ref="carbonChart"></canvas>
              </div>
              <div class="row justify-between items-center q-mt-sm text-body2">
                <span>36.4 kg of CO2</span>
                <span>181.1 kg of CO2</span>
              </div>
              <div class="text-subtitle2 q-mt-md">Green Energy Generated</div>
              <div class="bar-container q-mt-sm">
                <canvas ref="greenChart"></canvas>
              </div>
              <div class="row justify-between items-center q-mt-sm text-body2">
                <span>145 kWh</span>
                <span>1678 kWh</span>
              </div>
            </div>
          </q-card>
        </div>
      </div>
      <div class="row q-col-gutter-md q-mt-lg">
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Emissions By Activities (T CO₂)</div>
            <div class="card-content d-flex">
              <div class="flex-1 chart-container">
                <canvas ref="activitiesChart"></canvas>
              </div>
              <div class="legend flex-1 q-ml-md text-body2">
                <div v-for="scope in scopes" :key="scope.label" class="row items-center q-mb-xs">
                  <q-icon name="lens" size="12px" :class="scope.color" />
                  <span class="q-ml-xs">
                    {{ scope.label }} – {{ scope.percent }}%
                  </span>
                </div>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Emissions Over Time (T CO₂)</div>
            <div class="card-content">
              <div class="chart-container">
                <canvas ref="overTimeChart"></canvas>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-12 col-md-4">
          <q-card flat bordered class="card">
            <div class="card-header">Power Factor Last 7 days</div>
            <div class="card-content">
              <div class="text-subtitle2">
                Power Factor last 7 days average: 0.97
              </div>
              <div class="chart-container q-mt-sm">
                <canvas ref="powerChart"></canvas>
              </div>
            </div>
          </q-card>
        </div>
      </div>
    </q-page>
  </template>

  <script>
  import { ref, onMounted } from 'vue'
  import Chart from 'chart.js/auto'
  export default {
    name: 'ComplianceManagement',
    setup() {
      const costChart = ref(null)
      const changeChart = ref(null)
      const usageChart = ref(null)
      const intensityGauge = ref(null)
      const carbonChart = ref(null)
      const greenChart = ref(null)
      const activitiesChart = ref(null)
      const overTimeChart = ref(null)
      const powerChart = ref(null)
      const usageData = [10,20,30,45,60,80,100,120,140,160,180,200,220,240,260,280,300]
      const appliances = [
        { label: 'Heating & AC', value: 1.4 },
        { label: 'EV Charge', value: 1.4 },
        { label: 'Plug Loads', value: 1.4 },
        { label: 'Refrigeration', value: 1.4 },
        { label: 'Lightning', value: 1.4 },
        { label: 'Others', value: 1.4 }
      ]
      const maxAppliance = Math.max(...appliances.map(a => a.value))
      const scopes = [
        { label: 'Scope 1', percent: 18.8, color: 'text-warning' },
        { label: 'Scope 2', percent: 48.0, color: 'text-danger' },
        { label: 'Scope 3', percent: 33.2, color: 'text-positive' }
      ]
      onMounted(() => {
        new Chart(costChart.value, {
          type: 'doughnut',
          data: { labels:['Electricity','Gas'], datasets:[{ data:[83.5,16.5], backgroundColor:['#f1c40f','#2ecc71'] }] },
          options:{ cutout:'70%', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
        })
        new Chart(changeChart.value, {
          type:'bar',
          data:{ labels:['Mar','Apr'], datasets:[{ data:[420,534], backgroundColor:'#2ecc71' }] },
          options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true}} }
        })
        new Chart(usageChart.value, {
          type:'line',
          data:{ labels:Array(usageData.length).fill(''), datasets:[{ data:usageData, fill:{ target:'origin', above:'#2ecc7133', below:'#e74c3c33' }, borderWidth:0 }] },
          options:{ maintainAspectRatio:false, scales:{ y:{ display:false }, x:{ display:false } }, elements:{ line:{ tension:0.4 } }, plugins:{legend:{display:false}} }
        })
        new Chart(intensityGauge.value, {
          type:'doughnut',
          data:{ labels:[], datasets:[{ data:[60,40], backgroundColor:['#e74c3c','#2ecc71'] }] },
          options:{ cutout:'85%', rotation:-90, circumference:180, responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
        })
        new Chart(carbonChart.value, {
          type:'bar',
          data:{ labels:[''], datasets:[{ data:[36.4], backgroundColor:'#d35400' },{ data:[181.1], backgroundColor:'#ecf0f1' }] },
          options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
        })
        new Chart(greenChart.value, {
          type:'bar',
          data:{ labels:[''], datasets:[{ data:[145], backgroundColor:'#2ecc71' },{ data:[1678], backgroundColor:'#ecf0f1' }] },
          options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
        })
        new Chart(activitiesChart.value, {
          type:'doughnut',
          data:{ labels:scopes.map(s=>s.label), datasets:[{ data:scopes.map(s=>s.percent), backgroundColor:['#f1c40f','#e74c3c','#2ecc71'] }] },
          options:{ cutout:'70%', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
        })
        new Chart(overTimeChart.value, {
          type:'bar',
          data:{ labels:['Jan','Feb','Mar'], datasets:[
            { label:'Scope 1', data:[300,200,150], backgroundColor:'#f1c40f' },
            { label:'Scope 2', data:[200,150,100], backgroundColor:'#e67e22' },
            { label:'Scope 3', data:[400,300,200], backgroundColor:'#e74c3c' }
          ] },
          options:{ responsive:true, maintainAspectRatio:false, scales:{ y:{ stacked:true }, x:{ stacked:true } }, plugins:{legend:{position:'top'}} }
        })
        new Chart(powerChart.value, {
          type:'bar',
          data:{ labels:['1','2','3','4','5','6','7'], datasets:[{ data:[0.98,0.95,0.99,0.93,0.99,0.99,0.91], backgroundColor:['#95a5a6','#e74c3c','#95a5a6','#e74c3c','#95a5a6','#95a5a6','#e74c3c'] }] },
          options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{ y:{ min:0.8, max:1, ticks:{ stepSize:0.05 } } } }
        })
      })
      return {
        costChart,
        changeChart,
        usageChart,
        intensityGauge,
        carbonChart,
        greenChart,
        activitiesChart,
        overTimeChart,
        powerChart,
        appliances,
        maxAppliance,
        scopes
      }
    }
  }
  </script>

  <style scoped>
  .compliance-dashboard {
    background: #fafafa;
  }
  .card {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .card-header {
    font-size: 1rem;
    font-weight: 600;
    border-bottom: 1px solid #ececec;
    padding-bottom: 0.5rem;
  }
  .card-content {
    margin-top: 0.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  .chart-container,
  .gauge-container,
  .bar-container {
    height: 180px;
    position: relative;
    width: 100%;
    margin-bottom: 0.5rem;
  }
  .chart-container canvas,
  .gauge-container canvas,
  .bar-container canvas {
    position: absolute;
    inset: 0;
    width: 100% !important;
    height: 100% !important;
  }
  .text-bold {
    font-weight: 700;
  }
  .legend-text {
    margin-left: 0.5rem;
  }
  .change-label {
    text-align: right;
  }
  p.text-subtitle2 {
    color: #636e72;
  }
  </style>

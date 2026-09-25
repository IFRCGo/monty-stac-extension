<script setup lang="ts">
// Context as a stack of hazard-independent layers. A hazard footprint cuts through the
// people and asset layers; the cut is Exposure.
const HAZ = '#cf3f02', CTX = '#2a78d6', EXP = '#1baf7a'
const layers = [
  { name: 'Coping capacity', ex: 'health access, governance', group: 'vulnerability & coping' },
  { name: 'Vulnerability', ex: 'poverty, uprooted people', group: 'vulnerability & coping' },
  { name: 'Buildings & infrastructure', ex: 'roads, hospitals, schools', group: 'people & assets' },
  { name: 'Population', ex: 'WorldPop, GHSL', group: 'people & assets' },
  { name: 'Admin boundaries', ex: 'CODs', group: 'reference' },
]
const dx = 60, w = 300, h = 46, step = 50, top = 40
const layerPath = (y: number) => `M${dx},${y} L${dx + w},${y} L${w},${y + h} L0,${y + h} Z`
</script>

<template>
  <svg viewBox="0 0 640 330" class="w-full" role="img" aria-label="Context layers stacked, with a hazard footprint intersecting the people and asset layers">
    <g transform="translate(10,0)">
      <g v-for="(l, i) in layers" :key="l.name">
        <path :d="layerPath(top + i * step)" :fill="CTX" :fill-opacity="0.12 + i * 0.07" :stroke="CTX" stroke-width="1.5">
          <title>{{ l.name }} — {{ l.ex }}</title>
        </path>
        <text :x="w + dx + 16" :y="top + i * step + 20" class="ln">{{ l.name }}</text>
        <text :x="w + dx + 16" :y="top + i * step + 36" class="ex">{{ l.ex }}</text>
      </g>
      <!-- hazard footprint cutting the people & assets layers -->
      <ellipse cx="170" :cy="top + 2 * step + 23" rx="70" ry="13" :fill="EXP" stroke="#fff" stroke-width="2" />
      <ellipse cx="170" :cy="top + 3 * step + 23" rx="70" ry="13" :fill="EXP" stroke="#fff" stroke-width="2" />
      <line x1="170" y1="6" x2="170" :y2="top + 3 * step + 10" :stroke="HAZ" stroke-width="2" stroke-dasharray="5 4" />
      <ellipse cx="170" cy="18" rx="70" ry="13" :fill="HAZ" fill-opacity="0.15" :stroke="HAZ" stroke-width="2" />
      <text x="250" y="22" class="ln">hazard footprint</text>
      <text x="170" :y="top + 3 * step + 27" text-anchor="middle" class="in">exposure</text>
    </g>
  </svg>
</template>

<style scoped>
.ln { font-size: 14px; font-weight: 700; fill: #3f3f3f; }
.ex { font-size: 12px; fill: #555; }
.in { font-size: 12px; font-weight: 700; fill: #0d1f17; }
</style>

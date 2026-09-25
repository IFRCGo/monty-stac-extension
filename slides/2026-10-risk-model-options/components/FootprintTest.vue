<script setup lang="ts">
// A hazard footprint laid over people and buildings. Elements inside the footprint are
// Exposure; every element is Context whether or not a hazard touches it.
import { computed } from 'vue'
const HAZ = '#cf3f02', CTX = '#2a78d6', EXP = '#1baf7a'
const cx = 250, cy = 150, rx = 150, ry = 85
const items = computed(() => {
  const out: { x: number; y: number; kind: 'person' | 'building'; inside: boolean }[] = []
  for (let r = 0; r < 7; r++) {
    for (let c = 0; c < 13; c++) {
      const x = 40 + c * 36 + (r % 2 ? 18 : 0)
      const y = 40 + r * 38
      const kind = (r * 13 + c) % 3 === 0 ? 'building' : 'person'
      const inside = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1
      out.push({ x, y, kind, inside })
    }
  }
  return out
})
</script>

<template>
  <svg viewBox="0 0 520 330" class="w-full" role="img"
       aria-label="People and buildings inside a hazard footprint are exposure; all of them are context">
    <rect x="10" y="12" width="500" height="280" rx="10" fill="#f4f8fd" />
    <ellipse :cx="cx" :cy="cy" :rx="rx" :ry="ry" :fill="HAZ" fill-opacity="0.1" :stroke="HAZ" stroke-width="2" />
    <g v-for="(it, i) in items" :key="i">
      <circle v-if="it.kind === 'person'" :cx="it.x" :cy="it.y" r="6"
              :fill="it.inside ? EXP : CTX" :fill-opacity="it.inside ? 1 : 0.45" stroke="#fff" stroke-width="2">
        <title>person — {{ it.inside ? 'exposed' : 'context only' }}</title>
      </circle>
      <rect v-else :x="it.x - 6" :y="it.y - 6" width="12" height="12" rx="2"
            :fill="it.inside ? EXP : CTX" :fill-opacity="it.inside ? 1 : 0.45" stroke="#fff" stroke-width="2">
        <title>building — {{ it.inside ? 'exposed' : 'context only' }}</title>
      </rect>
    </g>
    <text :x="cx" :y="cy - ry - 8" text-anchor="middle" class="lbl">hazard footprint</text>
    <!-- legend -->
    <g transform="translate(20,312)">
      <circle cx="6" cy="0" r="6" :fill="EXP" /><rect x="16" y="-6" width="12" height="12" rx="2" :fill="EXP" />
      <text x="36" y="4" class="lg"><tspan font-weight="700">Exposure</tspan> — inside the footprint</text>
      <circle cx="266" cy="0" r="6" :fill="CTX" fill-opacity="0.45" /><rect x="276" y="-6" width="12" height="12" rx="2" :fill="CTX" fill-opacity="0.45" />
      <text x="296" y="4" class="lg"><tspan font-weight="700">Context</tspan> — with or without a hazard</text>
    </g>
  </svg>
</template>

<style scoped>
.lbl { font-size: 13px; fill: #3f3f3f; font-weight: 600; }
.lg { font-size: 12px; fill: #3f3f3f; }
</style>

<script setup lang="ts">
// Schematic humanitarian population funnel (not to scale), with the data that feeds each stage.
const stages = [
  { name: 'Total population', from: 'Context', h: 150, fill: '#e6e6e6', ink: '#3f3f3f' },
  { name: 'Exposed', from: 'Hazard ∩ Context', h: 122, fill: '#1baf7a', ink: '#0d1f17' },
  { name: 'Affected', from: 'Impact', h: 96, fill: '#d9d9d9', ink: '#3f3f3f' },
  { name: 'In need', from: '× vulnerability', h: 72, fill: '#104281', ink: '#ffffff' },
  { name: 'Targeted', from: 'Response', h: 52, fill: '#d9d9d9', ink: '#3f3f3f' },
  { name: 'Reached', from: 'Response', h: 36, fill: '#e6e6e6', ink: '#3f3f3f' },
]
const W = 150, gap = 8, mid = 95
</script>

<template>
  <svg viewBox="0 0 950 230" class="w-full" role="img" aria-label="Population funnel from total population to reached, schematic">
    <g v-for="(s, i) in stages" :key="s.name">
      <path :d="`M${i * (W + gap)},${mid - s.h / 2}
                 L${i * (W + gap) + W},${mid - (stages[i + 1]?.h ?? s.h * 0.8) / 2}
                 L${i * (W + gap) + W},${mid + (stages[i + 1]?.h ?? s.h * 0.8) / 2}
                 L${i * (W + gap)},${mid + s.h / 2} Z`"
            :fill="s.fill">
        <title>{{ s.name }} — fed by {{ s.from }}</title>
      </path>
      <text :x="i * (W + gap) + W / 2" :y="mid + 5" text-anchor="middle" class="st" :fill="s.ink">{{ s.name }}</text>
      <text :x="i * (W + gap) + W / 2" y="200" text-anchor="middle" class="fr">{{ s.from }}</text>
    </g>
    <text x="0" y="226" class="cap">Schematic, not to scale. Montandon estimates the exposed and in-need stages.</text>
  </svg>
</template>

<style scoped>
.st { font-size: 15px; font-weight: 700; }
.fr { font-size: 13px; fill: #555; }
.cap { font-size: 11px; fill: #777; }
</style>

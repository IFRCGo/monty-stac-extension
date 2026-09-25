<script setup lang="ts">
// Left: the risk triangle (H, E, V overlap = risk; capacity reduces it).
// Right: where each concept sits in time, and what Montandon covers today vs the proposal.
const HAZ = '#cf3f02', CTX = '#2a78d6', EXP = '#1baf7a'
const phases = [
  { name: 'Before', sub: 'risk', x: 470, w: 150, items: ['baseline hazard', 'population, assets', 'vulnerability', 'coping capacity'] },
  { name: 'Imminent', sub: 'forecast', x: 630, w: 150, items: ['forecast hazard', 'forecast exposure', 'early people in need'] },
  { name: 'After', sub: 'impact', x: 790, w: 170, items: ['event, hazard', 'exposure', 'impact, needs', 'response'] },
]
</script>

<template>
  <svg viewBox="0 0 980 330" class="w-full" role="img"
       aria-label="Risk is where hazard, exposure and vulnerability overlap; Montandon today covers the after-event phase, the proposal extends to before and imminent phases">
    <!-- risk triangle -->
    <circle cx="200" cy="165" r="140" fill="none" stroke="#8a8a8a" stroke-width="2" stroke-dasharray="6 5" />
    <text x="200" y="18" text-anchor="middle" class="m">capacity reduces risk</text>
    <circle cx="160" cy="130" r="72" :fill="HAZ" fill-opacity="0.18" :stroke="HAZ" stroke-width="2" />
    <circle cx="240" cy="130" r="72" :fill="EXP" fill-opacity="0.18" :stroke="EXP" stroke-width="2" />
    <circle cx="200" cy="200" r="72" :fill="CTX" fill-opacity="0.18" :stroke="CTX" stroke-width="2" />
    <text x="128" y="112" text-anchor="middle" class="b">Hazard</text>
    <text x="272" y="112" text-anchor="middle" class="b">Exposure</text>
    <text x="200" y="245" text-anchor="middle" class="b">Vulnerability</text>
    <text x="200" y="160" text-anchor="middle" class="r">Risk</text>

    <!-- timeline -->
    <line x1="470" y1="70" x2="960" y2="70" stroke="#bdbdbd" stroke-width="1" />
    <g v-for="p in phases" :key="p.name">
      <rect :x="p.x" y="40" :width="p.w - 6" height="30" rx="6" fill="#f2f2f2" />
      <text :x="p.x + (p.w - 6) / 2" y="60" text-anchor="middle" class="b">{{ p.name }} <tspan class="m">· {{ p.sub }}</tspan></text>
      <text v-for="(it, i) in p.items" :key="it" :x="p.x + 8" :y="96 + i * 20" class="s">{{ it }}</text>
    </g>
    <text x="785" y="30" text-anchor="middle" class="m">event</text>
    <line x1="785" y1="34" x2="785" y2="176" stroke="#555" stroke-width="1.5" stroke-dasharray="4 4" />

    <!-- coverage -->
    <rect x="790" y="192" width="164" height="30" rx="6" fill="#104281" />
    <text x="872" y="212" text-anchor="middle" class="w">Montandon today</text>
    <rect x="470" y="236" width="484" height="30" rx="6" fill="none" stroke="#104281" stroke-width="2" stroke-dasharray="6 4" />
    <text x="712" y="256" text-anchor="middle" class="b">the proposal: levels 1 → 4</text>
    <path d="M 780 282 L 490 282" stroke="#104281" stroke-width="2" marker-end="url(#ah)" />
    <text x="635" y="302" text-anchor="middle" class="m">from event records toward risk data</text>
    <defs>
      <marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
        <path d="M0,0 L10,5 L0,10 Z" fill="#104281" />
      </marker>
    </defs>
  </svg>
</template>

<style scoped>
.b { font-size: 14px; font-weight: 700; fill: #3f3f3f; }
.r { font-size: 20px; font-weight: 800; fill: #222; }
.m { font-size: 12px; font-weight: 400; fill: #666; }
.s { font-size: 13px; fill: #3f3f3f; }
.w { font-size: 13px; font-weight: 700; fill: #fff; }
</style>

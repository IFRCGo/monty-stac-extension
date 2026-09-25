<script setup lang="ts">
// Levels of integration as a roadmap. Level colours: validated blue ordinal ramp (light -> dark).
// Every step is a place to stop; level 2 is optional (level 3 can come without it).
const levels = [
  { n: 0, title: 'Today', adds: ['Events, hazards,', 'impacts, responses'], stop: ['No change. Exposure', 'stays mixed with impact'], effort: 'effort: none', c: '#86b6ef', t: '#0d1f33' },
  { n: 1, title: 'Event-linked exposure', adds: ['Exposure separate', 'from impact'], stop: ['Credible figures;', 'exposure for every event'], effort: 'effort: low', c: '#5598e7', t: '#0d1f33' },
  { n: 2, title: 'Pre-event occurrences', adds: ['Forecast hazards and', 'exposure before an event'], stop: ['Anticipatory action'], effort: 'effort: medium', c: '#2a78d6', t: '#fff', optional: true },
  { n: 3, title: 'Analytical results', adds: ['People-in-need estimates,', 'linked to their inputs'], stop: ['North-star figure', 'in the catalogue'], effort: 'effort: medium', c: '#1c5cab', t: '#fff' },
  { n: 4, title: 'Context catalogue', adds: ['Population, vulnerability,', 'coping, baseline hazards'], stop: ['All inputs in one place;', 'preparedness'], effort: 'effort: high · scope change', c: '#104281', t: '#fff' },
]
const W = 186, G = 12, X0 = 4
const cx = (i: number) => X0 + i * (W + G) + W / 2
</script>

<template>
  <svg viewBox="0 0 990 330" class="w-full" role="img"
       aria-label="Roadmap of five integration levels, each a possible stopping point">
    <defs>
      <linearGradient id="track" x1="0" x2="1" y1="0" y2="0">
        <stop v-for="(l, i) in levels" :key="l.n" :offset="i / 4" :stop-color="l.c" />
      </linearGradient>
    </defs>
    <!-- skip arc 1 -> 3 -->
    <path :d="`M${cx(1)},36 C${cx(1)},16 ${cx(3)},16 ${cx(3)},36`" fill="none" stroke="#1c5cab" stroke-width="2" stroke-dasharray="6 4" />
    <text :x="cx(2)" y="11" text-anchor="middle" class="skip">level 3 can come without level 2</text>
    <rect :x="cx(0)" y="46" :width="cx(4) - cx(0)" height="5" rx="2.5" fill="url(#track)" />
    <g v-for="(l, i) in levels" :key="l.n">
      <circle :cx="cx(i)" cy="48" r="20" :fill="l.c" stroke="#fff" stroke-width="3" />
      <circle :cx="cx(i)" cy="48" r="22" fill="none" :stroke="l.c" stroke-width="2" />
      <text :x="cx(i)" y="55" text-anchor="middle" class="num" :fill="l.t">{{ l.n }}</text>
      <!-- card -->
      <rect :x="X0 + i * (W + G)" y="84" :width="W" height="110" rx="8" :fill="l.c" fill-opacity="0.12"
            :stroke="l.c" :stroke-width="l.optional ? 2 : 1" :stroke-dasharray="l.optional ? '6 4' : 'none'" />
      <text :x="X0 + i * (W + G) + 12" y="110" class="ttl">{{ l.title }}</text>
      <text v-for="(a, k) in l.adds" :key="k" :x="X0 + i * (W + G) + 12" :y="136 + k * 18" class="body">{{ a }}</text>
      <!-- stop badge -->
      <rect :x="X0 + i * (W + G)" y="206" :width="W" height="68" rx="6" fill="#fff3ec" />
      <rect :x="X0 + i * (W + G)" y="206" width="4" height="68" fill="#cf3f02" />
      <text :x="X0 + i * (W + G) + 12" y="226" class="stop">Stop here:</text>
      <text v-for="(s, k) in l.stop" :key="k" :x="X0 + i * (W + G) + 12" :y="244 + k * 16" class="sb">{{ s }}</text>
      <text :x="cx(i)" y="296" text-anchor="middle" class="eff">{{ l.effort }}</text>
    </g>
  </svg>
</template>

<style scoped>
.skip { font-size: 12px; fill: #1c5cab; }
.num { font-size: 18px; font-weight: 700; }
.ttl { font-size: 15px; font-weight: 700; fill: #2b2b2b; }
.body { font-size: 13px; fill: #3f3f3f; }
.stop { font-size: 12px; font-weight: 700; fill: #cf3f02; }
.sb { font-size: 12px; fill: #3f3f3f; }
.eff { font-size: 11px; fill: #666; }
</style>

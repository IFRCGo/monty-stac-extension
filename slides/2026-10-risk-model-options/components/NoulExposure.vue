<script setup lang="ts">
// GDACS NOUL-26 (eventid 1001294) population in the 39 kt and 74 kt wind fields per track point,
// read from the GDACS timeline on 2026-08-03 (discussion #110). Observed points are filled,
// forecast points hollow; the forecast segment is dashed.
const pts = [
  { t: '25 Jul 06h', obs: true, p39: 75490475, p74: 614941 },
  { t: '25 Jul 18h', obs: true, p39: 103014755, p74: 11167854 },
  { t: '26 Jul 00h', obs: true, p39: 80042232, p74: 10640921 },
  { t: '26 Jul 12h', obs: false, p39: 14518892, p74: 0 },
  { t: '27 Jul 00h', obs: false, p39: 0, p74: 0 },
]
const series = [
  { key: 'p39' as const, name: 'inside 39 kt wind field', color: '#1baf7a' },
  { key: 'p74' as const, name: 'inside 74 kt wind field', color: '#0e6e4c' },
]
const x0 = 90, x1 = 700, y0 = 240, y1 = 30, max = 120e6
const sx = (i: number) => x0 + (i / (pts.length - 1)) * (x1 - x0)
const sy = (v: number) => y0 - (v / max) * (y0 - y1)
const seg = (k: 'p39' | 'p74', from: number, to: number) =>
  pts.slice(from, to + 1).map((p, j) => `${j ? 'L' : 'M'}${sx(from + j)},${sy(p[k])}`).join(' ')
const yt = [0, 40e6, 80e6, 120e6]
const fmtM = (v: number) => `${(v / 1e6).toFixed(v >= 10e6 ? 0 : 1)} M`
</script>

<template>
  <svg viewBox="0 0 960 300" class="w-full" role="img" aria-label="NOUL-26 population inside the 39 and 74 knot wind fields, observed then forecast">
    <g v-for="t in yt" :key="t">
      <line :x1="x0" :y1="sy(t)" :x2="x1" :y2="sy(t)" stroke="#e6e6e6" stroke-width="1" />
      <text :x="x0 - 10" :y="sy(t) + 4" text-anchor="end" class="tk">{{ t ? `${t / 1e6} M` : '0' }}</text>
    </g>
    <line :x1="sx(2)" :y1="y1 - 10" :x2="sx(2)" :y2="y0" stroke="#777" stroke-width="1.5" stroke-dasharray="4 4" />
    <text :x="sx(2)" :y="y1 - 14" text-anchor="middle" class="tk">advisory 13 issued, 26 Jul 00h</text>
    <text :x="sx(1)" :y="y0 + 40" text-anchor="middle" class="ph">observed</text>
    <text :x="sx(3.5)" :y="y0 + 40" text-anchor="middle" class="ph">forecast</text>
    <g v-for="(p, i) in pts" :key="p.t">
      <text :x="sx(i)" :y="y0 + 20" text-anchor="middle" class="tk">{{ p.t }}</text>
    </g>
    <g v-for="s in series" :key="s.key">
      <path :d="seg(s.key, 0, 2)" fill="none" :stroke="s.color" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
      <path :d="seg(s.key, 2, 4)" fill="none" :stroke="s.color" stroke-width="2" stroke-dasharray="6 5" stroke-linecap="round" />
      <circle v-for="(p, i) in pts" :key="i" :cx="sx(i)" :cy="sy(p[s.key])" r="5"
              :fill="p.obs ? s.color : '#fff'" :stroke="p.obs ? '#fff' : s.color" stroke-width="2">
        <title>{{ p.t }} ({{ p.obs ? 'observed' : 'forecast' }}): {{ p[s.key].toLocaleString('en-US') }} people {{ s.name }}</title>
      </circle>
    </g>
    <text :x="sx(1)" :y="sy(pts[1].p39) - 12" text-anchor="middle" class="vl">103 M</text>
    <text :x="sx(1)" :y="sy(pts[1].p74) - 12" text-anchor="middle" class="vl">11.2 M</text>
    <!-- legend -->
    <g v-for="(s, i) in series" :key="s.name" :transform="`translate(740, ${70 + i * 26})`">
      <line x1="0" y1="0" x2="22" y2="0" :stroke="s.color" stroke-width="3" />
      <text x="30" y="4" class="lg">{{ s.name }}</text>
    </g>
    <g transform="translate(740, 136)">
      <circle cx="5" cy="0" r="5" fill="#555" /><text x="16" y="4" class="lg">observed</text>
      <circle cx="95" cy="0" r="5" fill="#fff" stroke="#555" stroke-width="2" /><text x="106" y="4" class="lg">forecast</text>
    </g>
    <text x="740" y="185" class="note">People in the wind field:</text>
    <text x="740" y="203" class="note"><tspan font-weight="700">exposure</tspan>, not people affected.</text>
    <text x="740" y="221" class="note">Filed as impact today.</text>
    <text :x="x0" y="298" class="cap">Source: GDACS timeline, eventid 1001294, read 2026-08-03 (#110)</text>
  </svg>
</template>

<style scoped>
.tk { font-size: 12px; fill: #777; }
.ph { font-size: 13px; font-weight: 700; fill: #3f3f3f; }
.vl { font-size: 12px; font-weight: 700; fill: #3f3f3f; }
.lg { font-size: 12px; fill: #3f3f3f; }
.note { font-size: 13px; fill: #3f3f3f; }
.cap { font-size: 11px; fill: #777; }
</style>

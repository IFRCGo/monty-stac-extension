<script setup lang="ts">
// Two panels: a hazard occurrence lives on a time axis (observed, then forecast);
// a baseline hazard has no time, only a return period. Values are illustrative.
const HAZ = '#cf3f02'
const track = [
  { x: 90, label: '25 Jul 06h', obs: true },
  { x: 170, label: '25 Jul 18h', obs: true },
  { x: 250, label: '26 Jul 00h', obs: true },
  { x: 330, label: '26 Jul 12h', obs: false },
  { x: 410, label: '27 Jul 00h', obs: false },
]
// return period (years) -> depth (m), plotted on a log x axis
const rp = [
  { t: 10, d: 0.5 },
  { t: 100, d: 1.4 },
  { t: 1000, d: 2.3 },
]
const x0 = 600, x1 = 900, y0 = 230, y1 = 70
const lx = (t: number) => x0 + ((Math.log10(t) - 1) / 2) * (x1 - x0)
const ly = (d: number) => y0 - (d / 2.5) * (y0 - y1)
const path = rp.map((p, i) => `${i ? 'L' : 'M'}${lx(p.t)},${ly(p.d)}`).join(' ')
</script>

<template>
  <svg viewBox="0 0 980 300" class="w-full" role="img"
       aria-label="A hazard occurrence sits on a time axis; a baseline hazard has only a return period">
    <!-- Left: occurrence -->
    <text x="40" y="28" class="h">Occurrence — has a time</text>
    <line x1="60" y1="160" x2="450" y2="160" class="axis" />
    <line x1="250" y1="70" x2="250" y2="200" class="now" />
    <text x="250" y="62" text-anchor="middle" class="m">issue time</text>
    <g v-for="p in track" :key="p.x">
      <circle :cx="p.x" cy="160" r="8" :fill="p.obs ? HAZ : '#fff'" :stroke="HAZ" stroke-width="2.5">
        <title>{{ p.label }} — {{ p.obs ? 'observed' : 'forecast' }}</title>
      </circle>
      <text :x="p.x" y="188" text-anchor="middle" class="s">{{ p.label }}</text>
    </g>
    <text x="170" y="130" text-anchor="middle" class="m">observed</text>
    <text x="370" y="130" text-anchor="middle" class="m">forecast</text>
    <rect x="60" y="222" width="390" height="46" rx="6" class="note" />
    <text x="255" y="242" text-anchor="middle" class="s"><tspan font-weight="700">Case A</tspan> — the forecast exists</text>
    <text x="255" y="259" text-anchor="middle" class="s">before anybody declares an event</text>

    <line x1="520" y1="20" x2="520" y2="280" class="sep" />

    <!-- Right: baseline -->
    <text x="560" y="28" class="h">Baseline — no time</text>
    <line :x1="x0" :y1="y0" :x2="x1" :y2="y0" class="axis" />
    <line :x1="x0" :y1="y0" :x2="x0" :y2="y1 - 10" class="axis" />
    <g v-for="t in [10, 100, 1000]" :key="t">
      <line :x1="lx(t)" :y1="y0" :x2="lx(t)" :y2="y0 + 5" class="axis" />
      <text :x="lx(t)" :y="y0 + 20" text-anchor="middle" class="s">{{ t }} yr</text>
    </g>
    <text :x="(x0 + x1) / 2" :y="y0 + 40" text-anchor="middle" class="m">return period</text>
    <text :x="x0 - 12" :y="y1 - 16" text-anchor="start" class="m">flood depth (illustrative)</text>
    <path :d="path" fill="none" :stroke="HAZ" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
    <g v-for="p in rp" :key="p.t">
      <circle :cx="lx(p.t)" :cy="ly(p.d)" r="6" :fill="HAZ" stroke="#fff" stroke-width="2">
        <title>1-in-{{ p.t }}-year flood: {{ p.d }} m (illustrative)</title>
      </circle>
      <text :x="lx(p.t) - 10" :y="ly(p.d) - 10" text-anchor="end" class="s">1 map</text>
    </g>
    <text x="750" y="292" text-anchor="middle" class="s"><tspan font-weight="700">Case B</tspan> — one map per return period · never an event</text>
  </svg>
</template>

<style scoped>
.h { font-size: 17px; font-weight: 700; fill: #3f3f3f; }
.m { font-size: 13px; fill: #555; }
.s { font-size: 12px; fill: #3f3f3f; }
.axis { stroke: #bdbdbd; stroke-width: 1; }
.now { stroke: #777; stroke-width: 1.5; stroke-dasharray: 4 4; }
.sep { stroke: #e3e3e3; stroke-width: 1; }
.note { fill: #fff3ec; stroke: none; }
</style>

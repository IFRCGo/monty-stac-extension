<script setup lang="ts">
// USGS PAGER population exposure by MMI, event us6000pi9w (all countries), log scale.
const EXP = '#1baf7a'
const data = [
  { mmi: 'IV', label: 'light', v: 130864619 },
  { mmi: 'V', label: 'moderate', v: 147452 },
  { mmi: 'VI', label: 'strong', v: 61485 },
  { mmi: 'VII', label: 'very strong', v: 27679 },
  { mmi: 'VIII', label: 'severe', v: 6964 },
  { mmi: 'IX', label: 'violent', v: 2998 },
]
const x0 = 130, x1 = 820, lo = 3, hi = 9 // log10 range: 1 000 .. 1 000 000 000
const sx = (v: number) => x0 + ((Math.log10(v) - lo) / (hi - lo)) * (x1 - x0)
const ticks = [1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
const tickLabel = (t: number) => (t >= 1e9 ? '1B' : t >= 1e6 ? `${t / 1e6}M` : `${t / 1e3}k`)
const fmt = (v: number) => v.toLocaleString('en-US').replace(/,/g, ' ')
const band = 38, bar = 22, top = 20
const barPath = (y: number, v: number) => {
  const x = sx(v), r = 4
  return `M${x0},${y} L${x - r},${y} Q${x},${y} ${x},${y + r} L${x},${y + bar - r} Q${x},${y + bar} ${x - r},${y + bar} L${x0},${y + bar} Z`
}
</script>

<template>
  <svg viewBox="0 0 960 300" class="w-full" role="img" aria-label="Population exposed by shaking intensity, log scale">
    <g v-for="t in ticks" :key="t">
      <line :x1="sx(t)" :y1="top - 6" :x2="sx(t)" :y2="top + band * data.length" class="grid" />
      <text :x="sx(t)" :y="top + band * data.length + 16" text-anchor="middle" class="tk">{{ tickLabel(t) }}</text>
    </g>
    <g v-for="(d, i) in data" :key="d.mmi">
      <text :x="x0 - 10" :y="top + i * band + bar / 2 + 5" text-anchor="end" class="yl">MMI {{ d.mmi }} <tspan class="sub">{{ d.label }}</tspan></text>
      <path :d="barPath(top + i * band, d.v)" :fill="EXP">
        <title>MMI {{ d.mmi }} ({{ d.label }}): {{ fmt(d.v) }} people</title>
      </path>
      <text :x="sx(d.v) + 8" :y="top + i * band + bar / 2 + 5" class="vl">{{ fmt(d.v) }}</text>
    </g>
    <!-- brackets -->
    <line x1="880" :y1="top" x2="880" :y2="top + band * 2 - 10" class="br" />
    <text x="890" :y="top + 30" class="bt">little or</text>
    <text x="890" :y="top + 46" class="bt">no damage</text>
    <line x1="880" :y1="top + band * 2" x2="880" :y2="top + band * 6 - 10" class="br" />
    <text x="890" :y="top + band * 4 - 8" class="bt">damaging</text>
    <text x="890" :y="top + band * 4 + 8" class="bt">(VI+)</text>
    <text :x="x0" y="296" class="cap">People exposed, all countries · log scale · source: USGS PAGER exposures.json</text>
  </svg>
</template>

<style scoped>
.grid { stroke: #e6e6e6; stroke-width: 1; }
.tk { font-size: 12px; fill: #777; }
.yl { font-size: 14px; font-weight: 600; fill: #3f3f3f; }
.sub { font-size: 11px; font-weight: 400; fill: #777; }
.vl { font-size: 13px; fill: #3f3f3f; }
.br { stroke: #777; stroke-width: 1.5; }
.bt { font-size: 12px; fill: #3f3f3f; }
.cap { font-size: 11px; fill: #777; }
</style>

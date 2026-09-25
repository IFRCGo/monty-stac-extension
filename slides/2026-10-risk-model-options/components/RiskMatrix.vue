<script setup lang="ts">
// Which arguments of Risk = f(H, E, [V], [C]) each framework uses, and how it partitions them.
// cell: 'use' = argument used · 'merge' = merged with the previous column · 'in' = folded into
// vulnerability · 'phys' = used, physical meaning · '' = not used.
type Cell = '' | 'use' | 'merge' | 'in' | 'phys'
const cols = ['Hazard', 'Exposure', 'Vulnerability', 'Capacity']
const rows: { name: string; cells: Cell[]; note: string }[] = [
  { name: 'UNDRR', cells: ['use', 'use', 'use', 'use'], note: 'four terms' },
  { name: 'INFORM Risk', cells: ['use', 'merge', 'use', 'use'], note: 'hazard & exposure merged' },
  { name: 'IPCC AR5', cells: ['use', 'use', 'use', 'in'], note: 'capacity inside vulnerability' },
  { name: 'Loss models (RDLS, GEM)', cells: ['use', 'use', 'phys', ''], note: 'damage curves' },
  { name: 'Rapid people in need', cells: ['use', 'use', 'use', ''], note: 'per admin unit' },
]
const colX = [330, 450, 570, 690]
const sig = [
  { t: 'Hazard', req: true, x: 116, w: 92 },
  { t: 'Exposure', req: true, x: 218, w: 110 },
  { t: '[Vulnerability]', req: false, x: 340, w: 170 },
  { t: '[Capacity]', req: false, x: 522, w: 128 },
]
const rowY = (i: number) => 150 + i * 44
</script>

<template>
  <svg viewBox="0 0 980 380" class="w-full" role="img"
       aria-label="Arguments of the risk function used by UNDRR, INFORM, IPCC AR5, loss models and the rapid people-in-need estimate">
    <!-- signature -->
    <text x="10" y="40" class="mono">Risk = f(</text>
    <g v-for="a in sig" :key="a.t">
      <rect :x="a.x" y="16" :width="a.w" height="34" rx="6" :class="a.req ? 'req' : 'opt'" />
      <text :x="a.x + a.w / 2" y="39" text-anchor="middle" class="mono" :class="{ muted: !a.req }">{{ a.t }}</text>
    </g>
    <text x="658" y="40" class="mono">, … )</text>
    <rect x="800" y="20" width="66" height="26" rx="6" class="req" /><text x="833" y="38" text-anchor="middle" class="k">always</text>
    <rect x="876" y="20" width="76" height="26" rx="6" class="opt" /><text x="914" y="38" text-anchor="middle" class="k">optional</text>

    <!-- header -->
    <text v-for="(c, i) in cols" :key="c" :x="colX[i]" y="110" text-anchor="middle" class="hd">{{ c }}</text>
    <text x="770" y="110" class="hd">How it partitions</text>
    <line x1="10" y1="122" x2="970" y2="122" class="rule" />

    <!-- rows -->
    <g v-for="(r, ri) in rows" :key="r.name">
      <text x="10" :y="rowY(ri) + 5" class="nm">{{ r.name }}</text>
      <g v-for="(c, i) in r.cells" :key="i">
        <circle v-if="c === 'use' && r.cells[i + 1] !== 'merge'" :cx="colX[i]" :cy="rowY(ri)" r="9" class="dot">
          <title>{{ r.name }} uses {{ cols[i] }}</title>
        </circle>
        <rect v-else-if="c === 'merge'" :x="colX[i - 1] - 9" :y="rowY(ri) - 9" :width="colX[i] - colX[i - 1] + 18" height="18" rx="9" class="dot">
          <title>{{ r.name }} merges {{ cols[i - 1] }} and {{ cols[i] }}</title>
        </rect>
        <g v-else-if="c === 'phys'">
          <circle :cx="colX[i] - 30" :cy="rowY(ri)" r="9" class="dot"><title>{{ r.name }}: physical vulnerability</title></circle>
          <rect :x="colX[i] - 16" :y="rowY(ri) - 11" width="66" height="22" rx="4" class="tag" />
          <text :x="colX[i] + 17" :y="rowY(ri) + 4" text-anchor="middle" class="k">physical</text>
        </g>
        <g v-else-if="c === 'in'">
          <rect :x="colX[i] - 30" :y="rowY(ri) - 11" width="60" height="22" rx="4" class="tag" />
          <text :x="colX[i]" :y="rowY(ri) + 4" text-anchor="middle" class="k">→ in V</text>
        </g>
        <text v-else-if="c === ''" :x="colX[i]" :y="rowY(ri) + 5" text-anchor="middle" class="none">—</text>
      </g>
      <text x="770" :y="rowY(ri) + 5" class="note">{{ r.note }}</text>
    </g>
  </svg>
</template>

<style scoped>
.mono { font-family: "Roboto Mono", ui-monospace, monospace; font-size: 18px; fill: #3f3f3f; }
.mono.muted { fill: #666; }
.req { fill: #f2f2f2; stroke: #3f3f3f; stroke-width: 2; }
.opt { fill: none; stroke: #8a8a8a; stroke-width: 2; stroke-dasharray: 5 4; }
.k { font-size: 12px; fill: #3f3f3f; }
.hd { font-size: 14px; font-weight: 700; fill: #555; }
.rule { stroke: #ddd; stroke-width: 1; }
.nm { font-size: 15px; font-weight: 600; fill: #3f3f3f; }
.dot { fill: #3f3f3f; }
.tag { fill: #fff; stroke: #bbb; stroke-width: 1; }
.none { font-size: 14px; fill: #aaa; }
.note { font-size: 13px; fill: #555; }
</style>

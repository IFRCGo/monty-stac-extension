<script setup lang="ts">
// Which arguments of Risk = f(H, E, [V], [C]) each framework uses, and how it partitions them.
// cell: 'use' = argument used · 'merge' = merged with the previous column · 'in' = folded into another
// argument · 'phys' = used, physical meaning · '' = not used.
type Cell = '' | 'use' | 'merge' | 'in' | 'phys'
const cols = ['Hazard', 'Exposure', 'Vulnerability', 'Capacity']
const rows: { name: string; cells: Cell[]; note: string }[] = [
  { name: 'UNDRR', cells: ['use', 'use', 'use', 'use'], note: 'four terms' },
  { name: 'INFORM Risk', cells: ['use', 'merge', 'use', 'use'], note: 'hazard & exposure in one dimension' },
  { name: 'IPCC AR5', cells: ['use', 'use', 'use', 'in'], note: 'capacity inside vulnerability' },
  { name: 'Loss models (RDLS, GEM)', cells: ['use', 'use', 'phys', ''], note: 'damage curves' },
  { name: 'Rapid people in need', cells: ['use', 'use', 'use', ''], note: 'per admin unit' },
]
</script>

<template>
  <div class="rm">
    <div class="sig">
      <span class="fn">Risk = f(</span>
      <span class="arg req">Hazard</span>,
      <span class="arg req">Exposure</span>,
      <span class="arg opt">[Vulnerability]</span>,
      <span class="arg opt">[Capacity]</span>, …<span class="fn">)</span>
      <span class="key"><span class="arg req mini">always</span><span class="arg opt mini">optional</span></span>
    </div>
    <div class="grid">
      <div class="hd" />
      <div v-for="c in cols" :key="c" class="hd">{{ c }}</div>
      <div class="hd left">How it partitions</div>
      <template v-for="r in rows" :key="r.name">
        <div class="name">{{ r.name }}</div>
        <div v-for="(c, i) in r.cells" :key="i" class="cell" :class="{ bridge: c === 'merge' }">
          <span v-if="c === 'use' && r.cells[i + 1] !== 'merge'" class="dot" :title="`${r.name} uses ${cols[i]}`" />
          <span v-else-if="c === 'phys'" class="dot" :title="`${r.name}: physical vulnerability`" /><span v-if="c === 'phys'" class="tag">physical</span>
          <span v-else-if="c === 'merge'" class="bar" :title="`${r.name} merges ${cols[i - 1]} and ${cols[i]}`" />
          <span v-else-if="c === 'in'" class="tag">→ in V</span>
          <span v-else-if="c === ''" class="none">—</span>
        </div>
        <div class="note">{{ r.note }}</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.rm { margin-top: 0.5rem; }
.sig { font-family: var(--slidev-font-family-mono, monospace); font-size: 1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.35rem; flex-wrap: wrap; }
.arg { padding: 0.1rem 0.5rem; border-radius: 6px; }
.arg.req { border: 2px solid #3f3f3f; background: #f2f2f2; font-weight: 600; }
.arg.opt { border: 2px dashed #8a8a8a; color: #555; }
.arg.mini { font-size: 0.7rem; font-family: var(--slidev-font-family, sans-serif); margin-left: 0.4rem; }
.key { margin-left: auto; display: flex; }
.grid { display: grid; grid-template-columns: 1.7fr repeat(4, 1fr) 2.2fr; row-gap: 0.25rem; align-items: center; font-size: 0.85rem; }
.hd { font-weight: 700; color: #555; text-align: center; padding-bottom: 0.3rem; border-bottom: 1px solid #ddd; }
.hd.left { text-align: left; }
.name { font-weight: 600; padding: 0.35rem 0; }
.cell { display: flex; justify-content: center; align-items: center; gap: 0.3rem; height: 2rem; position: relative; }
.dot { width: 16px; height: 16px; border-radius: 50%; background: #3f3f3f; display: inline-block; }
.bar { position: absolute; right: 50%; width: 100%; height: 16px; border-radius: 8px; background: #3f3f3f; }
.tag { font-size: 0.7rem; color: #3f3f3f; border: 1px solid #bbb; border-radius: 4px; padding: 0 0.3rem; }
.none { color: #aaa; }
.note { color: #555; font-size: 0.78rem; }
</style>

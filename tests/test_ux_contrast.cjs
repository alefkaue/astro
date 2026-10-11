const assert = require('node:assert/strict');
const fs = require('node:fs');
function luminance(hex) {
  const channels = hex.replace('#','').match(/../g).map(c => parseInt(c,16)/255).map(c => c <= .04045 ? c/12.92 : ((c+.055)/1.055)**2.4);
  return channels[0]*.2126 + channels[1]*.7152 + channels[2]*.0722;
}
function ratio(text,bg) { const a=luminance(text),b=luminance(bg); return (Math.max(a,b)+.05)/(Math.min(a,b)+.05); }
const css = fs.readFileSync('static/astro.css','utf8');
const themes = [...css.matchAll(/--muted:(#[0-9A-Fa-f]{6}); --faint:(#[0-9A-Fa-f]{6})/g)];
assert.equal(themes.length,2);
for (const [index,backgrounds] of [['#FFFFFF','#F2F2F2','#E2E2E2'],['#0A0A0A','#141414','#242424','#3A3A3A']].entries()) {
  for (const bg of backgrounds) {
    const before = ratio(index ? '#8C8C8C' : '#6B6B6B',bg);
    const after = ratio(themes[index][1],bg);
    assert.ok(after >= 4.5, `Secondary text ${themes[index][1]} on ${bg}: ${after}`);
    assert.ok(ratio(themes[index][2],bg) >= 4.5);
    console.log(`${index ? 'Dark' : 'Light'} / ${bg}: ${before.toFixed(2)} → ${after.toFixed(2)}:1`);
  }
}

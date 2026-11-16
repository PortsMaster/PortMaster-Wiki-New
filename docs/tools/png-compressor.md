---
title: PNG Compressor - PortMaster Wiki

# Nothing here for glightbox to wrap at build time - the comparison images
# are both injected client-side, after a visitor picks or drops a file.
# Same reasoning as games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# PNG Compressor

Shrink a `screenshot.png` or `cover.png` without leaving your browser.

Needs one at 640x480 first? The [Screenshot Resizer](screenshot-resizer.md) makes
those, and the [Cover Generator](cover-generator.md) builds covers.

A screenshot straight out of a capture tool is usually a 24 or 32 bit PNG, which
stores a full colour value for every pixel. Cutting it down to a palette of at
most 256 colours typically saves 70-90% with no visible difference, which is what
[pngquant](https://pngquant.org/){:target="_blank" rel="noopener"} is for.

This page runs pngquant's own quantiser, libimagequant, compiled to WebAssembly
([wasm-pngquant](https://github.com/JanTrueno/wasm-pngquant){:target="_blank" rel="noopener"},
GPLv3), so the result is what `pngquant --quality 0-N` would give you. It all
happens in your browser: nothing is uploaded and nothing has to be installed.

## Pick your PNG

<div class="porter-tool">
  <div class="pq-setup">
    <div class="im-slot" data-slot="source">
      <div class="im-slot-preview"><i class="bi bi-file-earmark-image"></i></div>
      <div class="im-slot-body">
        <label for="pqSource">Image</label>
        <input type="file" id="pqSource" accept="image/*">
        <p class="help-text">Drop an image on this card, click it to browse, or paste one from your clipboard.</p>
      </div>
    </div>

    <div class="pq-controls">
      <div class="form-group">
        <label for="pqQuality">Quality <span class="pq-value" id="pqQualityValue">80</span></label>
        <input type="range" id="pqQuality" min="10" max="100" step="1" value="80">
        <p class="help-text" id="pqQualityNote">Fewer colours means a smaller file and, past a point, visible banding.</p>
      </div>

      <div class="form-group">
        <label class="filter-checkbox-item pq-dither">
          <input type="checkbox" id="pqDither" checked>
          <span>Dither</span>
        </label>
        <p class="help-text">Trades a little noise for smoother gradients. Worth turning off for pixel art, where it only makes the file bigger.</p>
      </div>
    </div>
  </div>
</div>

## Before and after

<div class="porter-tool">
  <div class="pq-result" id="pqResult" hidden>
    <div class="pq-compare" id="pqCompare">
      <img id="pqAfterImg" alt="Compressed image">
      <div class="pq-compare-overlay" id="pqOverlay">
        <img id="pqBeforeImg" alt="Original image">
      </div>
      <span class="pq-tag pq-tag-left">Original</span>
      <span class="pq-tag pq-tag-right">Compressed</span>
      <div class="pq-compare-handle" id="pqHandle" role="slider" tabindex="0"
           aria-label="Reveal more of the original or the compressed image"
           aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"></div>
    </div>

    <div class="pq-sizes" id="pqSizes"></div>
  </div>

  <p class="im-empty" id="pqEmpty">Pick an image to get started.</p>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="pqDownload" disabled>
      <i class="bi bi-download"></i> Download PNG
    </button>
    <button type="button" class="secondary-btn" id="pqReset">Start over</button>
  </div>
</div>

<script>
(function () {
  const input = document.getElementById('pqSource');
  const slot = input.closest('.im-slot');
  const preview = slot.querySelector('.im-slot-preview');
  const quality = document.getElementById('pqQuality');
  const qualityValue = document.getElementById('pqQualityValue');
  const qualityNote = document.getElementById('pqQualityNote');
  const dither = document.getElementById('pqDither');
  const result = document.getElementById('pqResult');
  const emptyMsg = document.getElementById('pqEmpty');
  const beforeImg = document.getElementById('pqBeforeImg');
  const afterImg = document.getElementById('pqAfterImg');
  const compare = document.getElementById('pqCompare');
  const overlay = document.getElementById('pqOverlay');
  const handle = document.getElementById('pqHandle');
  const sizes = document.getElementById('pqSizes');
  const downloadBtn = document.getElementById('pqDownload');
  const resetBtn = document.getElementById('pqReset');

  let sourceName = 'screenshot.png';
  let sourceBytes = 0;      // the file as it arrived, for the "before" figure
  let sourceUrl = null;
  let pixels = null;        // ImageData of the decoded source
  let resultUrl = null;
  let resultBlob = null;
  let runId = 0;            // guards against a slow run overwriting a newer one
  let debounce = null;

  // ===================================================================
  // pngquant (libimagequant compiled to WebAssembly)
  // ===================================================================

  // Fetched on first use rather than on page load, so nobody pays for the
  // ~250 KB module unless they actually drop an image in. Resolved against
  // the page URL, which is /tools/png-compressor/.
  const WASM_JS = '../../assets/wasm/pngquant/wasm_pngquant.js';
  let pngquant = null;

  function loadPngquant() {
    if (!pngquant) {
      pngquant = import(WASM_JS).then(async (mod) => {
        await mod.default();
        return mod;
      });
      // A failed load shouldn't stick: let the next image try again.
      pngquant.catch(() => { pngquant = null; });
    }
    return pngquant;
  }

  // Same scale and same meaning as pngquant's --speed: 1 is slowest and
  // best, 10 fastest. 3 is pngquant's own default, and a 640x480
  // screenshot still comes back in well under a second.
  const SPEED = 3;

  // The PNG pngquant writes is already final, so the only thing left to do
  // with it is report what it chose: palette size from PLTE, bits per
  // pixel from IHDR.
  function describePng(bytes) {
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    let depth = 8, colours = 0;
    for (let at = 8; at + 8 <= bytes.length;) {
      const len = view.getUint32(at);
      const type = String.fromCharCode(bytes[at + 4], bytes[at + 5], bytes[at + 6], bytes[at + 7]);
      if (type === 'IHDR') depth = bytes[at + 16];
      else if (type === 'PLTE') colours = len / 3;
      else if (type === 'IDAT' || type === 'IEND') break;
      at += 12 + len;
    }
    return { depth, colours };
  }

  // ===================================================================
  // Wiring
  // ===================================================================

  function formatBytes(n) {
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
    return (n / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }

  function setBusy(on) {
    compare.classList.toggle('is-busy', on);
    downloadBtn.disabled = on || !resultBlob;
  }

  async function compress() {
    if (!pixels) return;
    const id = ++runId;
    setBusy(true);
    // Let the browser paint the busy state before the main thread goes away
    // for however long the quantiser takes.
    await new Promise(r => setTimeout(r, 0));
    if (id !== runId) return;

    let bytes;
    try {
      const pq = await loadPngquant();
      if (id !== runId) return;
      // Minimum quality 0, i.e. pngquant --quality 0-N: always hand back
      // the best palette it can at or under the target rather than giving
      // up when an image can't reach some floor.
      bytes = pq.compress_png(pixels.data, pixels.width, pixels.height,
        0, Number(quality.value), dither.checked ? 1.0 : 0.0, SPEED);
    } catch (e) {
      if (id !== runId) return;
      sizes.textContent = 'Could not load or run pngquant: ' + (e && e.message ? e.message : e);
      setBusy(false);
      return;
    }
    if (id !== runId) return;
    const blob = new Blob([bytes], { type: 'image/png' });
    const info = describePng(bytes);

    if (resultUrl) URL.revokeObjectURL(resultUrl);
    resultBlob = blob;
    resultUrl = URL.createObjectURL(blob);
    afterImg.src = resultUrl;

    const delta = sourceBytes ? Math.round((1 - blob.size / sourceBytes) * 100) : 0;

    // Coming out bigger is a real outcome, not an error, and it has two
    // causes worth telling apart. Dithering on flat art is by far the
    // common one: the noise it sprays over every solid region is exactly
    // the kind of thing deflate cannot pack, and switching it off can turn
    // "3x bigger" into "half the size" on the same image.
    let hint = '';
    if (delta <= 0) {
      hint = dither.checked
        ? '<span class="pq-hint">Dithering is doing this - on flat artwork it adds noise that will not compress. Try it off.</span>'
        : '<span class="pq-hint">This PNG is already well packed, so a palette version has nothing to win back.</span>';
    }

    sizes.innerHTML =
      '<span class="pq-size"><strong>Original</strong> ' + formatBytes(sourceBytes) + '</span>' +
      '<span class="pq-size"><strong>Compressed</strong> ' + formatBytes(blob.size) + '</span>' +
      '<span class="pq-size pq-delta ' + (delta > 0 ? 'is-smaller' : 'is-bigger') + '">' +
      (delta > 0 ? delta + '% smaller' : Math.abs(delta) + '% bigger') + '</span>' + hint;

    qualityNote.textContent = info.colours + ' colour palette at ' +
      info.depth + ' bits per pixel.';

    setBusy(false);
  }

  function schedule() {
    clearTimeout(debounce);
    debounce = setTimeout(compress, 180);
  }

  async function handleFile(file) {
    if (!file || !file.type || !file.type.startsWith('image/')) {
      reset();
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      return;
    }

    if (sourceUrl) URL.revokeObjectURL(sourceUrl);
    sourceUrl = URL.createObjectURL(file);
    sourceBytes = file.size;
    sourceName = file.name && /\.png$/i.test(file.name) ? file.name : 'screenshot.png';

    try {
      const img = await loadImage(sourceUrl);
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(img, 0, 0);
      pixels = ctx.getImageData(0, 0, img.width, img.height);

      preview.innerHTML = '';
      const thumb = new Image();
      thumb.src = sourceUrl;
      thumb.alt = '';
      preview.appendChild(thumb);
      slot.classList.add('is-filled');

      beforeImg.src = sourceUrl;
      // Locks the box to the source's shape so the two layers stay aligned
      // while the compressed image is still being written.
      compare.style.aspectRatio = img.width + ' / ' + img.height;
      result.hidden = false;
      emptyMsg.style.display = 'none';
      setPosition(50);
      await compress();
    } catch (e) {
      reset();
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
    }
  }

  function reset() {
    runId++;
    pixels = null;
    resultBlob = null;
    sourceBytes = 0;
    if (resultUrl) { URL.revokeObjectURL(resultUrl); resultUrl = null; }
    if (sourceUrl) { URL.revokeObjectURL(sourceUrl); sourceUrl = null; }
    input.value = '';
    slot.classList.remove('is-filled', 'is-dragover');
    preview.innerHTML = '<i class="bi bi-file-earmark-image"></i>';
    beforeImg.removeAttribute('src');
    afterImg.removeAttribute('src');
    sizes.textContent = '';
    result.hidden = true;
    emptyMsg.style.display = '';
    downloadBtn.disabled = true;
    compare.classList.remove('is-busy');
    qualityNote.textContent = 'Fewer colours means a smaller file and, past a point, visible banding.';
  }

  // ===== Comparison slider =====
  function setPosition(pct) {
    const clamped = Math.max(0, Math.min(100, pct));
    compare.style.setProperty('--pq-pos', clamped + '%');
    handle.setAttribute('aria-valuenow', Math.round(clamped));
  }

  function positionFromEvent(e) {
    const box = compare.getBoundingClientRect();
    setPosition(((e.clientX - box.left) / box.width) * 100);
  }

  // Pointer events rather than mouse+touch pairs: one code path covers a
  // mouse, a finger and a stylus, and capture keeps the drag alive when the
  // pointer leaves the box.
  let dragging = 0;

  compare.addEventListener('pointerdown', (e) => {
    if (result.hidden) return;
    dragging = e.pointerId;
    // Capture is a nicety - it keeps events coming when the pointer leaves
    // the box - but it throws on a pointer the browser no longer considers
    // active, and the drag itself must not depend on it having worked.
    try { compare.setPointerCapture(e.pointerId); } catch (err) { /* not fatal */ }
    compare.classList.add('is-dragging');
    positionFromEvent(e);
  });

  compare.addEventListener('pointermove', (e) => {
    if (dragging !== e.pointerId) return;
    positionFromEvent(e);
  });

  ['pointerup', 'pointercancel'].forEach(evt => compare.addEventListener(evt, (e) => {
    if (dragging !== e.pointerId) return;
    dragging = 0;
    try { compare.releasePointerCapture(e.pointerId); } catch (err) { /* already gone */ }
    compare.classList.remove('is-dragging');
  }));

  handle.addEventListener('keydown', (e) => {
    const step = e.shiftKey ? 10 : 2;
    const now = Number(handle.getAttribute('aria-valuenow'));
    if (e.key === 'ArrowLeft') setPosition(now - step);
    else if (e.key === 'ArrowRight') setPosition(now + step);
    else if (e.key === 'Home') setPosition(0);
    else if (e.key === 'End') setPosition(100);
    else return;
    e.preventDefault();
  });

  // ===== Slot: click, native picker, drag-and-drop or paste =====
  input.addEventListener('change', () => {
    handleFile(input.files && input.files[0]);
  });

  slot.addEventListener('click', (e) => {
    if (e.target === input || e.target.closest('label[for]')) return;
    input.click();
  });

  ['dragenter', 'dragover'].forEach(evt => slot.addEventListener(evt, (e) => {
    e.preventDefault(); // required or the browser rejects the drop outright
    slot.classList.add('is-dragover');
  }));

  slot.addEventListener('dragleave', (e) => {
    if (slot.contains(e.relatedTarget)) return;
    slot.classList.remove('is-dragover');
  });

  slot.addEventListener('drop', (e) => {
    e.preventDefault();
    slot.classList.remove('is-dragover');
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (!file) return;
    input.files = e.dataTransfer.files;
    handleFile(file);
  });

  document.addEventListener('paste', (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.kind !== 'file' || !item.type.startsWith('image/')) continue;
      const file = item.getAsFile();
      if (!file) continue;
      e.preventDefault();
      input.value = '';
      handleFile(file);
      return;
    }
  });

  quality.addEventListener('input', () => {
    qualityValue.textContent = quality.value;
    schedule();
  });

  dither.addEventListener('change', schedule);

  downloadBtn.addEventListener('click', () => {
    if (!resultBlob) return;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(resultBlob);
    a.download = sourceName;
    a.click();
    // Revoking immediately can cancel the download in some browsers.
    setTimeout(() => URL.revokeObjectURL(a.href), 10000);
  });

  resetBtn.addEventListener('click', () => {
    reset();
    quality.value = 80;
    qualityValue.textContent = '80';
    dither.checked = true;
  });

  setPosition(50);
})();
</script>

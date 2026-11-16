# wasm-pngquant

Used by the PNG Compressor page (`docs/tools/png-compressor.md`).

libimagequant (pngquant's quantiser) compiled to WebAssembly. Source:
https://github.com/JanTrueno/wasm-pngquant, a fork of
https://github.com/kloptops/wasm-pngquant that adds a
`compress_png(rgba, width, height, quality_min, quality_max, dither, speed)`
export, so the page's quality slider and dither toggle can drive it. GPLv3: see
`LICENSE` in this folder.

Rebuild from the wasm-pngquant source:

```bash
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version 0.2.128 --locked
cargo build --release --target wasm32-unknown-unknown
wasm-bindgen --target web --out-dir pkg target/wasm32-unknown-unknown/release/wasm_pngquant.wasm
cp pkg/wasm_pngquant.js pkg/wasm_pngquant_bg.wasm <this folder>
```

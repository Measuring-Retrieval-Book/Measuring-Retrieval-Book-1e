const fs = require("fs");
const path = require("path");
const sharp = require("sharp");

const root = path.resolve(__dirname, "..");
const directory = path.join(root, "assets", "diagrams");
const files = fs.readdirSync(directory).filter((name) => name.endsWith(".svg")).sort();

async function render() {
  const width = 4;
  for (let start = 0; start < files.length; start += width) {
    const batch = files.slice(start, start + width);
    await Promise.all(batch.map(async (name) => {
      const source = path.join(directory, name);
      const target = source.replace(/\.svg$/, ".png");
      await sharp(source, { density: 220 }).png({ compressionLevel: 9 }).toFile(target);
    }));
    const complete = Math.min(start + width, files.length);
    if (complete % 24 === 0 || complete === files.length) {
      console.log(`Rendered ${complete}/${files.length} diagrams`);
    }
  }
}

render().catch((error) => {
  console.error(error);
  process.exit(1);
});

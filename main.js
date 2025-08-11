import { Actor } from 'apify';
import { execSync } from 'child_process';
import fs from 'fs';

await Actor.init();

console.log("Démarrage du scraper Python...");
execSync('python3 scraper.py', { stdio: 'inherit' });

console.log("Lecture du fichier output.json...");
const data = fs.readFileSync('output.json', 'utf-8');
const items = JSON.parse(data);

console.log(`Export ${items.length} annonces`);
await Actor.pushData(items);

await Actor.exit();

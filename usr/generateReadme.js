import fs from 'fs/promises'; // Import fs with promises
import { calculateAge } from './calculateAge.js';
import { getGitHubStats } from './getStats.js';

// Function to generate Neofetch-style SVG
async function generateNeofetchSVG(ascii, otherInfo) {
	const svgWidth = 800;
	const svgHeight = 600;
	const lineHeight = 20;
	const fontSize = 16;
	const marginLeft = 20;
	const marginTop = 40;

	let svgContent = `<svg width="${svgWidth}" height="${svgHeight}" xmlns="http://www.w3.org/2000/svg">`;

	// Function to create text elements for each line
	function createTextElement(text, x, y) {
		return `<text x="${x}" y="${y}" font-family="Arial" font-size="${fontSize}" fill="white">${text}</text>`;
	}

	// Split the info into lines and add them to the SVG
	const lines = otherInfo.split('\n');
	lines.forEach((line, index) => {
		svgContent += createTextElement(
			line,
			marginLeft,
			marginTop + index * lineHeight
		);
	});

	// Add ASCII art to the SVG
	svgContent += `<foreignObject x="${marginLeft}" y="${
		marginTop + lines.length * lineHeight
	}" width="${svgWidth - marginLeft * 2}" height="${
		svgHeight - (marginTop + lines.length * lineHeight)
	}"><pre>${ascii}</pre></foreignObject>`;

	svgContent += '</svg>';
	return svgContent;
}

// Function to write SVG content to README file
async function writeToREADME(svgContent) {
	try {
		await fs.writeFile('README.md', svgContent);
		console.log('SVG content has been written to README.md');
	} catch (error) {
		console.error('Error writing SVG content to README.md:', error);
	}
}

// Function to read ASCII art from file
async function readAsciiArt() {
	try {
		return await fs.readFile('jellyfish30.txt', 'utf8');
	} catch (error) {
		console.error('Error reading ASCII art file:', error);
		throw error;
	}
}

// Main function
async function main() {
	try {
		// Read ASCII art
		const ascii = await readAsciiArt();

		// Get GitHub stats
		const githubStatsData = await getGitHubStats(
			process.env.GITHUB_TOKEN,
			process.env.GITHUB_USERNAME
		);

		// Generate other information
		const otherInfo = await generateOtherInfo(githubStatsData);

		// Generate Neofetch-style SVG
		const neofetchSVG = await generateNeofetchSVG(ascii, otherInfo);

		await writeToREADME(neofetchSVG);

		// Write SVG content to a file
		await fs.writeFile('neofetch.svg', neofetchSVG);

		console.log('Neofetch-style SVG generated successfully.');
	} catch (error) {
		console.error('Error generating Neofetch-style SVG:', error);
	}
}

// Function to generate other information
async function generateOtherInfo(githubStats) {
	try {
		let otherInfo = '';

		otherInfo += `          Su401@Github\n`;
		otherInfo += `            OS: A coffee fueled brain\n`;
		otherInfo += `          Host: A very tired body\n`;
		otherInfo += `        Kernel: Trauma\n`;
		otherInfo += `        Uptime: ${calculateAge('2000-10-04')}\n`; // Provide birthday directly
		otherInfo += `         Shell: DAIKAN - Direct Assertive Individual Known for Abrasive Nature\n`;
		otherInfo += `         Theme: Dark because light attracts bugs\n`;
		otherInfo += `       Memory: Very weak\n`;
		otherInfo += `GitHub Stats:\n`;
		otherInfo += `  Repositories Count: ${githubStats.repositoryCount}\n`;
		otherInfo += `  Total Contributions: ${githubStats.totalContributions}\n`;
		otherInfo += `  Languages Percentage:\n`;
		for (const language in githubStats.languagePercentages) {
			otherInfo += `    ${language}: ${githubStats.languagePercentages[language]}%\n`;
		}

		return otherInfo;
	} catch (error) {
		console.error('Error generating GitHub stats:', error);
		throw error;
	}
}

// Call the main function
main();

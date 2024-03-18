// generateReadme.js
import boxen from 'boxen';
import chalk from 'chalk';
import fs from 'fs';
import { calculateAge } from './calculateAge.js';
import { getGitHubStats } from './getStats.js';

// Replace with your birthday in yyyy-mm-dd format
const birthday = '2000-10-04';

async function main() {
	// Import ASCII art
	const ascii = fs.readFileSync('jellyfish30.txt', 'utf8');

	try {
		const githubStatsData = await getGitHubStats(
			process.env.GITHUB_TOKEN,
			process.env.GITHUB_USERNAME
		);
		// Generate other information
		const otherInfo = await generateOtherInfo(githubStatsData);

		// Combine ASCII art and other information
		const combinedInfo = ascii + '\n\n' + otherInfo;

		// Style the combined information using boxen
		const formattedOutput = boxen(combinedInfo, {
			padding: 1,
			margin: 1,
			borderStyle: 'round',
		});

		// Write the styled information to the README file
		fs.writeFileSync('../README.md', formattedOutput);
	} catch (error) {
		console.error('Error generating README:', error);
	}
}

async function generateOtherInfo(githubStats) {
	try {
		let otherInfo = '';

		// Neofetch style template
		otherInfo += '```\n';
		otherInfo += `          Su401@Github\n`;
		otherInfo += `            OS: A coffee fueled brain\n`;
		otherInfo += `          Host: A very tired body\n`;
		otherInfo += `        Kernel: Trauma\n`;
		otherInfo += `        Uptime: ${calculateAge(birthday)}\n`;
		otherInfo += `         Shell: DAIKAN - Direct Assertive Individual Known for Abrasive Nature\n`;
		otherInfo += `         Theme: Dark because light attracts bugs\n`;
		otherInfo += `       Memory: Very week\n`;
		otherInfo += `GitHub Stats:\n`;
		otherInfo += `  Repositories Count: ${githubStats.repositoryCount}\n`;
		otherInfo += `  Total Contributions: ${githubStats.totalContributions}\n`;
		otherInfo += `  Languages Percentage:\n`;
		for (const language in githubStats.languagePercentages) {
			otherInfo += `    ${language}: ${githubStats.languagePercentages[language]}%\n`;
		}
		otherInfo += '```\n';

		return otherInfo;
	} catch (error) {
		console.error('Error generating GitHub stats:', error);
		throw error;
	}
}

main();

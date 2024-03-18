import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

async function getGitHubStats(token, username) {
	const headers = {
		Authorization: `bearer ${token}`,
	};
	const body = {
		query: `query {
            user(login: "${username}") {
                repositories(first: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
                    totalCount
                    nodes {
                        languages(first: 50) {
                            edges {
                                node {
                                    name
                                }
                                size
                            }
                        }
                    }
                }
                contributionsCollection {
                    contributionCalendar {
                        totalContributions
                    }
                }
            }
        }`,
	};

	try {
		const response = await axios.post(
			'https://api.github.com/graphql',
			body,
			{
				headers,
			}
		);
		const data = response.data.data.user;

		// Count the number of repositories
		const repositoryCount = data.repositories.totalCount;
		const { totalContributions } =
			data.contributionsCollection.contributionCalendar;

		// Calculate the percentage of languages used
		const languageCounts = {};
		data.repositories.nodes.forEach((repo) => {
			repo.languages.edges.forEach((edge) => {
				const languageName = edge.node.name;
				const languageSize = edge.size;
				languageCounts[languageName] =
					(languageCounts[languageName] || 0) + languageSize;
			});
		});
		const totalSize = Object.values(languageCounts).reduce(
			(total, size) => total + size,
			0
		);
		const languagePercentages = {};
		Object.entries(languageCounts).forEach(([language, size]) => {
			languagePercentages[language] = ((size / totalSize) * 100).toFixed(
				2
			);
		});

		return {
			repositoryCount,
			totalContributions,
			languagePercentages,
		};
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export { getGitHubStats };

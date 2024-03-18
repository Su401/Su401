function calculateAge(birthday) {
	// Parse the birthday string into a Date object
	let birthDate = new Date(birthday);

	// Get the current date
	let currentDate = new Date();

	// Calculate the difference in milliseconds
	let difference = currentDate - birthDate;

	// Convert the difference to years, months, and days
	let years = Math.floor(difference / (1000 * 60 * 60 * 24 * 365));
	let months = Math.floor(
		(difference % (1000 * 60 * 60 * 24 * 365)) /
			(1000 * 60 * 60 * 24 * 30.44)
	);
	let days = Math.floor(
		(difference % (1000 * 60 * 60 * 24 * 30.44)) / (1000 * 60 * 60 * 24)
	);

	let uptime = `${years} years, ${months} months, and ${days} days`;

	return uptime;
}

export { calculateAge };

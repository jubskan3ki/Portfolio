/**
 * Generates a random integer between min and max (inclusive)
 * @param min Minimum value
 * @param max Maximum value
 * @returns Random integer
 */
export const randomInt = (min: number, max: number): number => {
	return Math.floor(Math.random() * (max - min + 1)) + min;
};

/**
 * Selects a random element from an array
 * @param array Array to select from
 * @returns Random element from the array
 */
export const randomElement = <T>(array: T[]): T => {
	return array[Math.floor(Math.random() * array.length)];
};

/**
 * Selects random elements from an array
 * @param array Array to select from
 * @param count Number of elements to select
 * @returns Array of random elements
 */
export const randomElements = <T>(array: T[], count: number): T[] => {
	// Ensure we don't try to select more elements than the array contains
	const selectionCount = Math.min(count, array.length);

	// Clone the array to avoid modifying the original
	const shuffled = [...array];

	// Fisher-Yates shuffle algorithm
	for (let i = shuffled.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
	}

	return shuffled.slice(0, selectionCount);
};

/**
 * Generates a random date between start and end dates
 * @param start Start date
 * @param end End date
 * @returns Random date between start and end
 */
export const randomDate = (start: Date, end: Date): Date => {
	return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
};

/**
 * Generates a random ID
 * @param prefix Optional prefix for the ID
 * @returns Random ID string
 */
export const generateId = (prefix = ''): string => {
	return `${prefix}${prefix ? '-' : ''}${Math.random().toString(36).substring(2, 10)}`;
};

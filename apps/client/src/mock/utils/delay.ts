/**
 * Simulates network latency by creating a promise that resolves after a specified delay
 * @param ms Time in milliseconds to delay
 * @returns Promise that resolves after the specified delay
 */
export const delay = (ms: number): Promise<void> => {
	return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Creates a delayed response with the provided data
 * @param data Data to return after delay
 * @param ms Time in milliseconds to delay
 * @returns Promise that resolves with the data after the specified delay
 */
export const delayedResponse = async <T>(data: T, ms = 1000): Promise<T> => {
	await delay(ms);
	return data;
};

/**
 * Standard API response format
 */
export interface ApiResponse<T> {
	success: boolean;
	data?: T;
	error?: {
		code: string;
		message: string;
	};
	meta?: {
		page?: number;
		perPage?: number;
		total?: number;
		totalPages?: number;
	};
}

/**
 * Creates a successful API response
 * @param data Data to include in the response
 * @param meta Optional metadata for pagination
 * @returns Formatted successful API response
 */
export const successResponse = <T>(data: T, meta?: ApiResponse<T>['meta']): ApiResponse<T> => {
	return {
		success: true,
		data,
		...(meta ? { meta } : {}),
	};
};

/**
 * Creates an error API response
 * @param code Error code
 * @param message Error message
 * @returns Formatted error API response
 */
export const errorResponse = <T>(code: string, message: string): ApiResponse<T> => {
	return {
		success: false,
		error: {
			code,
			message,
		},
	};
};

/**
 * Creates a paginated API response
 * @param items Array of items to paginate
 * @param page Current page number (1-based)
 * @param perPage Number of items per page
 * @returns Paginated API response
 */
export const paginatedResponse = <T>(items: T[], page = 1, perPage = 10): ApiResponse<T[]> => {
	const total = items.length;
	const totalPages = Math.ceil(total / perPage);

	// Ensure page is within bounds
	const safePage = Math.max(1, Math.min(page, totalPages || 1));

	// Calculate slice indices
	const startIndex = (safePage - 1) * perPage;
	const endIndex = Math.min(startIndex + perPage, total);

	// Get items for the current page
	const paginatedItems = items.slice(startIndex, endIndex);

	return successResponse(paginatedItems, {
		page: safePage,
		perPage,
		total,
		totalPages,
	});
};

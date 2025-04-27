// Export all contact mock data
export * from './faqs';

// Export a method to get all contact data
import { faqs } from './faqs';

export const getAllContactData = () => {
	return {
		faqs,
	};
};

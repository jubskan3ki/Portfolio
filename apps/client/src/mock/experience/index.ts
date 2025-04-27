// Export all experience mock data
export * from './education';
export * from './professional';

// Export a method to get all experience data
import { educationExperiences } from './education';
import { professionalExperiences } from './professional';

export const getAllExperienceData = () => {
	return {
		professionalExperiences,
		educationExperiences,
	};
};

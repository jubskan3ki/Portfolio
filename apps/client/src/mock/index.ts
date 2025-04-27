// Centralize all mock data exports
import * as blogMocks from './blog';
import * as contactMocks from './contact';
import * as experienceMocks from './experience';
import * as projectsMocks from './projects';
import * as stacksMocks from './stacks';
import * as mockUtils from './utils';

// Export all mock data for convenient imports
export { blogMocks, contactMocks, experienceMocks, mockUtils, projectsMocks, stacksMocks };

// Export a function to initialize all mock data with a consistent delay
export const initMockData = async (delay = 1000) => {
	await mockUtils.delay(delay);
	return {
		blog: blogMocks,
		projects: projectsMocks,
		experience: experienceMocks,
		stacks: stacksMocks,
		contact: contactMocks,
	};
};

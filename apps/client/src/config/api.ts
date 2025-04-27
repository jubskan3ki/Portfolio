export const API_BASE_URL = 'http://localhost:8000';

export const API_ENDPOINTS = {
	// User Management
	USER: {
		LOGIN: '/api/user/login/',
		LOGOUT: '/api/user/logout/',
		PROFILE: '/api/user/profile/',
		REQUEST_RESET_PASSWORD: '/api/user/request-reset-password/',
		RESET_PASSWORD: '/api/user/reset-password/',
	},

	// Stack Management
	STACK: {
		BASE: '/api/stacks/',
		BY_CATEGORY: (category: string) => `/api/stacks/category/${category}/`,
		MOST_PROFICIENT: '/api/stacks/most-proficient/',
		DETAIL: (id: string | number) => `/api/stacks/${id}/`,
	},

	// Project Management
	PROJECT: {
		BASE: '/api/projects/',
		ACTIVE: '/api/projects/active/',
		RECENT: '/api/projects/recent/',
		ARCHIVED: '/api/projects/archived/',
		BY_TAG: '/api/projects/by-tag/',
		DETAIL: (id: string | number) => `/api/projects/${id}/`,
	},

	// Experience Management
	EXPERIENCE: {
		BASE: '/api/experience/',
		CURRENT: '/api/experience/current/',
		PROFESSIONAL: '/api/experience/professional/',
		EDUCATIONAL: '/api/experience/educational/',
		HIGHLIGHTED: '/api/experience/highlighted/',
		DETAIL: (id: string | number) => `/api/experience/${id}/`,
	},

	// Contact Messages
	CONTACT: {
		BASE: '/api/contact/',
		UNREAD: '/api/contact/unread/',
		DETAIL: (id: string | number) => `/api/contact/${id}/`,
		MARK_AS_READ: (id: string | number) => `/api/contact-messages/${id}/mark-as-read/`,
	},

	// Blog Management
	BLOG: {
		BASE: '/api/blog/',
		RECENT: '/api/blog/recent/',
		POPULAR: '/api/blog/popular/',
		DRAFTS: '/api/blog/drafts/',
		DETAIL: (id: string | number) => `/api/blog/${id}/`,
	},
};

// types/feature/experience.ts

/**
 * Types pour les fonctionnalités d'expérience professionnelle
 */

// Type pour une expérience professionnelle ou éducative
export interface Experience {
	id: string;
	title: string;
	company: string;
	location: string;
	period: string;
	startDate: string;
	endDate?: string;
	description: string;
	logo?: string;
	technologies?: string[] | readonly string[];
	skills?: string[] | readonly string[];
	achievements?: string[] | readonly string[];
	type?: string;
}

// Type pour un type d'expérience (ex: professionnel, éducation)
export interface ExperienceType {
	id: string;
	name: string;
	icon?: string;
}

// Type pour les paramètres de filtrage d'expériences
export interface ExperienceFilterParams {
	type?: string;
	startYear?: number;
	endYear?: number;
	technologies?: string[];
	skills?: string[];
}

// Type pour la timeline d'expériences
export interface ExperienceTimeline {
	year: number;
	experiences: Experience[];
}

// Type pour les statistiques d'expérience
export interface ExperienceStats {
	totalYears: number;
	companiesCount: number;
	topSkills: { name: string; level: number }[];
	experienceByType: { type: string; count: number }[];
}

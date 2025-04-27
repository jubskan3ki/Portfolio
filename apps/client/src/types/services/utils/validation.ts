// types/services/utils/validation.ts

import type { z } from 'zod';

// Type pour le formulaire de contact
export interface ContactFormData {
	name: string;
	email: string;
	subject: 'general' | 'job' | 'project' | 'other';
	message: string;
	phone_number?: string;
}

// Type pour un projet
export interface ProjectData {
	title: string;
	description: string;
	status: 'completed' | 'in_progress' | 'planned' | 'archived';
	priority: number;
	tags: string[];
	github_link?: string;
	live_demo?: string;
}

// Type pour une technologie (stack)
export interface StackData {
	name: string;
	category: 'frontend' | 'backend' | 'database' | 'devops' | 'mobile' | 'design' | 'other';
	proficiency: number;
	experience_years: number;
	description?: string;
	official_website?: string;
}

// Type pour une expérience
export interface ExperienceData {
	title: string;
	company_or_school: string;
	location: string;
	start_date: string;
	end_date?: string;
	description: string;
	skills_acquired: string[];
	experience_type: 'education' | 'professional';
	is_highlighted: boolean;
	website?: string;
}

// Type pour un article de blog
export interface BlogPostData {
	title: string;
	content: string;
	status: 'draft' | 'published';
	tags: string[];
	meta_description: string;
	seo_keywords: string[];
}

// Type pour les données de connexion
export interface LoginData {
	email: string;
	password: string;
}

// Type pour la demande de réinitialisation de mot de passe
export interface PasswordResetRequestData {
	email: string;
}

// Type pour la réinitialisation de mot de passe
export interface PasswordResetData {
	email: string;
	code: string;
	new_password: string;
}

// Interface pour les validateurs de formulaire
export interface Validators {
	contact: z.ZodSchema<ContactFormData>;
	project: z.ZodSchema<ProjectData>;
	stack: z.ZodSchema<StackData>;
	experience: z.ZodSchema<ExperienceData>;
	blog: z.ZodSchema<BlogPostData>;
	login: z.ZodSchema<LoginData>;
	passwordResetRequest: z.ZodSchema<PasswordResetRequestData>;
	passwordReset: z.ZodSchema<PasswordResetData>;
}

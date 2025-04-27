// src/services/utils/validation.ts
import { z } from 'zod';

import type { Validators } from '@/types/services/utils/validation';

// Schéma de validation pour le formulaire de contact
export const contactFormSchema = z.object({
	name: z.string().min(2, 'Le nom doit contenir au moins 2 caractères'),
	email: z.string().email("L'adresse email n'est pas valide"),
	subject: z.enum(['general', 'job', 'project', 'other'], {
		errorMap: () => ({ message: 'Veuillez sélectionner un sujet valide' }),
	}),
	message: z.string().min(10, 'Le message doit contenir au moins 10 caractères'),
	phone_number: z.string().optional(),
});

// Schéma de validation pour un projet
export const projectSchema = z.object({
	title: z.string().min(3, 'Le titre doit contenir au moins 3 caractères'),
	description: z.string().min(20, 'La description doit contenir au moins 20 caractères'),
	status: z.enum(['completed', 'in_progress', 'planned', 'archived'], {
		errorMap: () => ({ message: "Le statut du projet n'est pas valide" }),
	}),
	priority: z.number().min(1).max(10),
	tags: z.array(z.string()),
	github_link: z.string().url("L'URL GitHub n'est pas valide").optional().or(z.literal('')),
	live_demo: z.string().url("L'URL de démo n'est pas valide").optional().or(z.literal('')),
});

// Schéma de validation pour une technologie (stack)
export const stackSchema = z.object({
	name: z.string().min(2, 'Le nom doit contenir au moins 2 caractères'),
	category: z.enum(['frontend', 'backend', 'database', 'devops', 'mobile', 'design', 'other'], {
		errorMap: () => ({ message: "La catégorie n'est pas valide" }),
	}),
	proficiency: z.number().min(1).max(5),
	experience_years: z.number().min(0),
	description: z.string().optional(),
	official_website: z.string().url("L'URL du site officiel n'est pas valide").optional().or(z.literal('')),
});

// Schéma de validation pour une expérience
export const experienceSchema = z.object({
	title: z.string().min(3, 'Le titre doit contenir au moins 3 caractères'),
	company_or_school: z.string().min(2, "Le nom de l'entreprise/école doit contenir au moins 2 caractères"),
	location: z.string(),
	start_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Format de date invalide (YYYY-MM-DD)'),
	end_date: z
		.string()
		.regex(/^\d{4}-\d{2}-\d{2}$/, 'Format de date invalide (YYYY-MM-DD)')
		.optional()
		.or(z.literal('')),
	description: z.string().min(20, 'La description doit contenir au moins 20 caractères'),
	skills_acquired: z.array(z.string()),
	experience_type: z.enum(['education', 'professional'], {
		errorMap: () => ({ message: "Le type d'expérience n'est pas valide" }),
	}),
	is_highlighted: z.boolean(),
	website: z.string().url("L'URL du site web n'est pas valide").optional().or(z.literal('')),
});

// Schéma de validation pour un article de blog
export const blogPostSchema = z.object({
	title: z.string().min(5, 'Le titre doit contenir au moins 5 caractères'),
	content: z.string().min(50, 'Le contenu doit contenir au moins 50 caractères'),
	status: z.enum(['draft', 'published'], {
		errorMap: () => ({ message: "Le statut n'est pas valide" }),
	}),
	tags: z.array(z.string()),
	meta_description: z.string().max(160, 'La description meta doit faire maximum 160 caractères'),
	seo_keywords: z.array(z.string()),
});

// Schéma de validation pour la connexion
export const loginSchema = z.object({
	email: z.string().email("L'adresse email n'est pas valide"),
	password: z.string().min(8, 'Le mot de passe doit contenir au moins 8 caractères'),
});

// Schéma de validation pour la demande de réinitialisation de mot de passe
export const passwordResetRequestSchema = z.object({
	email: z.string().email("L'adresse email n'est pas valide"),
});

// Schéma de validation pour la réinitialisation de mot de passe
export const passwordResetSchema = z.object({
	email: z.string().email("L'adresse email n'est pas valide"),
	code: z.string().min(6, 'Le code doit contenir au moins 6 caractères'),
	new_password: z
		.string()
		.min(8, 'Le mot de passe doit contenir au moins 8 caractères')
		.regex(/[A-Z]/, 'Le mot de passe doit contenir au moins une majuscule')
		.regex(/[a-z]/, 'Le mot de passe doit contenir au moins une minuscule')
		.regex(/[0-9]/, 'Le mot de passe doit contenir au moins un chiffre')
		.regex(/[^A-Za-z0-9]/, 'Le mot de passe doit contenir au moins un caractère spécial'),
});

// Exportation des validateurs de formulaire
export const validators: Validators = {
	contact: contactFormSchema,
	project: projectSchema,
	stack: stackSchema,
	experience: experienceSchema,
	blog: blogPostSchema,
	login: loginSchema,
	passwordResetRequest: passwordResetRequestSchema,
	passwordReset: passwordResetSchema,
};

export default validators;

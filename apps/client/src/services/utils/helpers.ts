// src/services/utils/helpers.ts
import type {
	ArrayToStringFunction,
	CurrentYearFunction,
	FormatDateFRFunction,
	FormatNumberFunction,
	GetFileExtensionFunction,
	GroupStacksByCategoryFunction,
	IsImageFileFunction,
	RandomColorFunction,
	SlugifyFunction,
	TruncateTextFunction,
} from '@/types/services/utils/helpers';

/**
 * Formate une date en français
 */
export const formatDateFR: FormatDateFRFunction = (date: string | Date): string => {
	if (!date) return '';

	const options: Intl.DateTimeFormatOptions = {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
	};
	return new Date(date).toLocaleDateString('fr-FR', options);
};

/**
 * Tronque un texte à une longueur donnée et ajoute des points de suspension
 */
export const truncateText: TruncateTextFunction = (text: string, maxLength = 100): string => {
	if (!text || text.length <= maxLength) return text;
	return text.slice(0, maxLength) + '...';
};

/**
 * Génère des URLs conviviales (slug) à partir d'un titre
 */
export const slugify: SlugifyFunction = (text: string): string => {
	if (!text) return '';

	return text
		.toString()
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase()
		.trim()
		.replace(/\s+/g, '-')
		.replace(/[^\w-]+/g, '')
		.replace(/--+/g, '-');
};

/**
 * Formate un nombre avec séparateur de milliers
 */
export const formatNumber: FormatNumberFunction = (num: number): string => {
	return new Intl.NumberFormat('fr-FR').format(num);
};

/**
 * Classifie les stacks tech par catégorie
 */
export const groupStacksByCategory: GroupStacksByCategoryFunction = <T extends { category: string }>(
	stacks: T[]
): Record<string, T[]> => {
	return stacks.reduce(
		(acc, stack) => {
			const category = stack.category;
			if (!acc[category]) {
				acc[category] = [];
			}
			acc[category].push(stack);
			return acc;
		},
		{} as Record<string, T[]>
	);
};

/**
 * Récupère l'extension d'un fichier à partir de son nom
 */
export const getFileExtension: GetFileExtensionFunction = (filename: string): string => {
	return filename.split('.').pop() || '';
};

/**
 * Vérifie si un fichier est une image
 */
export const isImageFile: IsImageFileFunction = (filename: string): boolean => {
	const ext = getFileExtension(filename).toLowerCase();
	return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext);
};

/**
 * Génère une couleur aléatoire en hexadécimal
 */
export const randomColor: RandomColorFunction = (): string => {
	return '#' + Math.floor(Math.random() * 16777215).toString(16);
};

/**
 * Récupère l'année actuelle (utile pour footer)
 */
export const currentYear: CurrentYearFunction = (): number => {
	return new Date().getFullYear();
};

/**
 * Transforme un tableau en chaîne avec virgules
 */
export const arrayToString: ArrayToStringFunction = (arr: string[]): string => {
	if (!arr || !Array.isArray(arr)) return '';
	return arr.join(', ');
};

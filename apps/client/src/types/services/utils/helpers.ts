// types/services/utils/helpers.ts

// Type pour la fonction de formatage de date en français
export type FormatDateFRFunction = (date: string | Date) => string;

// Type pour la fonction de troncature de texte
export type TruncateTextFunction = (text: string, maxLength?: number) => string;

// Type pour la fonction de génération de slug
export type SlugifyFunction = (text: string) => string;

// Type pour la fonction de formatage de nombre
export type FormatNumberFunction = (num: number) => string;

// Type pour la fonction de regroupement des stacks par catégorie
export type GroupStacksByCategoryFunction = <T extends { category: string }>(stacks: T[]) => Record<string, T[]>;

// Type pour la fonction de récupération d'extension de fichier
export type GetFileExtensionFunction = (filename: string) => string;

// Type pour la fonction de vérification de fichier image
export type IsImageFileFunction = (filename: string) => boolean;

// Type pour la fonction de génération de couleur aléatoire
export type RandomColorFunction = () => string;

// Type pour la fonction d'année courante
export type CurrentYearFunction = () => number;

// Type pour la fonction de conversion de tableau en chaîne
export type ArrayToStringFunction = (arr: string[]) => string;

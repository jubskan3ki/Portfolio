// articles.ts
import { images } from '@/config/images';
import type { Article } from '@/types/feature/blog';

import { randomInt } from '../utils/generators';

const baseArticles = [
	{
		title: 'Introduction à Docker pour les développeurs',
		slug: 'docker-introduction-developpeurs',
		excerpt: 'Découvrez les bases de Docker pour accélérer vos workflows de développement.',
		topic: 'Docker',
		category: 'devops',
		tags: ['docker', 'devops', 'containers'],
	},
	{
		title: 'Déployer une app Flutter avec Firebase Hosting',
		slug: 'flutter-firebase-deployment',
		excerpt: 'Déployez votre app Flutter Web en quelques clics avec Firebase.',
		topic: 'Flutter + Firebase',
		category: 'mobile',
		tags: ['flutter', 'firebase', 'mobile'],
	},
	{
		title: 'Créer une API REST robuste avec NestJS',
		slug: 'nestjs-api-rest',
		excerpt: 'Apprenez à construire des API REST sécurisées et scalables avec NestJS.',
		topic: 'NestJS API',
		category: 'backend',
		tags: ['nestjs', 'api', 'backend'],
	},
	{
		title: 'Optimiser les performances dans une app React',
		slug: 'optimiser-performances-react',
		excerpt: 'Découvrez les techniques pour rendre vos applications React ultra-rapides.',
		topic: 'Optimisation React',
		category: 'frontend',
		tags: ['react', 'performance', 'frontend'],
	},
	{
		title: 'Introduction à GraphQL pour les débutants',
		slug: 'graphql-introduction',
		excerpt: 'Comprenez pourquoi GraphQL révolutionne la manière de construire des API modernes.',
		topic: 'GraphQL',
		category: 'api',
		tags: ['graphql', 'api', 'backend'],
	},
	{
		title: 'Déploiement Kubernetes pour les débutants',
		slug: 'kubernetes-deploiement-debutants',
		excerpt: 'Un guide simple pour orchestrer vos containers avec Kubernetes.',
		topic: 'Kubernetes',
		category: 'cloud',
		tags: ['kubernetes', 'cloud', 'devops'],
	},
	{
		title: 'Utiliser Firebase Authentication dans vos apps mobiles',
		slug: 'firebase-auth-mobile',
		excerpt: 'Ajoutez facilement une authentification sécurisée dans vos apps Flutter.',
		topic: 'Firebase Auth',
		category: 'mobile',
		tags: ['firebase', 'auth', 'mobile'],
	},
	{
		title: 'Construire une architecture microservices avec Node.js',
		slug: 'microservices-nodejs',
		excerpt: 'Passez du monolithe aux microservices avec Node.js et Docker.',
		topic: 'Microservices Node.js',
		category: 'architecture',
		tags: ['nodejs', 'microservices', 'architecture'],
	},
	{
		title: 'Meilleures pratiques de sécurité dans une API REST',
		slug: 'securite-api-rest',
		excerpt: "Sécurisez vos API contre les attaques courantes dès aujourd'hui.",
		topic: 'Sécurité API',
		category: 'security',
		tags: ['security', 'api', 'backend'],
	},
	{
		title: 'CI/CD moderne avec GitHub Actions',
		slug: 'ci-cd-github-actions',
		excerpt: 'Automatisez vos déploiements grâce à GitHub Actions.',
		topic: 'CI/CD GitHub Actions',
		category: 'devops',
		tags: ['ci-cd', 'github-actions', 'devops'],
	},
	{
		title: 'Utiliser AWS S3 pour stocker vos fichiers',
		slug: 'aws-s3-stockage',
		excerpt: 'Mettez en place un stockage sécurisé et scalable avec Amazon S3.',
		topic: 'AWS S3',
		category: 'cloud',
		tags: ['aws', 's3', 'cloud'],
	},
	{
		title: 'Créer des tests unitaires efficaces avec Jest',
		slug: 'tests-unitaires-jest',
		excerpt: 'Écrivez des tests robustes et maintenables avec Jest.',
		topic: 'Testing Jest',
		category: 'testing',
		tags: ['testing', 'jest', 'frontend'],
	},
	{
		title: 'Flutter State Management avec Riverpod',
		slug: 'flutter-riverpod-state-management',
		excerpt: "Simplifiez la gestion d'état dans Flutter avec Riverpod.",
		topic: 'State Management Flutter',
		category: 'mobile',
		tags: ['flutter', 'state-management', 'mobile'],
	},
	{
		title: 'Sécuriser vos apps Node.js avec Helmet',
		slug: 'securiser-nodejs-helmet',
		excerpt: 'Protégez vos applications Express avec Helmet et bonnes pratiques.',
		topic: 'Sécurité Node.js',
		category: 'backend',
		tags: ['nodejs', 'security', 'backend'],
	},
	{
		title: 'Créer une Progressive Web App (PWA) avec React',
		slug: 'pwa-react-creation',
		excerpt: 'Transformez vos applications React en PWA modernes.',
		topic: 'PWA React',
		category: 'frontend',
		tags: ['react', 'pwa', 'frontend'],
	},
	{
		title: "Gérer l'infrastructure cloud avec Terraform",
		slug: 'infrastructure-terraform',
		excerpt: 'Déployez et gérez votre infrastructure cloud avec du code (IaC).',
		topic: 'Terraform',
		category: 'cloud',
		tags: ['terraform', 'cloud', 'devops'],
	},
	{
		title: 'Booster vos apps avec Next.js et TypeScript',
		slug: 'nextjs-typescript-boost',
		excerpt: 'Utilisez Next.js + TypeScript pour des applications web ultra-rapides.',
		topic: 'Next.js + TypeScript',
		category: 'frontend',
		tags: ['nextjs', 'typescript', 'frontend'],
	},
	{
		title: 'Authentification OAuth2 avec NestJS',
		slug: 'nestjs-auth-oauth2',
		excerpt: 'Implémentez facilement OAuth2 dans vos APIs NestJS.',
		topic: 'OAuth2 NestJS',
		category: 'backend',
		tags: ['nestjs', 'auth', 'backend'],
	},
	{
		title: 'Introduction à Prisma ORM avec Node.js',
		slug: 'prisma-orm-nodejs',
		excerpt: 'Accédez à votre base de données plus rapidement avec Prisma.',
		topic: 'Prisma ORM',
		category: 'backend',
		tags: ['prisma', 'nodejs', 'database'],
	},
	{
		title: 'Mieux comprendre le serverless avec AWS Lambda',
		slug: 'serverless-aws-lambda',
		excerpt: 'Créez des fonctions serverless évolutives sur AWS.',
		topic: 'AWS Lambda',
		category: 'cloud',
		tags: ['aws', 'serverless', 'cloud'],
	},
	{
		title: 'Testing E2E avec Cypress pour vos apps frontend',
		slug: 'e2e-testing-cypress',
		excerpt: 'Testez vos applications de bout en bout avec Cypress.',
		topic: 'E2E Testing',
		category: 'testing',
		tags: ['testing', 'cypress', 'frontend'],
	},
];

const articleImages = [
	images.articles.article1,
	images.articles.article2,
	images.articles.article3,
	images.articles.article4,
	images.articles.article5,
];

const createArticleContent = (topic: string, paragraphCount = 6): string[] => {
	const content = [
		`Introduction sur ${topic}.`,
		`Pourquoi ${topic} est essentiel aujourd'hui.`,
		`Mise en place de ${topic} étape par étape.`,
		`Erreurs fréquentes avec ${topic} et comment les éviter.`,
		`Optimiser l'utilisation de ${topic} pour de meilleures performances.`,
		`Conclusion et bonnes pratiques sur ${topic}.`,
	];
	return content.slice(0, paragraphCount);
};

const createTableOfContents = (topic: string): string[] => [
	`Introduction à ${topic}`,
	'Installation et configuration',
	'Principes fondamentaux',
	'Exemples concrets',
	'Optimisations',
	'Conclusion',
];

export const articles: Article[] = baseArticles.map((baseArticle, index) => ({
	id: `article-${index + 1}`,
	title: baseArticle.title,
	slug: baseArticle.slug,
	excerpt: baseArticle.excerpt,
	content: createArticleContent(baseArticle.topic, 6),
	image: articleImages[index % articleImages.length],
	category: baseArticle.category,
	tags: baseArticle.tags,
	date: new Date(2024, index % 12, 5 + index).toISOString(),
	readTime: 4 + (index % 6),
	views: 200 + randomInt(200, 1500),
	toc: createTableOfContents(baseArticle.topic),
	author: {
		name: 'Juba Ait-Adda',
		avatar: images.others.profilePhoto,
		bio: "Développeur Web, Mobile et DevOps passionné par l'innovation technologique.",
		social: {
			github: 'https://github.com/juba-ait-adda',
			linkedin: 'https://linkedin.com/in/juba-ait-adda',
			twitter: 'https://twitter.com/juba-ait-adda',
		},
	},
}));

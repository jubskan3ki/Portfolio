import { images } from '@/config/images';
import type { Project } from '@/types/feature/project';

const projectImages = [
	images.projects.project1,
	images.projects.project2,
	images.projects.project3,
	images.projects.project4,
	images.projects.project5,
];

export const projects: Project[] = [
	{
		id: 'project-1',
		title: 'Foodcourt',
		slug: 'foodcourt',
		description: 'Plateforme web de réservation et de commande dans les foodcourts universitaires.',
		longDescription:
			'Foodcourt est une application web permettant aux étudiants de réserver, commander et suivre en temps réel leurs repas dans les foodcourts. Développée en React TypeScript pour le front-end, Go pour le back-end et Dockerisée pour assurer un déploiement rapide et fiable.',
		image: projectImages[0],
		category: 'web',
		technologies: ['React', 'TypeScript', 'Go', 'Docker', 'PostgreSQL'],
		date: '2025-01-10',
		features: [
			'Réservation de repas et gestion du panier',
			'Suivi des commandes en temps réel',
			'Tableau de bord admin pour la gestion des stands',
			'Paiement en ligne sécurisé',
			'Dockerisation complète pour déploiement rapide',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-2',
		title: 'TechRace',
		slug: 'techrace',
		description: 'Contrôle de voitures télécommandées via smartphone avec statistiques en temps réel.',
		longDescription:
			"TechRace est une solution mobile et web innovante permettant de piloter des voitures télécommandées à distance, visualiser les performances et analyser les résultats de course. L'application utilise React Native pour mobile, React pour web, Go pour le back-end, et Docker pour l'infrastructure.",
		image: projectImages[1],
		category: 'mobile',
		technologies: ['React Native', 'React', 'TypeScript', 'Go', 'Docker', 'WebSocket'],
		date: '2024-06-01',
		features: [
			'Contrôle de véhicules en temps réel via mobile',
			'Tableaux de bord de performances',
			'Système de gestion des courses et scores',
			'Dockerisation et communication WebSocket',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-3',
		title: 'SpotifyBoard',
		slug: 'spotifyboard',
		description: "Plateforme collaborative d'écoute musicale connectée à Spotify.",
		longDescription:
			'SpotifyBoard est un projet fullstack construit en Django pour le backend et Svelte + TypeScript pour le frontend, permettant aux utilisateurs de créer des sessions musicales partagées et collaboratives, avec hébergement Dockerisé.',
		image: projectImages[2],
		category: 'web',
		technologies: ['Django', 'Svelte', 'TypeScript', 'Docker', 'Spotify API'],
		date: '2024-03-15',
		features: [
			'Connexion sécurisée à Spotify',
			'Création de sessions collaboratives',
			'Vote et contrôle communautaire de la playlist',
			'Interface légère et temps réel',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-4',
		title: 'DogGuesser',
		slug: 'dogguesser',
		description: "Jeu en ligne de reconnaissance de races de chiens à partir d'images.",
		longDescription:
			'DogGuesser est une application web gamifiée en React, Node.js et TypeScript, où les utilisateurs doivent deviner les races de chiens à partir de photos en un temps limité. Le projet est Dockerisé pour un déploiement facilité.',
		image: projectImages[3],
		category: 'web',
		technologies: ['React', 'Node.js', 'TypeScript', 'Docker', 'Express'],
		date: '2024-01-20',
		features: [
			'Jeu chronométré et scoring',
			'Base de données d’images de races de chiens',
			'Interface ludique et responsive',
			'Déploiement Docker',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-5',
		title: 'RPlace Clone',
		slug: 'rplace-clone',
		description: "Reproduction collaborative de l'expérience R/Place de Reddit.",
		longDescription:
			'RPlace est un projet communautaire en React, Node.js et TypeScript, permettant à plusieurs utilisateurs de collaborer pour dessiner un pixel art géant en temps réel. Gestion de la concurrence et synchronisation assurées via WebSocket.',
		image: projectImages[4],
		category: 'web',
		technologies: ['React', 'Node.js', 'TypeScript', 'WebSocket', 'Docker'],
		date: '2023-12-05',
		features: [
			'Grille collaborative en temps réel',
			'Gestion des accès concurrentiels',
			'Animation et rafraîchissement dynamique',
			'Déploiement sur Docker',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-6',
		title: 'BlaBlaChat',
		slug: 'blablachat',
		description: 'Application de messagerie instantanée sécurisée en React.',
		longDescription:
			'BlaBlaChat est un projet de chat en ligne sécurisé développé en React TypeScript, avec communication WebSocket et conteneurisation Docker pour faciliter la scalabilité.',
		image: projectImages[0],
		category: 'web',
		technologies: ['React', 'TypeScript', 'Docker', 'WebSocket', 'Node.js'],
		date: '2023-09-01',
		features: [
			'Messagerie instantanée temps réel',
			'Salles de discussions privées et publiques',
			'Authentification utilisateur',
			'Déploiement multi-environnements avec Docker',
		],
		links: {
			demo: '',
			github: '',
		},
	},
	{
		id: 'project-7',
		title: 'Infrastructure Cloud - Terraform & Ansible',
		slug: 'terraform-ansible-infra',
		description: "Déploiement automatisé d'une infrastructure cloud via Terraform et Ansible.",
		longDescription:
			"Projet d'infrastructure as code permettant de provisionner, configurer et sécuriser des environnements cloud en utilisant Terraform et Ansible. Optimisé pour AWS et hébergé avec une approche modulaire et scalable.",
		image: projectImages[1],
		category: 'devops',
		technologies: ['Terraform', 'Ansible', 'AWS', 'Docker'],
		date: '2023-07-01',
		features: [
			'Provisionnement automatisé sur AWS',
			'Configuration automatique via Ansible',
			'Gestion centralisée des configurations et secrets',
			'Infrastructure modulaire et scalable',
		],
		links: {
			github: '',
			documentation: '',
		},
	},
	{
		id: 'project-8',
		title: 'Pipeline CI/CD Kubernetes',
		slug: 'ci-cd-kubernetes',
		description: "Mise en place d'un pipeline CI/CD complet sur cluster Kubernetes.",
		longDescription:
			"Développement d'une architecture CI/CD avancée pour automatiser les tests, les builds et les déploiements sur un cluster Kubernetes. Utilisation de Jenkins, GitHub Actions et Helm Charts.",
		image: projectImages[2],
		category: 'devops',
		technologies: ['Kubernetes', 'GitHub Actions', 'Jenkins', 'Helm', 'Docker'],
		date: '2023-04-01',
		features: [
			'Pipeline CI/CD automatisé avec GitHub Actions et Jenkins',
			'Déploiement continu sur Kubernetes',
			'Monitoring et rollback automatisés',
			'Gestion Helm Charts personnalisés',
		],
		links: {
			github: '',
			documentation: '',
		},
	},
];

import { images } from '@/config/images';
import type { Stack } from '@/types/feature/stacks';

export const stacks: Stack[] = [
	{
		id: 'vue',
		name: 'Vue.js',
		description: 'Framework JavaScript progressif pour construire des interfaces utilisateur.',
		logo: images.stacks.vue,
		category: 'frontend',
		tags: ['frontend', 'javascript', 'framework', 'spa', 'reactive'],
		slug: 'vue-js',
		experience: 4,
		level: 90,
		website: 'https://vuejs.org',
		websiteLabel: 'vuejs.org',
		github: 'https://github.com/vuejs/core',
		githubLabel: 'vuejs/core',
		firstRelease: '2014',
		license: 'MIT',
		content: `Vue.js est un framework JavaScript progressif pour construire des interfaces utilisateur. Contrairement à d'autres frameworks monolithiques, Vue est conçu pour être adopté de manière incrémentielle. La bibliothèque principale est focalisée uniquement sur la couche vue, et est facilement intégrable avec d'autres bibliothèques ou projets existants.

			Dans mon travail quotidien, j'utilise Vue.js pour créer des interfaces utilisateur dynamiques et réactives. Sa simplicité et sa flexibilité en font mon choix privilégié pour le développement front-end.

			Pourquoi Vue.js?

			Vue.js offre une courbe d'apprentissage douce qui permet de devenir productif rapidement. Sa documentation excellente est traduite en plusieurs langues et couvre tous les aspects du framework. L'écosystème riche comprend Vuex pour la gestion d'état, Vue Router pour le routage, et Nuxt.js pour les applications universelles. Vue excelle également en performance grâce à son DOM virtuel optimisé et sa réactivité fine. Sa flexibilité d'intégration permet de l'utiliser aussi bien pour des widgets isolés que pour des applications complètes.

			Avec la sortie de Vue 3, le framework a gagné en performances et en flexibilité grâce à la Composition API, permettant une meilleure réutilisation de la logique entre composants.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide complet et API de référence pour Vue.js',
				url: 'https://vuejs.org/guide/introduction.html',
			},
			{
				title: 'Vue Mastery',
				description: "Plateforme d'apprentissage avec des cours vidéo sur Vue.js",
				url: 'https://www.vuemastery.com/',
			},
			{
				title: 'Awesome Vue',
				description: "Liste curatée de ressources impressionnantes pour l'écosystème Vue.js",
				url: 'https://github.com/vuejs/awesome-vue',
			},
			{
				title: 'Vue School',
				description: 'Tutoriels vidéo premium et formations sur Vue.js et son écosystème',
				url: 'https://vueschool.io/',
			},
		],
		relatedStacks: [
			{
				name: 'Nuxt.js',
				logo: images.stacks.vue,
				slug: 'nuxt-js',
				category: 'frontend',
			},
			{
				name: 'Vite',
				logo: images.stacks.vite,
				slug: 'vite',
				category: 'frontend',
			},
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
			{
				name: 'Sass',
				logo: images.stacks.sass,
				slug: 'sass',
				category: 'frontend',
			},
		],
	},
	{
		id: 'react',
		name: 'React',
		description: 'Bibliothèque JavaScript pour construire des interfaces utilisateur.',
		logo: images.stacks.react,
		category: 'frontend',
		tags: ['frontend', 'javascript', 'library', 'spa', 'meta'],
		slug: 'react',
		experience: 3,
		level: 80,
		website: 'https://react.dev',
		websiteLabel: 'react.dev',
		github: 'https://github.com/facebook/react',
		githubLabel: 'facebook/react',
		firstRelease: '2013',
		license: 'MIT',
		content: `React est une bibliothèque JavaScript pour créer des interfaces utilisateur. Elle est maintenue par Meta (anciennement Facebook) et une communauté mondiale de développeurs individuels et d'entreprises.

			React permet de construire des interfaces utilisateur complexes à partir de petits morceaux de code isolés appelés "composants". C'est une approche déclarative qui facilite le raisonnement sur l'application et favorise la réutilisation du code.

			Points forts de React

			React se distingue par son DOM virtuel qui optimise les performances en minimisant les manipulations coûteuses du DOM réel. Son architecture basée sur les composants encourage la création de code modulaire et réutilisable. L'écosystème riche autour de React comprend des outils comme Redux pour la gestion d'état, React Router pour la navigation, et des frameworks comme Next.js et Remix pour le rendu côté serveur. React s'intègre facilement avec d'autres bibliothèques et offre un excellent support pour TypeScript, facilitant le développement d'applications robustes et maintenables.

			Les Hooks, introduits dans React 16.8, ont révolutionné la façon d'écrire des composants en permettant d'utiliser l'état et d'autres fonctionnalités de React sans avoir à écrire de classes, rendant le code plus concis et lisible.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Documentation et tutoriels pour React',
				url: 'https://react.dev/learn',
			},
			{
				title: 'React DevTools',
				description: 'Extension pour le débogage des applications React',
				url: 'https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi',
			},
			{
				title: 'React Query',
				description: 'Bibliothèque pour la gestion des données côté serveur dans React',
				url: 'https://tanstack.com/query/latest',
			},
			{
				title: 'React Handbook',
				description: 'Guide complet pour apprendre React',
				url: 'https://reacthandbook.dev',
			},
		],
		relatedStacks: [
			{
				name: 'Next.js',
				logo: images.stacks.react,
				slug: 'next-js',
				category: 'frontend',
			},
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
		],
	},
	{
		id: 'node',
		name: 'Node.js',
		description: "Environnement d'exécution JavaScript côté serveur.",
		logo: images.stacks.node,
		category: 'backend',
		tags: ['backend', 'javascript', 'runtime', 'server', 'asynchronous'],
		slug: 'node-js',
		experience: 4,
		level: 85,
		website: 'https://nodejs.org',
		websiteLabel: 'nodejs.org',
		github: 'https://github.com/nodejs/node',
		githubLabel: 'nodejs/node',
		firstRelease: '2009',
		license: 'MIT',
		content: `Node.js est un environnement d'exécution JavaScript construit sur le moteur JavaScript V8 de Chrome. Il permet d'exécuter du code JavaScript côté serveur, ce qui était traditionnellement réservé aux navigateurs.

			Grâce à son modèle non-bloquant piloté par les événements, Node.js est particulièrement adapté aux applications temps réel et aux API nécessitant de hautes performances.

			Avantages de Node.js

			Le modèle d'E/S non-bloquant de Node.js permet de gérer de nombreuses opérations simultanées sans bloquer le thread principal, ce qui en fait une solution idéale pour les applications nécessitant de nombreuses connexions simultanées. Sa haute performance pour les applications en temps réel est due à sa boucle d'événements efficace et à son exécution asynchrone. L'utilisation du même langage (JavaScript) côté client et serveur simplifie le développement full-stack et permet le partage de code entre les deux environnements.

			Node.js dispose d'un vaste écosystème de packages via npm, le plus grand registre de bibliothèques au monde, offrant des solutions pour presque tous les besoins de développement. Son excellente gestion des connexions simultanées en fait un choix privilégié pour les services de streaming, les API REST, les applications de chat et autres systèmes nécessitant de gérer de nombreuses connections en parallèle.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide et référence API pour Node.js',
				url: 'https://nodejs.org/en/docs/',
			},
			{
				title: 'Node.js Best Practices',
				description: 'Recueil des meilleures pratiques pour Node.js',
				url: 'https://github.com/goldbergyoni/nodebestpractices',
			},
			{
				title: 'Node.js Design Patterns',
				description: 'Livre sur les patterns de conception pour Node.js',
				url: 'https://www.nodejsdesignpatterns.com/',
			},
			{
				title: 'The Node.js Handbook',
				description: 'Guide complet pour apprendre Node.js',
				url: 'https://nodejs.dev/learn',
			},
		],
		relatedStacks: [
			{
				name: 'Express',
				logo: images.stacks.node,
				slug: 'express',
				category: 'backend',
			},
			{
				name: 'NestJS',
				logo: images.stacks.nest,
				slug: 'nestjs',
				category: 'backend',
			},
			{
				name: 'MongoDB',
				logo: images.stacks.mongodb,
				slug: 'mongodb',
				category: 'database',
			},
			{
				name: 'PostgreSQL',
				logo: images.stacks.postgresql,
				slug: 'postgresql',
				category: 'database',
			},
		],
	},
	{
		id: 'typescript',
		name: 'TypeScript',
		description: 'Surensemble typé de JavaScript qui se compile en JavaScript pur.',
		logo: images.stacks.typescript,
		category: 'frontend',
		tags: ['frontend', 'language', 'javascript', 'typing', 'microsoft'],
		slug: 'typescript',
		experience: 3,
		level: 85,
		website: 'https://www.typescriptlang.org',
		websiteLabel: 'typescriptlang.org',
		github: 'https://github.com/microsoft/TypeScript',
		githubLabel: 'microsoft/TypeScript',
		firstRelease: '2012',
		license: 'Apache-2.0',
		content: `TypeScript est un langage de programmation libre et open source développé par Microsoft qui ajoute un système de typage statique optionnel à JavaScript. TypeScript se compile en JavaScript pur, ce qui permet de l'utiliser partout où JavaScript est accepté.

			Le système de types de TypeScript permet aux développeurs de détecter les erreurs plus tôt dans le cycle de développement, tout en offrant une meilleure expérience de développement grâce à l'autocomplétion et la documentation intégrée.

			Pourquoi utiliser TypeScript

			La détection des erreurs à la compilation est l'un des principaux avantages de TypeScript, permettant d'identifier les problèmes avant même l'exécution du code. L'expérience de développement est considérablement améliorée grâce à l'autocomplétion intelligente, la navigation dans le code et la documentation intégrée dans les éditeurs modernes comme VS Code. Le refactoring devient plus sûr grâce au système de types qui vérifie automatiquement la cohérence des modifications à travers la base de code.

			TypeScript s'intègre parfaitement avec les principaux frameworks front-end comme React, Vue et Angular, ainsi qu'avec Node.js côté serveur. Les types servent également de documentation automatique du code, facilitant la compréhension des interfaces et des structures de données pour tous les membres de l'équipe.

			Les fonctionnalités avancées comme les types génériques, les types conditionnels et les utilitaires de types permettent de modéliser précisément des structures de données complexes et des comportements sophistiqués.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Manuel et référence pour TypeScript',
				url: 'https://www.typescriptlang.org/docs/',
			},
			{
				title: 'TypeScript Playground',
				description: 'Environnement en ligne pour tester du code TypeScript',
				url: 'https://www.typescriptlang.org/play',
			},
			{
				title: 'TypeScript Deep Dive',
				description: 'Livre gratuit en ligne sur TypeScript',
				url: 'https://basarat.gitbook.io/typescript/',
			},
			{
				title: 'Type Challenges',
				description: 'Collection de défis pour améliorer vos compétences en TypeScript',
				url: 'https://github.com/type-challenges/type-challenges',
			},
		],
		relatedStacks: [
			{
				name: 'Vue.js',
				logo: images.stacks.vue,
				slug: 'vue-js',
				category: 'frontend',
			},
			{
				name: 'React',
				logo: images.stacks.react,
				slug: 'react',
				category: 'frontend',
			},
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
			{
				name: 'NestJS',
				logo: images.stacks.nest,
				slug: 'nestjs',
				category: 'backend',
			},
		],
	},
	{
		id: 'docker',
		name: 'Docker',
		description: "Plateforme de conteneurisation d'applications.",
		logo: images.stacks.docker,
		category: 'devops',
		tags: ['devops', 'container', 'deployment', 'virtualization', 'microservices'],
		slug: 'docker',
		experience: 3,
		level: 80,
		website: 'https://www.docker.com',
		websiteLabel: 'docker.com',
		github: 'https://github.com/docker',
		githubLabel: 'docker',
		firstRelease: '2013',
		license: 'Apache-2.0',
		content: `Docker est une plateforme de conteneurisation qui permet de créer, déployer et exécuter des applications dans des conteneurs. Les conteneurs sont légers, autonomes et contiennent tout ce dont une application a besoin pour fonctionner.

			Avec Docker, les développeurs peuvent être sûrs que leur application fonctionnera partout, quelle que soit l'infrastructure sous-jacente, ce qui améliore considérablement la portabilité et la reproductibilité des environnements.

			Avantages de Docker

			Docker garantit des environnements de développement cohérents en encapsulant les dépendances et les configurations dans des conteneurs, éliminant ainsi le problème du "ça marche sur ma machine". L'isolation des applications assure que chaque conteneur dispose de ses propres ressources et processus, sans interférer avec d'autres applications ou le système hôte. Le déploiement devient rapide et reproductible grâce aux images immuables qui peuvent être versionnées et partagées via des registres comme Docker Hub.

			Docker optimise l'utilisation des ressources en partageant le noyau du système d'exploitation hôte et en n'embarquant que les bibliothèques et binaires nécessaires, contrairement aux machines virtuelles traditionnelles. Son intégration facile dans les pipelines CI/CD permet d'automatiser les tests et les déploiements, accélérant considérablement le cycle de développement logiciel.

			L'écosystème Docker comprend également des outils comme Docker Compose pour orchestrer des applications multi-conteneurs et s'intègre parfaitement avec des plateformes d'orchestration comme Kubernetes pour les déploiements à grande échelle.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guides et référence pour Docker',
				url: 'https://docs.docker.com/',
			},
			{
				title: 'Docker Hub',
				description: "Registre public d'images Docker",
				url: 'https://hub.docker.com/',
			},
			{
				title: 'Docker Curriculum',
				description: 'Guide complet pour apprendre Docker',
				url: 'https://docker-curriculum.com/',
			},
			{
				title: 'Play with Docker',
				description: 'Laboratoire en ligne pour expérimenter avec Docker',
				url: 'https://labs.play-with-docker.com/',
			},
		],
		relatedStacks: [
			{
				name: 'Kubernetes',
				logo: images.stacks.kubernetes,
				slug: 'kubernetes',
				category: 'devops',
			},
			{
				name: 'AWS',
				logo: images.stacks.aws,
				slug: 'aws',
				category: 'devops',
			},
			{
				name: 'Terraform',
				logo: images.stacks.terraform,
				slug: 'terraform',
				category: 'devops',
			},
			{
				name: 'Ansible',
				logo: images.stacks.ansible,
				slug: 'ansible',
				category: 'devops',
			},
		],
	},
	{
		id: 'nestjs',
		name: 'NestJS',
		description:
			'Framework Node.js progressif pour construire des applications côté serveur efficaces et évolutives.',
		logo: images.stacks.nest,
		category: 'backend',
		tags: ['backend', 'typescript', 'framework', 'api', 'microservices'],
		slug: 'nestjs',
		experience: 3,
		level: 75,
		website: 'https://nestjs.com',
		websiteLabel: 'nestjs.com',
		github: 'https://github.com/nestjs/nest',
		githubLabel: 'nestjs/nest',
		firstRelease: '2017',
		license: 'MIT',
		content: `NestJS est un framework Node.js progressif pour la construction d'applications serveur efficaces, évolutives et maintenables. Il utilise TypeScript par défaut et combine des éléments de la programmation orientée objet (OOP), de la programmation fonctionnelle (FP) et de la programmation fonctionnelle réactive (FRP).

			Inspiré par Angular, NestJS propose une architecture modulaire qui facilite l'organisation du code en composants réutilisables et testables. Il est particulièrement adapté aux applications d'entreprise et aux API REST professionnelles.

			Points forts de NestJS

			NestJS offre une architecture claire et bien structurée basée sur les contrôleurs, les services et les modules, facilitant la maintenance de projets complexes. Son intégration native avec TypeScript permet un développement robuste avec vérification des types statiques et une meilleure autocomplétion dans les éditeurs de code. Le framework inclut des fonctionnalités avancées comme l'injection de dépendances, les guards, les intercepteurs, les pipes et les filtres d'exception qui permettent de créer des applications modulaires et facilement testables.

			La flexibilité de NestJS est remarquable : il supporte différents transports comme REST, GraphQL, WebSockets, gRPC et même des architectures en microservices. La documentation exhaustive et la communauté active sont d'excellentes ressources pour les développeurs. Pour la persistance des données, NestJS s'intègre facilement avec des ORM comme TypeORM, Sequelize, ou Mongoose, couvrant la plupart des bases de données relationnelles et NoSQL.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide complet et référence API pour NestJS',
				url: 'https://docs.nestjs.com/',
			},
			{
				title: 'NestJS Courses',
				description: 'Formations officielles sur NestJS',
				url: 'https://courses.nestjs.com/',
			},
			{
				title: 'Awesome NestJS',
				description: 'Collection de ressources pour NestJS',
				url: 'https://github.com/nestjs/awesome-nestjs',
			},
		],
		relatedStacks: [
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
			{
				name: 'PostgreSQL',
				logo: images.stacks.postgresql,
				slug: 'postgresql',
				category: 'database',
			},
		],
	},
	{
		id: 'postgresql',
		name: 'PostgreSQL',
		description: 'Système de gestion de base de données relationnelle open source avancé.',
		logo: images.stacks.postgresql,
		category: 'database',
		tags: ['database', 'sql', 'relational', 'open-source', 'enterprise'],
		slug: 'postgresql',
		experience: 4,
		level: 85,
		website: 'https://www.postgresql.org',
		websiteLabel: 'postgresql.org',
		github: 'https://github.com/postgres/postgres',
		githubLabel: 'postgres/postgres',
		firstRelease: '1996',
		license: 'PostgreSQL License',
		content: `PostgreSQL est un système de gestion de base de données relationnelle object-relationnelle (ORDBMS) open source avancé. Avec plus de 30 ans de développement actif, PostgreSQL a gagné une solide réputation pour sa fiabilité, sa robustesse et ses performances.

			Connu pour sa conformité aux standards SQL et sa capacité à gérer des charges de travail allant de petites applications à de grands entrepôts de données avec de nombreux utilisateurs simultanés, PostgreSQL est un choix privilégié pour les applications critiques.

			Atouts de PostgreSQL

			La conformité SQL de PostgreSQL est exemplaire, supportant presque toutes les fonctionnalités du standard SQL:2016. Ses capacités avancées incluent les types de données personnalisés, l'héritage de tables, les fonctions et procédures stockées dans plusieurs langages de programmation, les index sophistiqués (B-tree, Hash, GiST, SP-GiST, GIN, BRIN), et le support natif pour les données géospatiales via l'extension PostGIS.

			PostgreSQL excelle en matière d'intégrité des données avec son support complet pour les transactions ACID, les clés étrangères, les contraintes d'exclusion, et les déclencheurs (triggers). Sa haute extensibilité se manifeste par sa capacité à gérer des téraoctets de données et sa riche bibliothèque d'extensions comme TimescaleDB pour les séries temporelles, pgVector pour les recherches vectorielles, ou pg_stat_statements pour le monitoring des performances.

			La sécurité est une priorité avec des fonctionnalités comme l'authentification forte, le contrôle d'accès basé sur les rôles, le chiffrement au niveau des colonnes, et la conformité GDPR. De plus, PostgreSQL bénéficie d'une communauté active et d'un écosystème riche d'outils de gestion, de surveillance et d'administration.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Manuel complet de PostgreSQL',
				url: 'https://www.postgresql.org/docs/current/',
			},
			{
				title: 'PostgreSQL Tutorial',
				description: 'Tutoriels et guides pratiques pour PostgreSQL',
				url: 'https://www.postgresqltutorial.com/',
			},
			{
				title: 'PostgreSQL Weekly',
				description: 'Newsletter hebdomadaire sur PostgreSQL',
				url: 'https://postgresweekly.com/',
			},
		],
		relatedStacks: [
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
			{
				name: 'Django',
				logo: images.stacks.django,
				slug: 'django',
				category: 'backend',
			},
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
		],
	},
	{
		id: 'aws',
		name: 'AWS',
		description: 'Plateforme de services cloud proposée par Amazon.',
		logo: images.stacks.aws,
		category: 'devops',
		tags: ['devops', 'cloud', 'infrastructure', 'serverless', 'paas'],
		slug: 'aws',
		experience: 3,
		level: 75,
		website: 'https://aws.amazon.com',
		websiteLabel: 'aws.amazon.com',
		github: '',
		githubLabel: '',
		firstRelease: '2006',
		license: 'Propriétaire',
		content: `Amazon Web Services (AWS) est la plateforme de services cloud la plus complète et largement adoptée au monde. Elle offre plus de 200 services complets de centres de données dans le monde entier, permettant aux entreprises de toutes tailles de réduire leurs coûts informatiques, gagner en agilité et innover plus rapidement.

			AWS propose une grande variété de services allant du calcul, du stockage, des bases de données jusqu'à l'intelligence artificielle, l'apprentissage automatique, l'IoT et bien plus encore.

			Principaux avantages d'AWS

			La scalabilité élastique d'AWS permet d'adapter rapidement les ressources en fonction des besoins, éliminant ainsi la nécessité de surestimer les capacités pour les pics d'utilisation. Le modèle de paiement à l'usage garantit que vous ne payez que pour les ressources que vous consommez effectivement, optimisant les coûts opérationnels. La disponibilité mondiale avec des régions et zones de disponibilité multiples assure une haute disponibilité et une résilience face aux pannes localisées.

			AWS offre une sécurité de niveau entreprise avec des contrôles d'accès granulaires (IAM), le chiffrement des données au repos et en transit, la protection contre les attaques DDoS, et la conformité avec de nombreuses certifications (ISO, SOC, HIPAA, etc.). L'innovation continue se traduit par des centaines de nouveaux services et fonctionnalités chaque année, permettant aux entreprises de rester à la pointe de la technologie.

			Parmi les services les plus populaires figurent EC2 pour le calcul, S3 pour le stockage d'objets, RDS pour les bases de données relationnelles, Lambda pour le calcul sans serveur, et CloudFormation pour l'infrastructure as code.`,
		resources: [
			{
				title: 'Documentation AWS',
				description: 'Documentation complète pour tous les services AWS',
				url: 'https://docs.aws.amazon.com/',
			},
			{
				title: 'AWS Well-Architected',
				description: "Bonnes pratiques pour l'architecture cloud",
				url: 'https://aws.amazon.com/architecture/well-architected/',
			},
			{
				title: 'AWS Training',
				description: 'Formations et certifications officielles AWS',
				url: 'https://aws.amazon.com/training/',
			},
			{
				title: 'AWS Samples',
				description: "Exemples de code et d'architecture pour AWS",
				url: 'https://github.com/aws-samples',
			},
		],
		relatedStacks: [
			{
				name: 'Terraform',
				logo: images.stacks.terraform,
				slug: 'terraform',
				category: 'devops',
			},
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Kubernetes',
				logo: images.stacks.kubernetes,
				slug: 'kubernetes',
				category: 'devops',
			},
		],
	},
	{
		id: 'golang',
		name: 'Go',
		description: "Langage de programmation open source conçu pour la simplicité et l'efficacité.",
		logo: images.stacks.golang,
		category: 'backend',
		tags: ['backend', 'language', 'compiled', 'concurrent', 'google'],
		slug: 'golang',
		experience: 2,
		level: 70,
		website: 'https://go.dev',
		websiteLabel: 'go.dev',
		github: 'https://github.com/golang/go',
		githubLabel: 'golang/go',
		firstRelease: '2009',
		license: 'BSD-3-Clause',
		content: `Go (ou Golang) est un langage de programmation open source développé par Google. Conçu pour être simple, efficace et fiable, Go combine la facilité d'utilisation des langages interprétés avec les performances et la sécurité des langages compilés.

			Particulièrement adapté aux systèmes distribués et aux applications nécessitant une haute concurrence, Go est largement utilisé dans le cloud computing, les microservices et les outils DevOps.

			Caractéristiques distinctives de Go

			La simplicité syntaxique de Go permet aux développeurs d'être rapidement productifs, avec peu de mots-clés et une approche minimaliste qui réduit la complexité du code. Sa compilation rapide transforme le code source en binaires natifs en quelques secondes, accélérant considérablement le cycle de développement. Le système de gestion de la concurrence basé sur les goroutines et les channels permet d'écrire facilement des programmes hautement parallèles qui utilisent efficacement les processeurs multi-cœurs.

			Go inclut un garbage collector moderne à faible latence qui gère automatiquement la mémoire sans sacrifier les performances. Sa bibliothèque standard complète fournit tout le nécessaire pour le développement web, le réseau, la cryptographie et bien plus encore. Les binaires statiques autonomes facilitent le déploiement sans dépendances externes, idéal pour les conteneurs et les environnements cloud.

			L'écosystème Go s'est considérablement développé avec des frameworks comme Gin et Echo pour le web, GORM pour l'ORM, et des outils comme Docker, Kubernetes et Terraform qui sont eux-mêmes écrits en Go.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Documentation et tutoriels pour Go',
				url: 'https://go.dev/doc/',
			},
			{
				title: 'Go by Example',
				description: 'Exemples pratiques de code Go',
				url: 'https://gobyexample.com/',
			},
			{
				title: 'Awesome Go',
				description: 'Liste curatée de frameworks, bibliothèques et logiciels Go',
				url: 'https://github.com/avelino/awesome-go',
			},
			{
				title: 'Go Playground',
				description: 'Environnement en ligne pour tester du code Go',
				url: 'https://play.golang.org/',
			},
		],
		relatedStacks: [
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Kubernetes',
				logo: images.stacks.kubernetes,
				slug: 'kubernetes',
				category: 'devops',
			},
			{
				name: 'PostgreSQL',
				logo: images.stacks.postgresql,
				slug: 'postgresql',
				category: 'database',
			},
		],
	},
	{
		id: 'svelte',
		name: 'Svelte',
		description: 'Framework JavaScript compilé qui déplace le travail du navigateur vers la compilation.',
		logo: images.stacks.svelte,
		category: 'frontend',
		tags: ['frontend', 'javascript', 'framework', 'reactive', 'compiler'],
		slug: 'svelte',
		experience: 2,
		level: 65,
		website: 'https://svelte.dev',
		websiteLabel: 'svelte.dev',
		github: 'https://github.com/sveltejs/svelte',
		githubLabel: 'sveltejs/svelte',
		firstRelease: '2016',
		license: 'MIT',
		content: `Svelte est un framework JavaScript radical qui prend une nouvelle approche de la construction d'interfaces utilisateur. Contrairement aux frameworks traditionnels comme React ou Vue qui font le gros du travail dans le navigateur, Svelte déplace ce travail dans une étape de compilation qui se produit lors de la construction de l'application.

			Le résultat est un code plus léger, plus rapide et avec une expérience de développement simplifiée, sans les complexités et surcoûts des DOM virtuels.

			Pourquoi choisir Svelte

			La simplicité de Svelte est frappante : son API intuitive et sa syntaxe claire permettent d'écrire moins de code pour obtenir les mêmes résultats qu'avec d'autres frameworks. En tant que framework compilé, Svelte génère un code JavaScript hautement optimisé qui manipule directement le DOM sans intermédiaire, résultant en des performances exceptionnelles et des bundles plus légers.

			La réactivité est intégrée au cœur de Svelte, avec des mises à jour automatiques de l'interface utilisateur lorsque l'état de l'application change, sans nécessiter de hooks ou de méthodes spéciales. L'animation est également simplifiée grâce à des transitions et des animations natives qui sont faciles à implémenter.

			Avec SvelteKit, un framework d'application similaire à Next.js ou Nuxt, Svelte propose une solution complète pour le développement d'applications web modernes avec le rendu côté serveur, la génération de sites statiques et une expérience de développement optimisée. L'approche "pas de runtime" de Svelte en fait un excellent choix pour les applications nécessitant des performances maximales et une empreinte minimale.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide complet et tutoriels pour Svelte',
				url: 'https://svelte.dev/docs',
			},
			{
				title: 'Svelte REPL',
				description: 'Environnement en ligne pour tester et partager du code Svelte',
				url: 'https://svelte.dev/repl',
			},
			{
				title: 'SvelteKit',
				description: "Framework d'application pour Svelte",
				url: 'https://kit.svelte.dev/',
			},
			{
				title: 'Svelte Society',
				description: 'Communauté et ressources pour Svelte',
				url: 'https://sveltesociety.dev/',
			},
		],
		relatedStacks: [
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
			{
				name: 'Vite',
				logo: images.stacks.vite,
				slug: 'vite',
				category: 'frontend',
			},
			{
				name: 'Sass',
				logo: images.stacks.sass,
				slug: 'sass',
				category: 'frontend',
			},
		],
	},
	{
		id: 'terraform',
		name: 'Terraform',
		description: "Outil d'infrastructure as code pour provisionner et gérer des ressources cloud.",
		logo: images.stacks.terraform,
		category: 'devops',
		tags: ['devops', 'infrastructure', 'iac', 'automation', 'hashicorp'],
		slug: 'terraform',
		experience: 3,
		level: 75,
		website: 'https://www.terraform.io',
		websiteLabel: 'terraform.io',
		github: 'https://github.com/hashicorp/terraform',
		githubLabel: 'hashicorp/terraform',
		firstRelease: '2014',
		license: 'MPL-2.0',
		content: `Terraform est un outil d'infrastructure as code (IaC) développé par HashiCorp qui permet aux utilisateurs de définir et de provisionner une infrastructure complète en utilisant un langage de configuration déclaratif simple.

			Avec Terraform, vous pouvez gérer des services et des ressources sur plusieurs fournisseurs de cloud (AWS, Azure, Google Cloud) ainsi que des services internes avec une syntaxe cohérente et une approche unifiée.

			Avantages de Terraform

			Le modèle déclaratif de Terraform permet de définir l'état souhaité de l'infrastructure plutôt que les étapes pour y parvenir, simplifiant considérablement la gestion des ressources complexes. Son approche multi-cloud permet d'utiliser la même syntaxe et les mêmes outils pour gérer des ressources sur différents fournisseurs, évitant l'enfermement propriétaire et facilitant les déploiements hybrides.

			La gestion d'état de Terraform suit précisément les ressources créées et leur configuration actuelle, permettant des mises à jour incrémentielles et une meilleure traçabilité des changements. La planification d'exécution (terraform plan) fournit un aperçu des modifications qui seront apportées avant leur application, réduisant les risques d'erreurs et de surprises.

			La modularité est encouragée via les modules Terraform, qui encapsulent des configurations réutilisables et partagées. L'écosystème comprend une vaste collection de fournisseurs pour presque tous les services cloud populaires et solutions d'infrastructure, ainsi que le Terraform Registry qui facilite le partage et la découverte de modules communautaires.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Documentation complète pour Terraform',
				url: 'https://developer.hashicorp.com/terraform/docs',
			},
			{
				title: 'Terraform Registry',
				description: 'Dépôt de modules et fournisseurs Terraform',
				url: 'https://registry.terraform.io/',
			},
			{
				title: 'Learn Terraform',
				description: 'Tutoriels interactifs pour apprendre Terraform',
				url: 'https://developer.hashicorp.com/terraform/tutorials',
			},
			{
				title: 'Terraform Best Practices',
				description: 'Guide des bonnes pratiques pour Terraform',
				url: 'https://www.terraform-best-practices.com/',
			},
		],
		relatedStacks: [
			{
				name: 'AWS',
				logo: images.stacks.aws,
				slug: 'aws',
				category: 'devops',
			},
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Kubernetes',
				logo: images.stacks.kubernetes,
				slug: 'kubernetes',
				category: 'devops',
			},
			{
				name: 'Ansible',
				logo: images.stacks.ansible,
				slug: 'ansible',
				category: 'devops',
			},
		],
	},
	{
		id: 'kubernetes',
		name: 'Kubernetes',
		description: "Plateforme open source pour l'orchestration de conteneurs.",
		logo: images.stacks.kubernetes,
		category: 'devops',
		tags: ['devops', 'container', 'orchestration', 'microservices', 'google'],
		slug: 'kubernetes',
		experience: 2,
		level: 70,
		website: 'https://kubernetes.io',
		websiteLabel: 'kubernetes.io',
		github: 'https://github.com/kubernetes/kubernetes',
		githubLabel: 'kubernetes/kubernetes',
		firstRelease: '2014',
		license: 'Apache-2.0',
		content: `Kubernetes (souvent abrégé en K8s) est une plateforme open source d'orchestration de conteneurs conçue pour automatiser le déploiement, la mise à l'échelle et la gestion des applications conteneurisées. Originellement développé par Google, il est maintenant maintenu par la Cloud Native Computing Foundation.

			Kubernetes permet de gérer des clusters d'instances informatiques et d'orchestrer des conteneurs sur ces instances selon les besoins des applications, offrant une plateforme solide pour des architectures en microservices.

			Caractéristiques clés de Kubernetes

			L'auto-réparation est l'une des fonctionnalités les plus puissantes de Kubernetes : il redémarre automatiquement les conteneurs qui échouent, remplace et replanifie les conteneurs lorsque les nœuds meurent, et tue les conteneurs qui ne répondent pas aux contrôles de santé. Le scaling horizontal automatique permet d'augmenter ou diminuer automatiquement le nombre de conteneurs en fonction de l'utilisation du CPU ou d'autres métriques définies.

			L'équilibrage de charge intégré distribue le trafic réseau entre les instances d'une application pour assurer la stabilité du déploiement. La découverte de services permet aux conteneurs de se trouver mutuellement via un système de nommage interne et d'équilibrage de charge. Les déploiements et rollbacks automatisés permettent de décrire l'état souhaité pour vos conteneurs déployés, et Kubernetes peut changer l'état réel vers l'état souhaité à un rythme contrôlé.

			La gestion de configuration secrète permet de stocker et gérer les informations sensibles comme les mots de passe et les tokens OAuth. Le stockage persistant offre un système de montage pour les données persistantes, permettant aux conteneurs d'accéder au même système de fichiers malgré les redémarrages. L'écosystème riche autour de Kubernetes comprend des outils comme Helm (gestionnaire de paquets), Istio (maillage de services), Prometheus (monitoring) et de nombreuses solutions certifiées par la CNCF.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Documentation complète pour Kubernetes',
				url: 'https://kubernetes.io/docs/home/',
			},
			{
				title: 'Kubernetes Playground',
				description: 'Laboratoire en ligne pour expérimenter Kubernetes',
				url: 'https://labs.play-with-k8s.com/',
			},
			{
				title: 'Kubernetes Patterns',
				description: 'Recueil de modèles de conception pour Kubernetes',
				url: 'https://k8spatterns.io/',
			},
			{
				title: 'CNCF Landscape',
				description: "Carte interactive de l'écosystème cloud native",
				url: 'https://landscape.cncf.io/',
			},
		],
		relatedStacks: [
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Terraform',
				logo: images.stacks.terraform,
				slug: 'terraform',
				category: 'devops',
			},
			{
				name: 'AWS',
				logo: images.stacks.aws,
				slug: 'aws',
				category: 'devops',
			},
			{
				name: 'Golang',
				logo: images.stacks.golang,
				slug: 'golang',
				category: 'backend',
			},
		],
	},
	{
		id: 'sass',
		name: 'Sass',
		description: "Langage d'extension CSS qui ajoute puissance et élégance au CSS de base.",
		logo: images.stacks.sass,
		category: 'frontend',
		tags: ['frontend', 'css', 'preprocessor', 'styling'],
		slug: 'sass',
		experience: 4,
		level: 90,
		website: 'https://sass-lang.com',
		websiteLabel: 'sass-lang.com',
		github: 'https://github.com/sass/sass',
		githubLabel: 'sass/sass',
		firstRelease: '2006',
		license: 'MIT',
		content: `Sass (Syntactically Awesome Style Sheets) est un langage de feuilles de style préprocesseur qui étend CSS avec des fonctionnalités puissantes comme les variables, les règles imbriquées, les mixins, les fonctions et plus encore. Le code Sass est compilé en CSS standard que les navigateurs peuvent comprendre.

			Disponible en deux syntaxes (SCSS, plus proche du CSS, et l'indentation Sass originale), il offre une façon plus organisée et efficace d'écrire des styles.

			Avantages de Sass

			Les variables permettent de stocker des couleurs, tailles de police et autres valeurs fréquemment utilisées pour une maintenance plus facile et cohérente. Les règles imbriquées reproduisent la hiérarchie visuelle du HTML et rendent le code plus lisible et organisé. Les mixins permettent de réutiliser des blocs entiers de styles et peuvent accepter des arguments pour créer des variations à partir d'un même modèle.

			Les fonctions intégrées de Sass offrent des capacités mathématiques et de manipulation de couleurs avancées, tandis que les opérateurs permettent d'effectuer des calculs directement dans les feuilles de style. Le système d'import permet de diviser les styles en fichiers plus petits et mieux organisés, avec la possibilité de créer des bibliothèques réutilisables.

			Les boucles et les conditionnels apportent une logique programmatique aux styles, permettant de générer des règles CSS basées sur des conditions ou de manière répétitive. L'héritage via @extend permet à un sélecteur d'hériter les styles d'un autre, favorisant la composition plutôt que la duplication de code. Avec les modules introduits dans Sass 3.5, il est encore plus facile de créer et maintenir des bibliothèques de styles réutilisables et bien organisées.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide et référence pour Sass',
				url: 'https://sass-lang.com/documentation/',
			},
			{
				title: 'Sass Guidelines',
				description: 'Guide de style opinionné pour du Sass propre et maintenable',
				url: 'https://sass-guidelin.es/fr/',
			},
			{
				title: 'Sassmeister',
				description: 'Playground en ligne pour tester du code Sass',
				url: 'https://www.sassmeister.com/',
			},
			{
				title: 'Awesome Sass',
				description: 'Collection de ressources Sass impressionnantes',
				url: 'https://github.com/Famolus/awesome-sass',
			},
		],
		relatedStacks: [
			{
				name: 'Vue.js',
				logo: images.stacks.vue,
				slug: 'vue-js',
				category: 'frontend',
			},
			{
				name: 'React',
				logo: images.stacks.react,
				slug: 'react',
				category: 'frontend',
			},
			{
				name: 'Svelte',
				logo: images.stacks.svelte,
				slug: 'svelte',
				category: 'frontend',
			},
		],
	},
	{
		id: 'django',
		name: 'Django',
		description: 'Framework web Python de haut niveau qui encourage le développement rapide et propre.',
		logo: images.stacks.django,
		category: 'backend',
		tags: ['backend', 'python', 'framework', 'orm', 'web'],
		slug: 'django',
		experience: 3,
		level: 80,
		website: 'https://www.djangoproject.com',
		websiteLabel: 'djangoproject.com',
		github: 'https://github.com/django/django',
		githubLabel: 'django/django',
		firstRelease: '2005',
		license: 'BSD-3-Clause',
		content: `Django est un framework web Python de haut niveau qui encourage le développement rapide, propre et pragmatique. Développé par des journalistes pour gérer les sites d'actualités, Django a évolué pour devenir l'un des frameworks web les plus populaires grâce à sa philosophie "batteries included" et son accent sur la sécurité et la scalabilité.

			Django suit le modèle architectural MVT (Model-View-Template), une variation du modèle MVC, et inclut un ORM puissant qui simplifie l'interaction avec les bases de données.

			Points forts de Django

			L'administration automatique de Django est l'une de ses fonctionnalités les plus appréciées, générant une interface d'administration complète et prête à l'emploi basée sur vos modèles de données. Son ORM puissant permet de définir des modèles de données en Python pur sans avoir à écrire de SQL, tout en offrant un contrôle fin sur les requêtes lorsque nécessaire.

			La sécurité est une priorité pour Django, qui inclut des protections robustes contre les vulnérabilités web courantes comme les injections SQL, les attaques XSS, CSRF et le clickjacking. La scalabilité est assurée par une architecture qui encourage la séparation des préoccupations et permet de déployer différentes parties de l'application sur différents serveurs.

			L'écosystème Django est riche, avec des milliers de packages réutilisables disponibles via PyPI, et une communauté active qui maintient le framework à jour avec les meilleures pratiques web. Django REST framework étend les capacités de Django pour construire facilement des API RESTful, tandis que des projets comme Channels ajoutent le support pour WebSockets et les communications asynchrones.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide complet et tutoriels pour Django',
				url: 'https://docs.djangoproject.com/',
			},
			{
				title: 'Django REST framework',
				description: 'Boîte à outils puissante pour construire des API Web',
				url: 'https://www.django-rest-framework.org/',
			},
			{
				title: 'Two Scoops of Django',
				description: 'Livre de bonnes pratiques pour Django',
				url: 'https://www.feldroy.com/books/two-scoops-of-django-3-x',
			},
			{
				title: 'Django Packages',
				description: 'Répertoire de packages et projets réutilisables',
				url: 'https://djangopackages.org/',
			},
		],
		relatedStacks: [
			{
				name: 'Python',
				logo: images.stacks.python,
				slug: 'python',
				category: 'backend',
			},
			{
				name: 'PostgreSQL',
				logo: images.stacks.postgresql,
				slug: 'postgresql',
				category: 'database',
			},
			{
				name: 'Nginx',
				logo: images.stacks.nginx,
				slug: 'nginx',
				category: 'devops',
			},
		],
	},
	{
		id: 'python',
		name: 'Python',
		description: 'Langage de programmation interprété, polyvalent et facile à apprendre.',
		logo: images.stacks.python,
		category: 'backend',
		tags: ['backend', 'language', 'scripting', 'data-science', 'ai'],
		slug: 'python',
		experience: 4,
		level: 90,
		website: 'https://www.python.org',
		websiteLabel: 'python.org',
		github: 'https://github.com/python/cpython',
		githubLabel: 'python/cpython',
		firstRelease: '1991',
		license: 'Python Software Foundation License',
		content: `Python est un langage de programmation interprété, de haut niveau et à usage général, créé par Guido van Rossum. Sa philosophie de conception met l'accent sur la lisibilité du code et sa syntaxe permet aux programmeurs d'exprimer des concepts en moins de lignes que dans d'autres langages.

			Python supporte plusieurs paradigmes de programmation, dont la programmation orientée objet, impérative, fonctionnelle et procédurale, et dispose d'un système de gestion de mémoire automatique.

			Avantages de Python

			La simplicité et la lisibilité de Python en font un excellent choix pour les débutants, avec une syntaxe claire qui ressemble presque à du pseudo-code ou à de l'anglais simplifié. Sa polyvalence permet de l'utiliser dans une variété de domaines : développement web, data science, intelligence artificielle, automatisation, scientifique, et bien plus encore.

			La bibliothèque standard extensive de Python offre des modules pour presque toutes les tâches courantes, tandis que l'écosystème PyPI (Python Package Index) contient plus de 300 000 packages tiers. L'interpréteur interactif de Python facilite l'expérimentation et le prototypage rapide, permettant de tester des idées sans avoir à compiler ou exécuter un programme complet.

			Python excelle en science des données avec des bibliothèques comme NumPy, pandas, et Matplotlib, et en apprentissage automatique avec TensorFlow, PyTorch et scikit-learn. Pour le développement web, des frameworks comme Django et Flask offrent des solutions robustes. La communauté Python est l'une des plus grandes et des plus actives, fournissant un support, des tutoriels et des ressources pour tous les niveaux de compétence.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Référence complète du langage Python',
				url: 'https://docs.python.org/fr/',
			},
			{
				title: 'Real Python',
				description: 'Tutoriels et articles sur Python',
				url: 'https://realpython.com/',
			},
			{
				title: 'PyPI',
				description: 'Index des packages Python',
				url: 'https://pypi.org/',
			},
			{
				title: 'Python Koans',
				description: 'Apprentissage de Python par la pratique',
				url: 'https://github.com/gregmalcolm/python_koans',
			},
		],
		relatedStacks: [
			{
				name: 'Django',
				logo: images.stacks.django,
				slug: 'django',
				category: 'backend',
			},
			{
				name: 'Flask',
				logo: images.stacks.python,
				slug: 'flask',
				category: 'backend',
			},
			{
				name: 'PostgreSQL',
				logo: images.stacks.postgresql,
				slug: 'postgresql',
				category: 'database',
			},
			{
				name: 'MongoDB',
				logo: images.stacks.mongodb,
				slug: 'mongodb',
				category: 'database',
			},
		],
	},
	{
		id: 'mongodb',
		name: 'MongoDB',
		description: 'Base de données NoSQL orientée document, flexible et scalable.',
		logo: images.stacks.mongodb,
		category: 'database',
		tags: ['database', 'nosql', 'document', 'schemaless', 'json'],
		slug: 'mongodb',
		experience: 3,
		level: 80,
		website: 'https://www.mongodb.com',
		websiteLabel: 'mongodb.com',
		github: 'https://github.com/mongodb/mongo',
		githubLabel: 'mongodb/mongo',
		firstRelease: '2009',
		license: 'Server Side Public License',
		content: `MongoDB est une base de données NoSQL orientée document, conçue pour le stockage, la récupération et la gestion de données sous forme de documents JSON. Contrairement aux bases de données relationnelles traditionnelles, MongoDB utilise un format de document flexible similaire à JSON (BSON) qui permet aux données d'être structurées ou non structurées.

			Cette flexibilité permet de faire évoluer facilement les schémas de données au fil du temps, ce qui est particulièrement adapté aux applications modernes avec des besoins de données en constante évolution.

			Points forts de MongoDB

			Le modèle de données orienté document de MongoDB permet de représenter des structures hiérarchiques complexes au sein d'un seul document, souvent éliminant le besoin de jointures et améliorant les performances de lecture. La flexibilité du schéma permet de stocker des documents avec différentes structures dans la même collection, et de faire évoluer le schéma au fil du temps sans migrations complexes.

			MongoDB excelle en scalabilité horizontale grâce à son architecture de sharding qui distribue les données sur plusieurs serveurs, permettant de gérer de très grands volumes de données et de trafic. Les index secondaires, y compris les index géospatiaux, textuels et composites, permettent d'optimiser les requêtes complexes et d'améliorer les performances.

			L'agrégation et les requêtes ad hoc offrent des capacités d'analyse puissantes directement dans la base de données. MongoDB Atlas, le service cloud géré, simplifie le déploiement et la gestion, avec des fonctionnalités avancées comme la sauvegarde automatique, la mise à l'échelle, et la sécurité. L'écosystème MongoDB inclut des pilotes pour la plupart des langages de programmation, des outils comme Compass pour l'exploration visuelle des données, et des intégrations avec des technologies populaires comme Hadoop et Spark.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guides et référence pour MongoDB',
				url: 'https://docs.mongodb.com/',
			},
			{
				title: 'MongoDB University',
				description: 'Cours gratuits et certifications sur MongoDB',
				url: 'https://university.mongodb.com/',
			},
			{
				title: 'MongoDB Atlas',
				description: 'Service de base de données cloud MongoDB',
				url: 'https://www.mongodb.com/cloud/atlas',
			},
			{
				title: 'MongoDB Compass',
				description: 'Interface graphique pour explorer et manipuler les données',
				url: 'https://www.mongodb.com/products/compass',
			},
		],
		relatedStacks: [
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
			{
				name: 'Express',
				logo: images.stacks.node,
				slug: 'express',
				category: 'backend',
			},
			{
				name: 'Python',
				logo: images.stacks.python,
				slug: 'python',
				category: 'backend',
			},
		],
	},
	{
		id: 'nginx',
		name: 'Nginx',
		description: 'Serveur web haute performance, proxy inverse et équilibreur de charge.',
		logo: images.stacks.nginx,
		category: 'devops',
		tags: ['devops', 'webserver', 'proxy', 'load-balancer', 'performance'],
		slug: 'nginx',
		experience: 3,
		level: 75,
		website: 'https://nginx.org',
		websiteLabel: 'nginx.org',
		github: 'https://github.com/nginx/nginx',
		githubLabel: 'nginx/nginx',
		firstRelease: '2004',
		license: 'BSD-2-Clause',
		content: `Nginx (prononcé "engine-x") est un serveur web open source, un proxy inverse, un équilibreur de charge et un proxy de cache. Conçu pour maximiser les performances et la stabilité, Nginx est connu pour sa capacité à gérer simultanément un grand nombre de connexions avec une faible empreinte mémoire.

			Initialement créé pour résoudre le problème C10k (gérer 10 000 connexions simultanées), Nginx est devenu l'un des serveurs web les plus populaires au monde, alimentant des sites de toutes tailles, des petits blogs aux plus grands sites web.

			Atouts de Nginx

			L'architecture événementielle asynchrone de Nginx lui permet de gérer des milliers de connexions simultanées par processus de travail, ce qui en fait une solution idéale pour les sites à fort trafic. Comme proxy inverse, il excelle dans la distribution du trafic vers plusieurs serveurs d'applications, permettant de sécuriser et d'optimiser l'infrastructure backend.

			L'équilibrage de charge intégré distribue les requêtes sur plusieurs serveurs selon différentes méthodes (round-robin, least connections, etc.), améliorant la disponibilité et la fiabilité. Les capacités de mise en cache permettent de stocker les réponses fréquemment demandées, réduisant la charge sur les serveurs backend et améliorant la vitesse de réponse pour les utilisateurs.

			La terminaison SSL/TLS efficace décharge le chiffrement et le déchiffrement des connexions sécurisées, optimisant les performances des applications. La modularité de Nginx permet d'étendre ses fonctionnalités avec des modules comme ngx_http_geoip_module pour la géolocalisation ou ModSecurity pour la sécurité.

			Nginx Plus, la version commerciale, ajoute des fonctionnalités avancées comme l'équilibrage de charge basé sur la session, la surveillance en temps réel, et le support professionnel, adaptées aux environnements d'entreprise exigeants.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide et référence pour Nginx',
				url: 'https://nginx.org/en/docs/',
			},
			{
				title: 'Nginx Blog',
				description: 'Articles et actualités sur Nginx',
				url: 'https://www.nginx.com/blog/',
			},
			{
				title: 'DigitalOcean Nginx Tutorials',
				description: 'Guides pratiques pour configurer Nginx',
				url: 'https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04',
			},
			{
				title: 'Nginx Admin Guide',
				description: "Guide d'administration pour Nginx",
				url: 'https://docs.nginx.com/nginx/admin-guide/',
			},
		],
		relatedStacks: [
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Node.js',
				logo: images.stacks.node,
				slug: 'node-js',
				category: 'backend',
			},
			{
				name: 'Django',
				logo: images.stacks.django,
				slug: 'django',
				category: 'backend',
			},
		],
	},
	{
		id: 'git',
		name: 'Git',
		description: 'Système de contrôle de version distribué rapide et efficace.',
		logo: images.stacks.git,
		category: 'tools',
		tags: ['devops', 'version-control', 'collaboration', 'essential'],
		slug: 'git',
		experience: 4,
		level: 90,
		website: 'https://git-scm.com',
		websiteLabel: 'git-scm.com',
		github: 'https://github.com/git/git',
		githubLabel: 'git/git',
		firstRelease: '2005',
		license: 'GPL-2.0',
		content: `Git est un système de contrôle de version distribué qui permet de suivre les modifications du code source pendant le développement logiciel. Créé par Linus Torvalds en 2005 pour le développement du noyau Linux, Git est devenu le standard de facto pour le contrôle de version dans l'industrie du logiciel.

			Contrairement aux systèmes de contrôle de version centralisés, Git donne à chaque développeur un dépôt local complet qui contient tout l'historique du projet, permettant un travail hors ligne et offrant une robustesse face aux pannes de serveur.

			Fonctionnalités clés de Git

			La nature distribuée de Git permet à chaque développeur de travailler indépendamment, avec une copie complète du dépôt incluant tout l'historique, facilitant le travail hors ligne et la création de branches expérimentales. Les branches légères sont l'une des forces de Git, permettant de créer et fusionner facilement différentes lignes de développement sans surcharge significative.

			L'intégrité des données est garantie par un système de hachage cryptographique, où chaque fichier et commit est identifié par un hash SHA-1, rendant pratiquement impossible toute corruption silencieuse. Le staging area (ou index) permet aux développeurs de préparer précisément quels changements seront inclus dans le prochain commit, offrant un contrôle fin sur l'historique du projet.

			L'écosystème autour de Git est immense, avec des plateformes comme GitHub, GitLab et Bitbucket qui ajoutent des fonctionnalités de collaboration comme les pull requests, le suivi des problèmes, et l'intégration continue. Des workflows comme Gitflow ou GitHub Flow formalisent les pratiques pour structurer le développement en équipe, standardisant les processus de branchement et de fusion.

			Les hooks Git permettent d'automatiser des actions à différentes étapes du cycle de commit, comme la vérification de la qualité du code ou le déploiement automatique. Malgré sa courbe d'apprentissage initiale, la maîtrise de Git est devenue une compétence essentielle pour tout développeur moderne.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Manuel de référence complet pour Git',
				url: 'https://git-scm.com/doc',
			},
			{
				title: 'Learn Git Branching',
				description: 'Application interactive pour apprendre Git',
				url: 'https://learngitbranching.js.org/',
			},
			{
				title: 'Pro Git Book',
				description: 'Livre complet sur Git, disponible gratuitement',
				url: 'https://git-scm.com/book/fr/v2',
			},
			{
				title: 'Oh Shit, Git!?!',
				description: 'Guide pour se sortir des situations difficiles avec Git',
				url: 'https://ohshitgit.com/fr',
			},
		],
		relatedStacks: [
			{
				name: 'GitHub',
				logo: images.stacks.git,
				slug: 'github',
				category: 'devops',
			},
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Ansible',
				logo: images.stacks.ansible,
				slug: 'ansible',
				category: 'devops',
			},
		],
	},
	{
		id: 'vite',
		name: 'Vite',
		description: 'Outil de build nouvelle génération pour le développement web moderne.',
		logo: images.stacks.vite,
		category: 'tools',
		tags: ['frontend', 'build-tool', 'bundler', 'development', 'vue'],
		slug: 'vite',
		experience: 3,
		level: 85,
		website: 'https://vitejs.dev',
		websiteLabel: 'vitejs.dev',
		github: 'https://github.com/vitejs/vite',
		githubLabel: 'vitejs/vite',
		firstRelease: '2020',
		license: 'MIT',
		content: `Vite (mot français pour "rapide") est un outil de build nouvelle génération pour le développement web moderne, créé par Evan You, le créateur de Vue.js. Vite offre une expérience de développement remarquablement rapide en tirant parti des fonctionnalités natives des modules ES des navigateurs modernes.

			Contrairement aux bundlers traditionnels qui traitent l'ensemble d'une application avant de servir le code, Vite adopte une approche différente qui divise les modules en deux catégories : les dépendances et le code source, permettant des temps de démarrage instantanés et des mises à jour à chaud ultra-rapides.

			Avantages de Vite

			Le serveur de développement ultra-rapide de Vite utilise les modules ES natifs, éliminant le besoin de bundler pendant le développement, ce qui permet des démarrages instantanés et des rechargements à chaud presque immédiats, même pour les grandes applications. L'optimisation des dépendances pré-bundle les bibliothèques tierces avec esbuild (écrit en Go), qui est 10 à 100 fois plus rapide que les bundlers JavaScript traditionnels.

			Vite est framework-agnostique, supportant officiellement Vue, React, Preact, Lit, Svelte et d'autres frameworks populaires via un système de plugins. La configuration est simple et intuitive, avec des valeurs par défaut sensées et la possibilité d'étendre les fonctionnalités via des plugins Rollup, utilisés pour la production.

			La production est optimisée avec Rollup, qui génère des bundles hautement optimisés avec la séparation du code, le tree-shaking, et d'autres optimisations. L'écosystème de plugins riche permet d'ajouter facilement le support pour TypeScript, JSX, CSS préprocesseurs, et bien plus encore.

			HMR (Hot Module Replacement) fonctionne de manière transparente, permettant de voir les changements instantanément dans le navigateur sans perdre l'état de l'application. L'API des plugins est unifiée pour le développement et la production, simplifiant la création d'outils intégrés.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide et référence pour Vite',
				url: 'https://vitejs.dev/guide/',
			},
			{
				title: 'Awesome Vite',
				description: 'Collection de ressources Vite',
				url: 'https://github.com/vitejs/awesome-vite',
			},
			{
				title: 'Vite Templates',
				description: 'Templates officiels pour démarrer avec Vite',
				url: 'https://github.com/vitejs/vite/tree/main/packages/create-vite',
			},
			{
				title: 'Vite Ecosystem CI',
				description: 'Compatibilité des plugins et bibliothèques avec Vite',
				url: 'https://github.com/vitejs/vite-ecosystem-ci',
			},
		],
		relatedStacks: [
			{
				name: 'Vue.js',
				logo: images.stacks.vue,
				slug: 'vue-js',
				category: 'frontend',
			},
			{
				name: 'React',
				logo: images.stacks.react,
				slug: 'react',
				category: 'frontend',
			},
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
			{
				name: 'Svelte',
				logo: images.stacks.svelte,
				slug: 'svelte',
				category: 'frontend',
			},
		],
	},
	{
		id: 'ansible',
		name: 'Ansible',
		description: "Outil d'automatisation IT simple mais puissant pour la configuration et le déploiement.",
		logo: images.stacks.ansible,
		category: 'devops',
		tags: ['devops', 'automation', 'configuration', 'deployment', 'infrastructure'],
		slug: 'ansible',
		experience: 3,
		level: 70,
		website: 'https://www.ansible.com',
		websiteLabel: 'ansible.com',
		github: 'https://github.com/ansible/ansible',
		githubLabel: 'ansible/ansible',
		firstRelease: '2012',
		license: 'GPL-3.0',
		content: `Ansible est une plateforme d'automatisation IT open source qui simplifie la gestion de configuration, le déploiement d'applications, et l'orchestration des tâches. Contrairement à d'autres outils d'automatisation, Ansible est agentless - il ne nécessite pas l'installation de logiciels spéciaux sur les nœuds gérés, utilisant simplement SSH pour se connecter et exécuter les tâches.

			Conçu pour être simple, mais puissant, Ansible décrit l'infrastructure en YAML, un format facile à lire et à écrire, rendant l'automatisation accessible à un large éventail de professionnels IT.

			Points forts d'Ansible

			L'approche agentless est l'une des caractéristiques distinctives d'Ansible : il utilise SSH (ou WinRM pour Windows) pour se connecter aux serveurs cibles, éliminant le besoin d'installer et de maintenir des agents sur chaque nœud. Les playbooks, écrits en YAML, offrent une syntaxe déclarative et lisible pour décrire l'état souhaité de l'infrastructure, facilitant la compréhension des processus d'automatisation.

			L'idempotence, un principe fondamental d'Ansible, garantit que l'exécution répétée d'un playbook produit toujours le même résultat, rendant les déploiements plus prévisibles et sécurisés. Les inventaires permettent de classer les serveurs en groupes et sous-groupes, facilitant la gestion de grands parcs informatiques et l'application de configurations spécifiques à différents environnements.

			Les rôles Ansible structurent les playbooks en unités réutilisables et partageables, favorisant les bonnes pratiques et la modularité. Ansible Galaxy, le hub communautaire, offre des milliers de rôles préconçus pour automatiser quasiment tous les aspects de l'infrastructure.

			AWX (et sa version commerciale, Ansible Tower) ajoute une interface web, des API REST, un contrôle d'accès basé sur les rôles, une planification des jobs, et une intégration avec les systèmes de notification, adaptés aux environnements d'entreprise.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide complet et référence pour Ansible',
				url: 'https://docs.ansible.com/',
			},
			{
				title: 'Ansible Galaxy',
				description: 'Hub pour partager et découvrir des rôles Ansible',
				url: 'https://galaxy.ansible.com/',
			},
			{
				title: 'Ansible for DevOps',
				description: "Livre sur l'utilisation d'Ansible pour l'automatisation",
				url: 'https://www.ansiblefordevops.com/',
			},
			{
				title: 'Red Hat Developer',
				description: 'Ressources et tutoriels pour Ansible',
				url: 'https://developers.redhat.com/topics/ansible',
			},
		],
		relatedStacks: [
			{
				name: 'Terraform',
				logo: images.stacks.terraform,
				slug: 'terraform',
				category: 'devops',
			},
			{
				name: 'Docker',
				logo: images.stacks.docker,
				slug: 'docker',
				category: 'devops',
			},
			{
				name: 'Kubernetes',
				logo: images.stacks.kubernetes,
				slug: 'kubernetes',
				category: 'devops',
			},
			{
				name: 'AWS',
				logo: images.stacks.aws,
				slug: 'aws',
				category: 'devops',
			},
		],
	},
	{
		id: 'flutter',
		name: 'Flutter',
		description: 'SDK de Google pour créer des applications multiplateformes avec une seule base de code.',
		logo: images.stacks.flutter,
		category: 'mobile',
		tags: ['mobile', 'cross-platform', 'ui-framework', 'dart', 'google'],
		slug: 'flutter',
		experience: 2,
		level: 65,
		website: 'https://flutter.dev',
		websiteLabel: 'flutter.dev',
		github: 'https://github.com/flutter/flutter',
		githubLabel: 'flutter/flutter',
		firstRelease: '2017',
		license: 'BSD-3-Clause',
		content: `Flutter est un SDK d'interface utilisateur open source créé par Google pour développer des applications nativement compilées pour mobile, web et desktop à partir d'une seule base de code. Utilisant le langage Dart, également développé par Google, Flutter propose une approche innovante du développement multiplateforme.

			Contrairement à d'autres frameworks multiplateformes qui utilisent des composants natifs ou des rendus web, Flutter dessine chaque pixel de l'interface utilisateur avec son propre moteur de rendu, offrant un contrôle précis sur l'apparence et le comportement des applications.

			Atouts de Flutter

			La philosophie "Write Once, Run Anywhere" de Flutter permet aux développeurs de maintenir une seule base de code qui fonctionne sur iOS, Android, web, Windows, macOS et Linux, réduisant considérablement le temps et les coûts de développement. Le Hot Reload accélère drastiquement le cycle de développement en permettant de voir immédiatement les changements de code dans l'application en cours d'exécution, sans perdre l'état actuel.

			L'approche "tout est un widget" de Flutter rend la construction d'interfaces utilisateur intuitive et flexible, avec des composants personnalisables qui maintiennent une apparence cohérente sur toutes les plateformes. Le moteur de rendu Skia, utilisé également par Chrome et Android, permet à Flutter de dessiner chaque pixel de l'UI, garantissant des interfaces fidèles à la conception et des animations fluides à 60fps.

			Les Material Design et Cupertino (iOS) widgets intégrés offrent des composants d'interface utilisateur qui suivent automatiquement les directives de conception des plateformes respectives. L'interopérabilité avec le code natif via les plugins et les canaux de plateforme permet d'accéder aux fonctionnalités spécifiques de chaque plateforme lorsque nécessaire.

			L'écosystème Flutter se développe rapidement, avec des milliers de packages sur pub.dev, la plateforme officielle de partage de code Dart et Flutter. Flutter est soutenu par Google et utilisé en interne pour plusieurs de leurs produits, garantissant un développement continu et un support à long terme.`,
		resources: [
			{
				title: 'Documentation officielle',
				description: 'Guide et tutoriels complets pour Flutter',
				url: 'https://docs.flutter.dev/',
			},
			{
				title: 'Flutter Cookbook',
				description: 'Recettes pour résoudre des problèmes courants en Flutter',
				url: 'https://docs.flutter.dev/cookbook',
			},
			{
				title: 'pub.dev',
				description: 'Dépôt officiel de packages pour Flutter',
				url: 'https://pub.dev/',
			},
			{
				title: 'Flutter Community',
				description: 'Articles et ressources de la communauté Flutter',
				url: 'https://fluttercommunity.dev/',
			},
		],
		relatedStacks: [
			{
				name: 'Firebase',
				logo: images.stacks.firebase,
				slug: 'firebase',
				category: 'backend',
			},
			{
				name: 'Dart',
				logo: images.stacks.flutter,
				slug: 'dart',
				category: 'frontend',
			},
			{
				name: 'TypeScript',
				logo: images.stacks.typescript,
				slug: 'typescript',
				category: 'frontend',
			},
		],
	},
	{
		id: 'figma',
		name: 'Figma',
		description: "Outil de conception d'interface collaboratif basé sur le web.",
		logo: images.stacks.figma,
		category: 'design',
		tags: ['design', 'ui', 'ux', 'prototyping', 'collaboration'],
		slug: 'figma',
		experience: 3,
		level: 80,
		website: 'https://www.figma.com',
		websiteLabel: 'figma.com',
		github: '',
		githubLabel: '',
		firstRelease: '2016',
		license: 'Propriétaire',
		content: `Figma est une application de conception d'interface utilisateur et de prototypage basée sur le web qui permet aux équipes de collaborer en temps réel. Lancé en 2016, Figma a rapidement gagné en popularité grâce à sa nature collaborative, ses performances impressionnantes et sa facilité d'accès sur différentes plateformes.

			Contrairement aux outils de conception traditionnels qui nécessitent des installations locales et des transferts de fichiers, Figma fonctionne directement dans le navigateur, permettant une collaboration en temps réel similaire à Google Docs mais pour la conception.

			Points forts de Figma

			La collaboration en temps réel est la fonctionnalité phare de Figma, permettant à plusieurs concepteurs et parties prenantes de travailler simultanément sur le même fichier, voyant les modifications les uns des autres instantanément. L'accès multiplateforme via le navigateur web ou l'application de bureau élimine les barrières d'entrée et assure que tous les utilisateurs ont toujours la dernière version.

			Les composants et les styles réutilisables permettent de créer des systèmes de conception cohérents et maintenables, avec des mises à jour propagées automatiquement dans tout le projet. Les bibliothèques partagées facilitent la gestion des actifs de conception à l'échelle de l'organisation, assurant la cohérence entre les projets et les équipes.

			Le prototypage interactif permet de créer des simulations fonctionnelles d'interfaces avec des transitions, des animations et des interactions, comblant le fossé entre la conception statique et l'expérience utilisateur dynamique. Les plugins et l'API Figma étendent les fonctionnalités de base, permettant l'automatisation et l'intégration avec d'autres outils de conception et de développement.

			Les fonctionnalités de commentaire et de feedback facilitent la communication et la révision au sein de l'équipe élargie, y compris les développeurs, les gestionnaires de produits et autres parties prenantes. L'intégration avec des outils de gestion de projet et de code comme Jira, GitHub et Slack renforce la collaboration entre les équipes de conception et de développement.`,
		resources: [
			{
				title: 'Aide Figma',
				description: "Centre d'aide et documentation officielle",
				url: 'https://help.figma.com/',
			},
			{
				title: 'Figma Community',
				description: 'Ressources, templates et plugins partagés par la communauté',
				url: 'https://www.figma.com/community',
			},
			{
				title: 'Figma Design',
				description: 'Blog officiel avec des tutoriels et études de cas',
				url: 'https://www.figma.com/blog/',
			},
			{
				title: 'Figma YouTube',
				description: 'Chaîne officielle avec des tutoriels vidéo',
				url: 'https://www.youtube.com/c/Figmadesign',
			},
		],
		relatedStacks: [
			{
				name: 'Photoshop',
				logo: images.stacks.photoshop,
				slug: 'photoshop',
				category: 'design',
			},
			{
				name: 'Illustrator',
				logo: images.stacks.illustrator,
				slug: 'illustrator',
				category: 'design',
			},
			{
				name: 'HTML/CSS',
				logo: images.stacks.sass,
				slug: 'html-css',
				category: 'frontend',
			},
		],
	},
	{
		id: 'photoshop',
		name: 'Adobe Photoshop',
		description: "Logiciel de référence pour l'édition d'images et la création graphique.",
		logo: images.stacks.photoshop,
		category: 'design',
		tags: ['design', 'image-editing', 'photography', 'creative', 'adobe'],
		slug: 'photoshop',
		experience: 3,
		level: 75,
		website: 'https://www.adobe.com/products/photoshop.html',
		websiteLabel: 'adobe.com/photoshop',
		github: '',
		githubLabel: '',
		firstRelease: '1990',
		license: 'Propriétaire',
		content: `Adobe Photoshop est le logiciel de référence mondial pour l'édition d'images, la conception graphique, la retouche photo et la composition numérique. Depuis son lancement en 1990, Photoshop est devenu un outil essentiel pour les professionnels de la création et s'est imposé comme le standard de l'industrie pour le traitement d'images.

			Avec ses capacités puissantes et sa flexibilité exceptionnelle, Photoshop permet aux designers, photographes et artistes de manipuler des images avec une précision pixel par pixel et de créer pratiquement n'importe quelle vision créative.

			Fonctionnalités clés de Photoshop

			Le système de calques, l'une des innovations les plus importantes de Photoshop, permet de travailler sur différents éléments d'une image séparément, facilitant les modifications non destructives et les compositions complexes. Les outils de sélection précis (lasso, sélection rapide, sélection par plage de couleurs) permettent d'isoler et de modifier des parties spécifiques d'une image avec une grande précision.

			Les filtres et réglages non destructifs offrent des moyens puissants pour ajuster les couleurs, la luminosité, le contraste et autres propriétés de l'image tout en préservant les données originales. Les masques de calque et masques vectoriels permettent de contrôler avec précision la visibilité de différentes parties de l'image, essentiels pour les compositions et retouches avancées.

			Le support des graphiques vectoriels, comprenant les textes, formes et tracés, combine la flexibilité du dessin vectoriel avec la richesse des images matricielles. L'automatisation via les actions et les scripts permet de rationaliser les flux de travail répétitifs, économisant un temps précieux sur les tâches routinières.

			L'intégration avec la suite Adobe Creative Cloud facilite le passage entre Photoshop et d'autres applications comme Illustrator, InDesign et After Effects pour des projets multimédias complets. Les dernières versions incluent des outils d'intelligence artificielle comme Select Subject et Neural Filters qui révolutionnent certaines tâches autrefois laborieuses, comme la sélection précise de sujets ou le vieillissement/rajeunissement de portraits.`,
		resources: [
			{
				title: 'Documentation Adobe',
				description: 'Guide utilisateur officiel pour Photoshop',
				url: 'https://helpx.adobe.com/fr/photoshop/user-guide.html',
			},
			{
				title: 'Adobe Photoshop Tutorials',
				description: 'Tutoriels officiels pour tous les niveaux',
				url: 'https://helpx.adobe.com/fr/photoshop/tutorials.html',
			},
			{
				title: 'Envato Tuts+',
				description: 'Collection de tutoriels Photoshop approfondis',
				url: 'https://design.tutsplus.com/categories/adobe-photoshop',
			},
			{
				title: 'Photoshop Café',
				description: 'Astuces, tutoriels et ressources pour Photoshop',
				url: 'https://photoshopcafe.com/',
			},
		],
		relatedStacks: [
			{
				name: 'Illustrator',
				logo: images.stacks.illustrator,
				slug: 'illustrator',
				category: 'design',
			},
			{
				name: 'Figma',
				logo: images.stacks.figma,
				slug: 'figma',
				category: 'design',
			},
			{
				name: 'CSS',
				logo: images.stacks.sass,
				slug: 'css',
				category: 'frontend',
			},
		],
	},
	{
		id: 'illustrator',
		name: 'Adobe Illustrator',
		description: 'Logiciel de création graphique vectorielle de référence.',
		logo: images.stacks.illustrator,
		category: 'design',
		tags: ['design', 'vector', 'graphics', 'creative', 'adobe'],
		slug: 'illustrator',
		experience: 2,
		level: 70,
		website: 'https://www.adobe.com/products/illustrator.html',
		websiteLabel: 'adobe.com/illustrator',
		github: '',
		githubLabel: '',
		firstRelease: '1987',
		license: 'Propriétaire',
		content: `Adobe Illustrator est le logiciel de référence pour la création graphique vectorielle, utilisé par des millions de designers et d'artistes à travers le monde. Lancé en 1987, Illustrator a défini les standards de l'industrie pour le dessin vectoriel et reste l'outil privilégié pour la création de logos, d'illustrations, d'icônes et de travaux graphiques nécessitant une mise à l'échelle sans perte de qualité.

			Contrairement aux graphiques bitmap (comme ceux créés dans Photoshop), les créations vectorielles d'Illustrator sont basées sur des formules mathématiques, permettant de les redimensionner à l'infini sans dégradation de la qualité.

			Atouts d'Illustrator

			Les outils de dessin vectoriel précis comme le crayon, la plume et les formes primitives permettent de créer des illustrations complexes avec des courbes parfaites et des lignes nettes. Le système de calques offre un contrôle organisationnel sur les éléments de conception, facilitant la gestion de projets complexes et les modifications non destructives.

			Les dégradés avancés, y compris les dégradés de formes et de maillage, permettent de créer des transitions de couleur complexes et des effets de profondeur réalistes. Les outils de typographie sophistiqués offrent un contrôle précis sur le texte, essentiel pour les logos, les affiches et autres conceptions incorporant des éléments textuels.

			Les symboles et les modèles permettent de réutiliser facilement des éléments graphiques, améliorant l'efficacité et la cohérence dans les projets à grande échelle. L'intégration avec Adobe Creative Cloud facilite le flux de travail entre Illustrator et d'autres applications Adobe comme Photoshop, InDesign et After Effects.

			Les fonctionnalités de préparation à la production, comme les repères d'impression, la séparation des couleurs et le support des profils ICC, assurent que les conceptions sont prêtes pour l'impression professionnelle. Les capacités d'exportation flexibles permettent de générer des actifs dans divers formats pour le web, l'impression et les applications mobiles.`,
		resources: [
			{
				title: 'Documentation Adobe',
				description: 'Guide utilisateur officiel pour Illustrator',
				url: 'https://helpx.adobe.com/fr/illustrator/user-guide.html',
			},
			{
				title: 'Adobe Illustrator Tutorials',
				description: 'Tutoriels officiels pour tous les niveaux',
				url: 'https://helpx.adobe.com/fr/illustrator/tutorials.html',
			},
			{
				title: 'Illustrator Vector Tutorials',
				description: 'Collection de tutoriels avancés pour Illustrator',
				url: 'https://vector.tutsplus.com/categories/adobe-illustrator',
			},
			{
				title: 'Vectips',
				description: 'Blog spécialisé dans les techniques Illustrator',
				url: 'https://vectips.com/',
			},
		],
		relatedStacks: [
			{
				name: 'Photoshop',
				logo: images.stacks.photoshop,
				slug: 'photoshop',
				category: 'design',
			},
			{
				name: 'Figma',
				logo: images.stacks.figma,
				slug: 'figma',
				category: 'design',
			},
			{
				name: 'SVG',
				logo: images.stacks.illustrator,
				slug: 'svg',
				category: 'frontend',
			},
		],
	},
];

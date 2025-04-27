/**
 * Configuration centralisée des images
 * Utilise les imports dynamiques de Vite pour gérer correctement les chemins d'images
 */

// Déclaration de type pour import.meta.glob
declare global {
	interface ImportMeta {
		glob: (pattern: string, options?: { eager?: boolean }) => Record<string, any>;
	}
}

// Importation de l'helper glob de Vite pour l'importation des assets
const imageModules = import.meta.glob('/src/assets/images/**/*.*', { eager: true });

// Type pour les différentes catégories d'images
export interface ImageCategory {
	[key: string]: string;
}

// Helper pour obtenir le chemin relatif complet
const getImagePath = (path: string): string => {
	// Résolution dynamique du chemin complet
	const modulePath = `/src${path.split('/src')[1]}`;
	const module = imageModules[modulePath] as any;

	// Retourne le chemin résolu ou un placeholder en cas d'erreur
	return module?.default || `/api/placeholder/200/200?text=${path.split('/').pop()}`;
};

// Articles
const articles: ImageCategory = {
	article1: getImagePath('/src/assets/images/article/article-1.jpg'),
	article2: getImagePath('/src/assets/images/article/article-2.jpg'),
	article3: getImagePath('/src/assets/images/article/article-3.jpg'),
	article4: getImagePath('/src/assets/images/article/article-4.jpg'),
	article5: getImagePath('/src/assets/images/article/article-5.jpg'),
};

// Projets
const projects: ImageCategory = {
	project1: getImagePath('/src/assets/images/project/projet-1.jpg'),
	project2: getImagePath('/src/assets/images/project/projet-2.jpg'),
	project3: getImagePath('/src/assets/images/project/projet-3.jpg'),
	project4: getImagePath('/src/assets/images/project/projet-4.jpg'),
	project5: getImagePath('/src/assets/images/project/projet-5.jpg'),
};

// Technologies/Stack
const stacks: ImageCategory = {
	aws: getImagePath('/src/assets/images/stack/aws.svg'),
	django: getImagePath('/src/assets/images/stack/django.svg'),
	docker: getImagePath('/src/assets/images/stack/docker.svg'),
	figma: getImagePath('/src/assets/images/stack/figma.svg'),
	flutter: getImagePath('/src/assets/images/stack/flutter.svg'),
	git: getImagePath('/src/assets/images/stack/git.svg'),
	golang: getImagePath('/src/assets/images/stack/golang.svg'),
	illustrator: getImagePath('/src/assets/images/stack/illustrator.svg'),
	mongodb: getImagePath('/src/assets/images/stack/mongodb.svg'),
	nest: getImagePath('/src/assets/images/stack/nest.svg'),
	nginx: getImagePath('/src/assets/images/stack/nginx.svg'),
	node: getImagePath('/src/assets/images/stack/node.svg'),
	photoshop: getImagePath('/src/assets/images/stack/photoshop.svg'),
	postgresql: getImagePath('/src/assets/images/stack/postgresql.svg'),
	python: getImagePath('/src/assets/images/stack/python.svg'),
	react: getImagePath('/src/assets/images/stack/react.svg'),
	sass: getImagePath('/src/assets/images/stack/sass.svg'),
	svelte: getImagePath('/src/assets/images/stack/svelte.svg'),
	terraform: getImagePath('/src/assets/images/stack/terraform.svg'),
	typescript: getImagePath('/src/assets/images/stack/typescript.svg'),
	vite: getImagePath('/src/assets/images/stack/vite.svg'),
	vue: getImagePath('/src/assets/images/stack/vue.svg'),
	ansible: getImagePath('/src/assets/images/stack/ansible.svg'),
	kubernetes: getImagePath('/src/assets/images/stack/kubernetes.svg'),
};

// Autres images
const others: ImageCategory = {
	logo: getImagePath('/src/assets/images/logo.png'),
	profilePhoto: getImagePath('/src/assets/images/Photo Profile.JPG'),
};

// Export consolidé de toutes les images
export const images = {
	articles,
	projects,
	stacks,
	others,
	// Liste complète de toutes les images
	all: {
		...articles,
		...projects,
		...stacks,
		...others,
	},
};

// Export par défaut
export default images;

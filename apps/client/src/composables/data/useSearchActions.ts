import { computed } from 'vue';
import { useRouter } from 'vue-router';

import { SITE_CONFIG } from '@/composables/seo/useSeo';

import type { SearchAction } from '@/types/composables/data';

export type { SearchAction };

export function useSearchActions() {
    const router = useRouter();
    const email = SITE_CONFIG.author.email;

    async function copyEmail() {
        if (!navigator?.clipboard) {
            return;
        }
        try {
            await navigator.clipboard.writeText(email);
        } catch (err) {
            console.warn('[search-actions] clipboard write failed:', err);
        }
    }

    const actions = computed<SearchAction[]>(() => [
        {
            id: 'nav-blog',
            title: 'Aller au blog',
            subtitle: 'Articles techniques',
            icon: 'blog',
            link: '/blog',
        },
        {
            id: 'nav-projects',
            title: 'Voir les projets',
            subtitle: 'Réalisations',
            icon: 'projects',
            link: '/projects',
        },
        {
            id: 'nav-stacks',
            title: 'Voir les stacks',
            subtitle: 'Compétences techniques',
            icon: 'stacks',
            link: '/stacks',
        },
        {
            id: 'nav-contact',
            title: 'Me contacter',
            subtitle: 'Formulaire + FAQ',
            icon: 'mail',
            link: '/contact',
        },
        {
            id: 'copy-email',
            title: 'Copier mon email',
            subtitle: email,
            icon: 'link',
            run: copyEmail,
        },
        {
            id: 'ext-github',
            title: 'GitHub',
            subtitle: 'github.com/jubskan3ki',
            icon: 'github',
            link: 'https://github.com/jubskan3ki',
            external: true,
        },
        {
            id: 'ext-linkedin',
            title: 'LinkedIn',
            subtitle: 'linkedin.com/in/juba-aitadda',
            icon: 'linkedin',
            link: 'https://www.linkedin.com/in/juba-aitadda/',
            external: true,
        },
    ]);

    async function run(action: SearchAction) {
        if (action.run) {
            await action.run();
            return;
        }
        if (!action.link) {
            return;
        }
        if (action.external) {
            if (typeof window !== 'undefined') {
                window.open(action.link, '_blank', 'noopener');
            }
            return;
        }
        router.push(action.link);
    }

    return { actions, run };
}

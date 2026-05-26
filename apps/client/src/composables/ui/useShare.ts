import type { MaybeRef } from 'vue';
import { computed, ref, toValue } from 'vue';
import type { UseShareReturn } from '@/types/composables/ui';

export function useShare(title: MaybeRef<string>): UseShareReturn {
    const linkCopied = ref(false);

    const shareUrl = computed(() => {
        if (import.meta.client) {
            return window.location.href;
        }
        return '';
    });

    const shareOn = (platform: 'twitter' | 'linkedin') => {
        const text = encodeURIComponent(toValue(title));
        const url = encodeURIComponent(shareUrl.value);

        const urls: Record<string, string> = {
            twitter: `https://twitter.com/intent/tweet?text=${text}&url=${url}`,
            linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
        };

        window.open(urls[platform], '_blank', 'noopener,noreferrer,width=600,height=400');
    };

    const copyLink = async () => {
        try {
            await navigator.clipboard.writeText(shareUrl.value);
            linkCopied.value = true;
            setTimeout(() => {
                linkCopied.value = false;
            }, 2000);
        } catch {
            /* noop */
        }
    };

    return { shareUrl, linkCopied, shareOn, copyLink };
}

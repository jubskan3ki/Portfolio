import type { MaybeRef } from 'vue';
import { computed, onScopeDispose, ref, toValue } from 'vue';
import type { UseShareReturn } from '@/types/composables/ui';

export function useShare(title: MaybeRef<string>): UseShareReturn {
    const linkCopied = ref(false);
    let resetTimer: ReturnType<typeof setTimeout> | null = null;

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
            if (resetTimer) {
                clearTimeout(resetTimer);
            }
            resetTimer = setTimeout(() => {
                linkCopied.value = false;
                resetTimer = null;
            }, 2000);
        } catch {
            /* noop */
        }
    };

    onScopeDispose(() => {
        if (resetTimer) {
            clearTimeout(resetTimer);
        }
    });

    return { shareUrl, linkCopied, shareOn, copyLink };
}

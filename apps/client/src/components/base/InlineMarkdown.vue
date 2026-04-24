<script lang="ts">
    import { defineComponent, h, type PropType, type VNode } from 'vue';

    import { parseInlineMarkdown } from '@/services/utils/contentParser';

    import type { InlineNode } from '@/types/feature/blog';

    // Rendu VNode récursif : Vue échappe automatiquement les textes
    // (zéro injection HTML, pas besoin de v-html).
    function renderNode(n: InlineNode): VNode | string {
        if (n.type === 'text') {
            return n.content;
        }
        if (n.type === 'code') {
            return h('code', n.content);
        }
        if (n.type === 'strong') {
            return h('strong', n.children.map(renderNode));
        }
        if (n.type === 'em') {
            return h('em', n.children.map(renderNode));
        }
        return h(
            'a',
            { href: n.url, target: '_blank', rel: 'noopener noreferrer' },
            n.children.map(renderNode),
        );
    }

    export default defineComponent({
        name: 'InlineMarkdown',
        props: {
            text: { type: String as PropType<string>, required: true },
        },
        setup(props) {
            // Render function pure : pas de template à compiler, pas d'instance enfant.
            return () => parseInlineMarkdown(props.text).map(renderNode);
        },
    });
</script>

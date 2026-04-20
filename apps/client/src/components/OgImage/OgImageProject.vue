<template>
    <div
        :style="{
            width: '100%',
            height: '100%',
            display: 'flex',
            background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #312e81 100%)',
            fontFamily: 'Lato, sans-serif',
            color: '#ffffff',
        }"
    >
        <div
            :style="{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '60px',
                flex: 1,
            }"
        >
            <div :style="{ display: 'flex', alignItems: 'center', gap: '14px' }">
                <span
                    :style="{
                        display: 'flex',
                        fontSize: '14px',
                        fontWeight: 700,
                        color: '#a78bfa',
                        textTransform: 'uppercase',
                        letterSpacing: '0.18em',
                    }"
                >
                    Projet
                </span>
                <span
                    v-if="category"
                    :style="{
                        display: 'flex',
                        fontSize: '14px',
                        fontWeight: 600,
                        color: '#cbd5e1',
                        textTransform: 'uppercase',
                        letterSpacing: '0.12em',
                        padding: '6px 14px',
                        borderRadius: '999px',
                        border: '1px solid rgba(203, 213, 225, 0.25)',
                    }"
                >
                    {{ category }}
                </span>
            </div>

            <div
                :style="{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '20px',
                }"
            >
                <h1
                    :style="{
                        fontSize: title.length > 45 ? '52px' : '64px',
                        fontWeight: 700,
                        lineHeight: 1.1,
                        letterSpacing: '-0.03em',
                        margin: 0,
                    }"
                >
                    {{ title }}
                </h1>
                <p
                    v-if="description"
                    :style="{
                        display: '-webkit-box',
                        fontSize: '20px',
                        color: '#cbd5e1',
                        lineHeight: 1.5,
                        margin: 0,
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                    }"
                >
                    {{ description }}
                </p>
            </div>

            <div
                :style="{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }"
            >
                <div :style="{ display: 'flex', gap: '10px' }">
                    <span
                        v-for="tech in visibleTech"
                        :key="tech"
                        :style="{
                            display: 'flex',
                            fontSize: '16px',
                            fontWeight: 600,
                            color: '#e0e7ff',
                            background: 'rgba(99, 102, 241, 0.18)',
                            border: '1px solid rgba(167, 139, 250, 0.35)',
                            padding: '8px 16px',
                            borderRadius: '10px',
                        }"
                    >
                        {{ tech }}
                    </span>
                </div>
                <div :style="{ display: 'flex', alignItems: 'center', gap: '12px' }">
                    <div
                        :style="{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '44px',
                            height: '44px',
                            borderRadius: '999px',
                            background: 'linear-gradient(135deg, #a78bfa, #6366f1)',
                            fontSize: '18px',
                            fontWeight: 700,
                        }"
                    >
                        JA
                    </div>
                    <span :style="{ fontSize: '16px', fontWeight: 600 }">juba-aitadda.dev</span>
                </div>
            </div>
        </div>

        <div
            v-if="image"
            :style="{
                display: 'flex',
                width: '380px',
                height: '100%',
                position: 'relative',
                overflow: 'hidden',
            }"
        >
            <img
                :src="image"
                :style="{ width: '100%', height: '100%', objectFit: 'cover' }"
                alt=""
            />
            <div
                :style="{
                    position: 'absolute',
                    inset: 0,
                    display: 'flex',
                    background: 'linear-gradient(270deg, transparent 60%, rgba(15, 23, 42, 0.9))',
                }"
            ></div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    const props = withDefaults(
        defineProps<{
            title: string;
            description?: string;
            image?: string;
            category?: string;
            technologies?: string[];
        }>(),
        {
            description: '',
            image: '',
            category: '',
            technologies: () => [],
        },
    );

    const visibleTech = computed(() => (props.technologies ?? []).slice(0, 4));
</script>

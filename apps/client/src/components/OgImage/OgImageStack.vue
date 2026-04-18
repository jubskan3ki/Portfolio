<template>
    <div
        :style="{
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            padding: '72px',
            background: 'radial-gradient(circle at top left, #312e81 0%, #0f172a 60%, #020617 100%)',
            fontFamily: 'Lato, sans-serif',
            color: '#ffffff',
            position: 'relative',
        }"
    >
        <!-- Top: label -->
        <span
            :style="{
                display: 'flex',
                fontSize: '14px',
                fontWeight: 700,
                color: '#a78bfa',
                textTransform: 'uppercase',
                letterSpacing: '0.22em',
            }"
        >
            Compétence · Stack
        </span>

        <!-- Core: logo + name -->
        <div
            :style="{
                display: 'flex',
                alignItems: 'center',
                gap: '36px',
            }"
        >
            <div
                v-if="logo"
                :style="{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '200px',
                    height: '200px',
                    borderRadius: '32px',
                    background: 'rgba(255, 255, 255, 0.06)',
                    border: '1px solid rgba(167, 139, 250, 0.35)',
                    flexShrink: 0,
                }"
            >
                <img
                    :src="logo"
                    :style="{ width: '140px', height: '140px', objectFit: 'contain' }"
                    alt=""
                />
            </div>
            <div
                :style="{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '14px',
                    flex: 1,
                }"
            >
                <h1
                    :style="{
                        fontSize: '82px',
                        fontWeight: 700,
                        letterSpacing: '-0.03em',
                        lineHeight: 1,
                        margin: 0,
                    }"
                >
                    {{ name }}
                </h1>
                <div
                    v-if="levelLabel"
                    :style="{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                    }"
                >
                    <span
                        :style="{
                            display: 'flex',
                            fontSize: '18px',
                            fontWeight: 700,
                            color: '#0f172a',
                            background: 'linear-gradient(135deg, #a78bfa, #818cf8)',
                            padding: '6px 16px',
                            borderRadius: '999px',
                            letterSpacing: '0.06em',
                            textTransform: 'uppercase',
                        }"
                    >
                        {{ levelLabel }}
                    </span>
                    <div
                        :style="{
                            display: 'flex',
                            gap: '4px',
                            alignItems: 'center',
                        }"
                    >
                        <span
                            v-for="n in 5"
                            :key="n"
                            :style="{
                                display: 'flex',
                                width: '16px',
                                height: '16px',
                                borderRadius: '999px',
                                background: n <= Math.round(level) ? '#a78bfa' : 'rgba(167, 139, 250, 0.18)',
                            }"
                        ></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottom: identity + description -->
        <div
            :style="{
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'space-between',
                gap: '40px',
            }"
        >
            <p
                v-if="description"
                :style="{
                    display: '-webkit-box',
                    fontSize: '20px',
                    color: '#cbd5e1',
                    lineHeight: 1.45,
                    margin: 0,
                    maxWidth: '720px',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                }"
            >
                {{ description }}
            </p>
            <span :style="{ display: 'flex', fontSize: '16px', color: '#94a3b8', fontWeight: 600, flexShrink: 0 }">
                juba-aitadda.dev
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';

    const props = withDefaults(
        defineProps<{
            name: string;
            description?: string;
            logo?: string;
            level?: number;
        }>(),
        {
            description: '',
            logo: '',
            level: 0,
        },
    );

    const levelLabel = computed(() => {
        const lvl = props.level ?? 0;
        if (lvl >= 4.5) {
            return 'Expert';
        }
        if (lvl >= 3.5) {
            return 'Advanced';
        }
        if (lvl >= 2.5) {
            return 'Intermediate';
        }
        if (lvl > 0) {
            return 'Beginner';
        }
        return '';
    });
</script>

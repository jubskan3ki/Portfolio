<template>
    <div
        :style="{
            width: '100%',
            height: '100%',
            display: 'flex',
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
            fontFamily: 'Lato, sans-serif',
            color: '#ffffff',
            position: 'relative',
        }"
    >
        <div
            v-if="image"
            :style="{
                display: 'flex',
                width: '420px',
                height: '100%',
                position: 'relative',
                overflow: 'hidden',
                borderRight: '4px solid rgba(167, 139, 250, 0.35)',
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
                    background: 'linear-gradient(90deg, transparent 40%, rgba(22, 33, 62, 0.85))',
                    display: 'flex',
                }"
            ></div>
        </div>

        <div
            :style="{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '60px',
                flex: 1,
            }"
        >
            <div :style="{ display: 'flex', alignItems: 'center', gap: '16px' }">
                <span
                    v-if="category"
                    :style="{
                        display: 'flex',
                        alignItems: 'center',
                        fontSize: '18px',
                        fontWeight: 700,
                        color: '#a78bfa',
                        textTransform: 'uppercase',
                        letterSpacing: '0.12em',
                        background: 'rgba(167, 139, 250, 0.12)',
                        padding: '8px 16px',
                        borderRadius: '999px',
                    }"
                >
                    {{ category }}
                </span>
                <span
                    v-if="readTime"
                    :style="{
                        display: 'flex',
                        fontSize: '16px',
                        color: '#cbd5e1',
                    }"
                >
                    {{ readTime }} min de lecture
                </span>
            </div>

            <div
                :style="{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '18px',
                }"
            >
                <h1
                    :style="{
                        fontSize: title.length > 60 ? '44px' : '54px',
                        fontWeight: 700,
                        lineHeight: 1.15,
                        letterSpacing: '-0.025em',
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

            <div :style="{ display: 'flex', alignItems: 'center', gap: '14px' }">
                <div
                    :style="{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '48px',
                        height: '48px',
                        borderRadius: '999px',
                        background: 'linear-gradient(135deg, #a78bfa, #6366f1)',
                        fontSize: '20px',
                        fontWeight: 700,
                    }"
                >
                    JA
                </div>
                <div :style="{ display: 'flex', flexDirection: 'column' }">
                    <span :style="{ fontSize: '17px', fontWeight: 700 }">Juba Ait-Adda</span>
                    <span :style="{ fontSize: '14px', color: '#94a3b8' }">juba-aitadda.dev · blog</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    withDefaults(
        defineProps<{
            title: string;
            description?: string;
            image?: string;
            category?: string;
            readTime?: number;
        }>(),
        {
            description: '',
            image: '',
            category: '',
            readTime: 0,
        },
    );
</script>

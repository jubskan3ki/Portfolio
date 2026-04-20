<template>
    <div
        :style="{
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            padding: '60px',
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
            fontFamily: 'Lato, sans-serif',
            color: '#ffffff',
        }"
    >
        <div
            v-if="category"
            :style="{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
            }"
        >
            <span
                :style="{
                    fontSize: '18px',
                    fontWeight: 600,
                    color: '#a78bfa',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                }"
            >
                {{ category }}
            </span>
            <span v-if="readTime" :style="{ fontSize: '16px', color: '#94a3b8' }">
                {{ readTime }} min de lecture
            </span>
        </div>

        <div
            :style="{
                display: 'flex',
                flexDirection: 'column',
                gap: '16px',
                flex: 1,
                justifyContent: 'center',
            }"
        >
            <h1
                :style="{
                    fontSize: title.length > 60 ? '42px' : '52px',
                    fontWeight: 700,
                    lineHeight: 1.2,
                    letterSpacing: '-0.02em',
                    margin: 0,
                    maxWidth: '900px',
                }"
            >
                {{ title }}
            </h1>
            <p
                v-if="description"
                :style="{
                    fontSize: '20px',
                    color: '#94a3b8',
                    lineHeight: 1.5,
                    margin: 0,
                    maxWidth: '800px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
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
            <div :style="{ display: 'flex', alignItems: 'center', gap: '12px' }">
                <div
                    :style="{
                        width: '44px',
                        height: '44px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #a78bfa, #6366f1)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '20px',
                        fontWeight: 700,
                    }"
                >
                    JA
                </div>
                <div :style="{ display: 'flex', flexDirection: 'column' }">
                    <span :style="{ fontSize: '16px', fontWeight: 600 }">Juba Ait-Adda</span>
                    <span :style="{ fontSize: '14px', color: '#94a3b8' }">juba-aitadda.dev</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    withDefaults(defineProps<{
        title: string;
        description?: string;
        category?: string;
        readTime?: number;
    }>(), {
        description: '',
        category: '',
        readTime: 0,
    });
</script>

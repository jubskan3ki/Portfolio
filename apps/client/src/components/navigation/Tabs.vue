<template>
	<div :class="['tabs', `tabs--${variant}`, { 'tabs--vertical': vertical }, customClass]">
		<!-- Navigation - utilise TabsItem en mode onglet -->
		<div
			ref="navRef"
			:class="[
				'tabs__nav',
				`tabs__nav--${align}`,
				{ 'tabs__nav--scrollable': scrollable },
				{ 'tabs__nav--full-width': fullWidth },
			]"
		>
			<TabsItem
				v-for="tab in tabs"
				:id="tab.id"
				:key="`tab-${tab.id}`"
				:tabs-id="tabsId"
				:is-active="activeTab === tab.id"
				:is-tab="true"
				:label="tab.label"
				:icon="tab.icon"
				:disabled="tab.disabled"
				:badge="tab.badge"
				@select="setActiveTab(tab.id)"
			/>

			<!-- Indicateur -->
			<div v-if="!vertical && showIndicator" class="tabs__indicator" :style="indicatorStyle"></div>
		</div>

		<!-- Contenus - utilise TabsItem en mode panneau -->
		<div class="tabs__panels">
			<TabsItem
				v-for="(tab, index) in tabs"
				:id="tab.id"
				:key="`panel-${tab.id}`"
				:tabs-id="tabsId"
				:is-active="activeTab === tab.id"
			>
				<slot :name="`tab-${index}`">
					<div v-if="tab.content" v-html="tab.content"></div>
				</slot>
			</TabsItem>
		</div>
	</div>
</template>

<script setup lang="ts">
	import TabsItem from '@/components/navigation/TabsItem.vue';
	import { computed, nextTick, onMounted, ref, watch } from 'vue';

	interface TabItem {
		id: string;
		label: string;
		icon?: string;
		content?: string;
		disabled?: boolean;
		badge?: {
			text: string | number;
			type?: string;
			variant?: string;
		};
	}

	const props = defineProps({
		modelValue: {
			type: [String, Number],
			default: '',
		},
		tabs: {
			type: Array as () => Array<TabItem>,
			default: () => [],
		},
		variant: {
			type: String,
			default: 'default',
			validator: (value: string) => ['default', 'outline', 'pills', 'underlined'].includes(value),
		},
		vertical: {
			type: Boolean,
			default: false,
		},
		align: {
			type: String,
			default: 'left',
			validator: (value: string) => ['left', 'center', 'right'].includes(value),
		},
		scrollable: {
			type: Boolean,
			default: false,
		},
		fullWidth: {
			type: Boolean,
			default: false,
		},
		showIndicator: {
			type: Boolean,
			default: true,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['update:modelValue', 'tab-change']);

	// Générer un ID unique pour ce composant tabs
	const tabsId = computed(() => {
		if (props.tabs.length > 0) {
			return props.tabs.map((tab) => tab.id).join('-');
		}
		return 'default-tabs';
	});

	// Trouver l'onglet actif par défaut
	const getDefaultActiveTab = () => {
		if (props.tabs.length === 0) return '';

		const firstEnabledTab = props.tabs.find((tab) => !tab.disabled);
		return firstEnabledTab ? firstEnabledTab.id : props.tabs[0].id;
	};

	// État local de l'onglet actif
	const activeTab = ref(props.modelValue || getDefaultActiveTab());

	// Navigation DOM et style de l'indicateur
	const navRef = ref<HTMLElement | null>(null);
	const indicatorStyle = ref({ width: '0px', transform: 'translateX(0px)' });

	// Gérer le changement d'onglet
	const setActiveTab = (id: string | number) => {
		const tab = props.tabs.find((tab) => tab.id === id);
		if (tab?.disabled) return;

		activeTab.value = id;
		emit('update:modelValue', id);
		emit('tab-change', id);
		updateIndicator();
	};

	// Mettre à jour la position de l'indicateur
	const updateIndicator = async () => {
		if (props.vertical || !props.showIndicator || !navRef.value) return;

		await nextTick();
		const tabs = navRef.value.querySelectorAll('.tabs-item__tab');
		const activeIndex = props.tabs.findIndex((tab) => tab.id === activeTab.value);

		if (activeIndex === -1) return;

		const activeTabElement = tabs[activeIndex] as HTMLElement;
		if (activeTabElement) {
			indicatorStyle.value = {
				width: `${activeTabElement.offsetWidth}px`,
				transform: `translateX(${activeTabElement.offsetLeft}px)`,
			};
		}
	};

	// Observer les changements de modelValue
	watch(
		() => props.modelValue,
		(newValue) => {
			if (newValue !== activeTab.value) {
				activeTab.value = newValue;
				updateIndicator();
			}
		}
	);

	// Observer les changements dans les onglets
	watch(
		() => props.tabs,
		async () => {
			await nextTick();
			updateIndicator();
		},
		{ deep: true }
	);

	// Initialisation
	onMounted(async () => {
		await nextTick();
		updateIndicator();
		window.addEventListener('resize', updateIndicator);
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;
	@use '@/styles/abstracts/functions' as func;

	.tabs {
		display: flex;
		flex-direction: column;
		width: 100%;

		// Variante verticale
		&--vertical {
			flex-direction: row;

			.tabs__nav {
				flex-direction: column;
				width: 200px;
				flex-shrink: 0;
				border-right: 1px solid vars.$gray-light;
			}

			.tabs__panels {
				flex: 1;
				padding-left: vars.$spacing-md;
			}
		}

		// Navigation
		&__nav {
			position: relative;
			display: flex;
			border-bottom: 1px solid vars.$gray-light;

			// Alignement
			&--center {
				justify-content: center;
			}

			&--right {
				justify-content: flex-end;
			}

			// Défilement pour beaucoup d'onglets
			&--scrollable {
				overflow-x: auto;
				scroll-behavior: smooth;
				-webkit-overflow-scrolling: touch;

				// Masquer la barre de défilement
				&::-webkit-scrollbar {
					display: none;
				}
				scrollbar-width: none;
			}

			// Onglets en pleine largeur
			&--full-width {
				:deep() .tabs-item__tab {
					flex: 1;
				}
			}
		}

		// Indicateur pour l'onglet actif
		&__indicator {
			position: absolute;
			bottom: 0;
			height: 2px;
			background-color: vars.$primary-color;
			transition:
				transform vars.$transition-base,
				width vars.$transition-base;
		}

		// Conteneur des panels
		&__panels {
			flex: 1;
			position: relative;
		}
	}

	// Variantes - écrites séparément pour éviter les problèmes de nesting avec :deep
	.tabs--vertical :deep() .tabs-item__tab {
		text-align: left;
		width: 100%;
		border-bottom: none;
	}

	.tabs--outline {
		.tabs__nav {
			border-bottom: none;
		}
	}

	.tabs--outline :deep() .tabs-item__tab {
		border: 1px solid vars.$gray-light;
		border-radius: vars.$border-radius-md;
		margin-right: vars.$spacing-xs;
		margin-bottom: vars.$spacing-xs;
	}

	.tabs--outline :deep() .tabs-item__tab--active {
		border-color: vars.$primary-color;
		color: vars.$primary-color;
	}

	.tabs--pills .tabs__nav {
		border-bottom: none;
		gap: vars.$spacing-xs;
	}

	.tabs--pills :deep() .tabs-item__tab {
		border-radius: vars.$border-radius-full;
	}

	.tabs--pills :deep() .tabs-item__tab--active {
		background-color: vars.$primary-color;
		color: vars.$white;
	}

	.tabs--underlined .tabs__indicator {
		height: 3px;
	}

	.tabs--underlined :deep() .tabs-item__tab--active {
		font-weight: 600;
	}
</style>

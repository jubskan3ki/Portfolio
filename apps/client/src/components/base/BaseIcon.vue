<template>
	<span
		:class="['icon', customClass]"
		:style="{
			width: `${size}px`,
			height: `${size}px`,
			color,
		}"
		role="img"
		:aria-label="name"
	>
		<font-awesome-icon
			:icon="resolveIcon"
			:size="resolveSize"
			:style="{ color }"
			:fixed-width="fixedWidth"
			:flip="resolveFlip"
			:rotation="resolveRotation"
			:spin="spin"
			:pulse="pulse"
		/>
	</span>
</template>

<script setup lang="ts">
	import { library } from '@fortawesome/fontawesome-svg-core';
	import { faGithub, faInstagram, faLinkedin, faTwitter } from '@fortawesome/free-brands-svg-icons';
	import {
		faArrowRight,
		faAward,
		faBookOpen,
		faBriefcase,
		faCalendar,
		faCheck,
		faChevronDown,
		faChevronLeft,
		faChevronRight,
		faChevronUp,
		faCircleCheck,
		faCircleInfo,
		faCircleXmark,
		faClock,
		faCloud,
		faCode,
		faEnvelope,
		faExternalLinkAlt,
		faEye,
		faFolder,
		faHashtag,
		faHeart,
		faHome,
		faLaptopCode,
		faLayerGroup,
		faList,
		faMapPin,
		faMobilePhone,
		faNewspaper,
		faPalette,
		faPhone,
		faQuestion,
		faServer,
		faStar,
		faTableCells,
		faTriangleExclamation,
		faWindowMaximize,
		faWindowRestore,
		faXmark,
	} from '@fortawesome/free-solid-svg-icons';
	import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
	import { computed } from 'vue';

	type IconSize =
		| 'xs'
		| 'sm'
		| 'lg'
		| '2x'
		| '3x'
		| '4x'
		| '5x'
		| '6x'
		| '2xs'
		| 'xl'
		| '2xl'
		| '1x'
		| '7x'
		| '8x'
		| '9x'
		| '10x'
		| undefined;
	type FlipType = 'horizontal' | 'vertical' | 'both' | undefined;
	type RotationType = 90 | 180 | 270 | '90' | '180' | '270' | undefined;

	const props = defineProps({
		name: {
			type: String,
			required: true,
		},
		size: {
			type: [Number, String],
			default: 24,
		},
		color: {
			type: String,
			default: 'currentColor',
		},
		fixedWidth: {
			type: Boolean,
			default: true,
		},
		flip: {
			type: [Boolean, String],
			default: false,
		},
		rotation: {
			type: [Number, String],
			default: null,
		},
		spin: {
			type: Boolean,
			default: false,
		},
		pulse: {
			type: Boolean,
			default: false,
		},
		customClass: {
			type: String,
			default: '',
		},
	});

	// Ajouter les icônes à la bibliothèque
	library.add(
		faChevronDown,
		faChevronUp,
		faChevronRight,
		faChevronLeft,
		faArrowRight,
		faCheck,
		faXmark,
		faHeart,
		faStar,
		faTriangleExclamation,
		faCircleInfo,
		faCircleXmark,
		faCircleCheck,
		faEnvelope,
		faPhone,
		faMapPin,
		faQuestion,
		faHome,
		faFolder,
		faLaptopCode,
		faBriefcase,
		faLayerGroup,
		faNewspaper,
		faCalendar,
		faExternalLinkAlt,
		faPalette,
		faTableCells,
		faLayerGroup,
		faBookOpen,
		faCode,
		faWindowRestore,
		faClock,
		faAward,
		faWindowMaximize,
		faServer,
		faCloud,
		faGithub,
		faTwitter,
		faLinkedin,
		faInstagram,
		faEye,
		faList,
		faHashtag,
		faMobilePhone
	);

	// Mapping des noms conviviaux aux icônes FontAwesome
	const ICON_MAP: Record<string, [string, string]> = {
		'chevron-down': ['fas', 'chevron-down'],
		'chevron-up': ['fas', 'chevron-up'],
		'chevron-right': ['fas', 'chevron-right'],
		'chevron-left': ['fas', 'chevron-left'],
		'arrow-right': ['fas', 'arrow-right'],
		check: ['fas', 'check'],
		close: ['fas', 'xmark'],
		heart: ['fas', 'heart'],
		star: ['fas', 'star'],
		warning: ['fas', 'triangle-exclamation'],
		info: ['fas', 'circle-info'],
		error: ['fas', 'circle-xmark'],
		success: ['fas', 'circle-check'],
		mail: ['fas', 'envelope'],
		phone: ['fas', 'phone'],
		'map-pin': ['fas', 'map-pin'],
		linkedin: ['fab', 'linkedin'],
		twitter: ['fab', 'twitter'],
		github: ['fab', 'github'],
		instagram: ['fab', 'instagram'],
		home: ['fas', 'home'],
		projects: ['fas', 'laptop-code'],
		experience: ['fas', 'briefcase'],
		stacks: ['fas', 'layer-group'],
		blog: ['fas', 'newspaper'],
		folder: ['fas', 'folder'],
		calendar: ['fas', 'calendar'],
		'external-link': ['fas', 'external-link-alt'],
		palette: ['fas', 'palette'],
		grid: ['fas', 'table-cells'],
		layers: ['fas', 'layer-group'],
		'book-open': ['fas', 'book-open'],
		code: ['fas', 'code'],
		'code-square': ['fas', 'window-restore'],
		clock: ['fas', 'clock'],
		award: ['fas', 'award'],
		layout: ['fas', 'window-maximize'],
		server: ['fas', 'server'],
		cloud: ['fas', 'cloud'],
		eye: ['fas', 'eye'],
		list: ['fas', 'list'],
		'x-circle': ['fas', 'circle-xmark'],
		hash: ['fas', 'hashtag'],
		smartphone: ['fas', 'mobile-phone'],
	};

	// Résoudre l'icône
	const resolveIcon = computed(() => {
		if (props.name in ICON_MAP) {
			return ICON_MAP[props.name];
		}

		console.warn(`Icon name "${props.name}" not found in icon map.`);
		return ['fas', 'question'] as [string, string];
	});

	// Résoudre la taille
	const resolveSize = computed((): IconSize => {
		const sizeNum = Number(props.size);

		if (isNaN(sizeNum)) {
			// Si la taille n'est pas un nombre, vérifier si elle correspond à une taille valide
			const validSizes: IconSize[] = [
				'xs',
				'sm',
				'lg',
				'2x',
				'3x',
				'4x',
				'5x',
				'6x',
				'2xs',
				'xl',
				'2xl',
				'1x',
				'7x',
				'8x',
				'9x',
				'10x',
			];
			return validSizes.includes(props.size as IconSize) ? (props.size as IconSize) : 'lg';
		}

		// Convertir la taille en pixels en valeur FontAwesome
		if (sizeNum <= 12) return 'xs';
		if (sizeNum <= 16) return 'sm';
		if (sizeNum <= 24) return 'lg';
		if (sizeNum <= 36) return '2x';
		if (sizeNum <= 48) return '3x';
		if (sizeNum <= 64) return '4x';
		if (sizeNum <= 96) return '5x';
		return '6x';
	});

	// Résoudre le flip
	const resolveFlip = computed((): FlipType => {
		if (typeof props.flip === 'boolean') {
			return props.flip ? 'horizontal' : undefined;
		}

		if (props.flip === 'horizontal' || props.flip === 'vertical' || props.flip === 'both') {
			return props.flip;
		}

		return undefined;
	});

	// Résoudre la rotation
	const resolveRotation = computed((): RotationType => {
		if (props.rotation === null) {
			return undefined;
		}

		const validRotations: RotationType[] = [90, 180, 270, '90', '180', '270'];
		return validRotations.includes(props.rotation as RotationType) ? (props.rotation as RotationType) : undefined;
	});
</script>

<style lang="scss" scoped>
	@use '@/styles/abstracts/variables' as vars;
	@use '@/styles/abstracts/mixins' as mix;

	.icon {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		line-height: 1;
		vertical-align: middle;
	}
</style>

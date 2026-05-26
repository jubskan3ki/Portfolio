import type {
    BlogFilters,
    ExperienceListFilters,
    ProjectListFilters,
    StackListFilters,
} from '@/types/composables/data';
import type { FilterPresetConfig } from '@/types/config/filterPresets';

function createPreset<T extends Record<string, unknown>>(
    defaults: T,
    pagination: FilterPresetConfig = { enabled: false },
) {
    const fieldConfig = Object.fromEntries(
        Object.keys(defaults).map((key) => [key, { resetOnChange: key !== 'ordering', debounced: key === 'search' }]),
    ) as Record<keyof T, { resetOnChange: boolean; debounced: boolean }>;

    return { defaults, fieldConfig, pagination };
}

export const filterPresets = {
    blog: createPreset<BlogFilters>(
        { category: '', tags: [], search: '', ordering: '-date' },
        { enabled: true, itemsPerPage: 6 },
    ),

    projects: createPreset<ProjectListFilters>({
        category: '',
        status: '',
        technologies: [],
        search: '',
        ordering: '-date',
    }),

    stacks: createPreset<StackListFilters>({
        category: '',
        search: '',
        ordering: '-level',
    }),

    experiences: createPreset<ExperienceListFilters>({
        type: '',
        search: '',
        ordering: '-start_date',
    }),
};

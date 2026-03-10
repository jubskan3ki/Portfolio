import type {
    AdminArticle,
    AdminExperience,
    AdminMessage,
    AdminProject,
    AdminStack,
    DataItem,
} from '@/types/feature/admin';

/** Type assertion — not a runtime guard. Use only when the DataItem origin is known. */
export function asAdminArticle(item: DataItem): AdminArticle {
    return item as AdminArticle;
}

export function asAdminProject(item: DataItem): AdminProject {
    return item as AdminProject;
}

export function asAdminStack(item: DataItem): AdminStack {
    return item as AdminStack;
}

export function asAdminExperience(item: DataItem): AdminExperience {
    return item as AdminExperience;
}

export function asAdminMessage(item: DataItem): AdminMessage {
    return item as AdminMessage;
}

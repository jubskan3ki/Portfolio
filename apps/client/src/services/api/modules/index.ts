import { articleKeys } from './articles';
import { authKeys } from './auth';
import { contactKeys } from './contact';
import { experienceKeys } from './experiences';
import { projectKeys } from './projects';
import { stackKeys } from './stacks';
import { statsKeys } from './stats';
import { transferKeys } from './transfer';

export const queryKeys = {
    articles: articleKeys,
    projects: projectKeys,
    stacks: stackKeys,
    experiences: experienceKeys,
    contact: contactKeys,
    auth: authKeys,
    stats: statsKeys,
    transfer: transferKeys,
} as const;

// Messages d'erreur centralisés pour l'application

export const ERROR_MESSAGES = {
    // Opérations génériques
    LOAD_FAILED: (entity: string) => `Impossible de charger ${entity}`,
    CREATE_FAILED: (entity: string) => `Erreur lors de la création de ${entity}`,
    UPDATE_FAILED: (entity: string) => `Erreur lors de la mise à jour de ${entity}`,
    DELETE_FAILED: (entity: string) => `Erreur lors de la suppression de ${entity}`,

    // Erreurs spécifiques
    NOT_FOUND: (entity: string) => `${entity} introuvable`,
    AUTH_EXPIRED: 'Votre session a expiré. Veuillez vous reconnecter.',
    FORBIDDEN: 'Vous n\'avez pas les permissions nécessaires.',
    NETWORK_ERROR: 'Impossible de contacter le serveur. Vérifiez votre connexion.',
    SERVER_ERROR: 'Une erreur inattendue s\'est produite. Veuillez réessayer.',

    // Validation
    FIELD_REQUIRED: 'Ce champ est requis',
    FIELD_INVALID: 'Format invalide',
    FILE_TOO_LARGE: (maxSize: number) => `Le fichier dépasse la taille maximale de ${maxSize}MB`,
    FILE_TYPE_INVALID: 'Type de fichier non accepté',

    // Entités spécifiques
    ARTICLE: {
        NOT_FOUND: 'Article introuvable',
        LOAD_FAILED: 'Impossible de charger l\'article',
        CREATE_FAILED: 'Erreur lors de la création de l\'article',
        UPDATE_FAILED: 'Erreur lors de la mise à jour de l\'article',
        DELETE_FAILED: 'Erreur lors de la suppression de l\'article',
    },
    PROJECT: {
        NOT_FOUND: 'Projet introuvable',
        LOAD_FAILED: 'Impossible de charger le projet',
        CREATE_FAILED: 'Erreur lors de la création du projet',
        UPDATE_FAILED: 'Erreur lors de la mise à jour du projet',
        DELETE_FAILED: 'Erreur lors de la suppression du projet',
    },
    STACK: {
        NOT_FOUND: 'Stack introuvable',
        LOAD_FAILED: 'Impossible de charger la stack',
        CREATE_FAILED: 'Erreur lors de la création de la stack',
        UPDATE_FAILED: 'Erreur lors de la mise à jour de la stack',
        DELETE_FAILED: 'Erreur lors de la suppression de la stack',
    },
    EXPERIENCE: {
        NOT_FOUND: 'Expérience introuvable',
        LOAD_FAILED: 'Impossible de charger l\'expérience',
        CREATE_FAILED: 'Erreur lors de la création de l\'expérience',
        UPDATE_FAILED: 'Erreur lors de la mise à jour de l\'expérience',
        DELETE_FAILED: 'Erreur lors de la suppression de l\'expérience',
    },
    CATEGORY: {
        CREATE_FAILED: 'Erreur lors de la création de la catégorie',
    },
    TAG: {
        CREATE_FAILED: 'Erreur lors de la création du tag',
    },
    TYPE: {
        CREATE_FAILED: 'Erreur lors de la création du type',
    },
} as const;

export const SUCCESS_MESSAGES = {
    // Opérations génériques
    CREATED: (entity: string) => `${entity} créé(e) avec succès`,
    UPDATED: (entity: string) => `${entity} mis(e) à jour avec succès`,
    DELETED: (entity: string) => `${entity} supprimé(e) avec succès`,

    // Entités spécifiques
    ARTICLE: {
        CREATED: 'Article créé avec succès',
        UPDATED: 'Article mis à jour avec succès',
        DELETED: 'Article supprimé avec succès',
    },
    PROJECT: {
        CREATED: 'Projet créé avec succès',
        UPDATED: 'Projet mis à jour avec succès',
        DELETED: 'Projet supprimé avec succès',
    },
    STACK: {
        CREATED: 'Stack créée avec succès',
        UPDATED: 'Stack mise à jour avec succès',
        DELETED: 'Stack supprimée avec succès',
    },
    EXPERIENCE: {
        CREATED: 'Expérience créée avec succès',
        UPDATED: 'Expérience mise à jour avec succès',
        DELETED: 'Expérience supprimée avec succès',
    },
    CATEGORY: {
        CREATED: 'Catégorie créée avec succès',
    },
    TAG: {
        CREATED: 'Tag créé avec succès',
    },
    TYPE: {
        CREATED: 'Type créé avec succès',
    },
} as const;

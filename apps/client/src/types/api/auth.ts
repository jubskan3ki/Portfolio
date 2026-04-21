export interface LoginCredentials {
    email: string;
    password: string;
    rememberMe?: boolean;
}

export interface UserProfile {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
    phoneNumber?: string;
    isActive: boolean;
    bio?: string;
    avatar?: string;
    position?: string;
    publicEmail?: string;
    linkedin?: string;
    github?: string;
    dateJoined?: string;
    updatedAt?: string;
}

export interface LoginResponse {
    user: UserProfile;
}

export interface UpdateProfileData {
    firstName?: string;
    lastName?: string;
    email?: string;
    phoneNumber?: string;
    bio?: string;
    avatar?: string;
    position?: string;
    publicEmail?: string;
    linkedin?: string;
    github?: string;
}

export interface ChangePasswordData {
    old_password: string;
    new_password: string;
}

export interface RequestResetPasswordData {
    email: string;
}

export interface VerifyResetCodeData {
    email: string;
    code: string;
}

export interface ConfirmResetPasswordData {
    email: string;
    code: string;
    newPassword: string;
}

export interface AuthMessageResponse {
    detail: string;
}

export interface VerifyCodeResponse {
    valid: boolean;
}

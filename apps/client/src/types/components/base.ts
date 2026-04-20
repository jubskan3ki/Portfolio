// Types for Base components

// Common types
export type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '';

export type ColorVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';

export type LinkTarget = '_blank' | '_self' | '_parent' | '_top';

export interface RouteObject {
    path: string;
    name?: string;
}

// BaseButton
export type ButtonType = 'button' | 'submit' | 'reset';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost';

export type ButtonSize = Size | 'icon';

export interface ButtonProps {
    text?: string;
    type?: ButtonType;
    variant?: ButtonVariant;
    size?: ButtonSize;
    disabled?: boolean;
    loading?: boolean;
    fullWidth?: boolean;
    customClass?: string;
    to?: string | RouteObject;
    params?: Record<string, string | number>;
    target?: LinkTarget;
    ariaLabel?: string;
}

// BaseInput
export type InputType
    = | 'text'
        | 'password'
        | 'email'
        | 'number'
        | 'tel'
        | 'url'
        | 'search'
        | 'date'
        | 'time'
        | 'datetime-local'
        | 'month'
        | 'week'
        | 'color';

export interface InputProps {
    id?: string;
    name?: string;
    label?: string;
    type?: InputType;
    placeholder?: string;
    required?: boolean;
    disabled?: boolean;
    readonly?: boolean;
    min?: string | number;
    max?: string | number;
    maxlength?: string | number;
    autocomplete?: string;
    clearable?: boolean;
    error?: string;
    success?: string;
    hint?: string;
    customClass?: string;
}

// BaseSelect
export interface SelectOption {
    value: string | number;
    label: string;
    image?: string;
    disabled?: boolean;
}

export type SelectInitialValue
    = | string
        | number
        | { id?: string | number; name?: string; slug?: string }
        | null
        | undefined;

export interface SelectProps {
    options?: SelectOption[];
    id?: string;
    label?: string;
    ariaLabel?: string;
    ariaLabelledby?: string;
    placeholder?: string;
    required?: boolean;
    disabled?: boolean;
    error?: string;
    success?: string;
    hint?: string;
    showImage?: boolean;
    allowCreate?: boolean;
    createLabel?: string;
    createPlaceholder?: string;
    /**
     * Raw value coming from the server (id, name, slug or related object).
     * When options arrive after the form has hydrated, the matching option
     * value is patched into v-model. Ignored once v-model holds a value.
     */
    initialValue?: SelectInitialValue;
}

// BaseMultiSelect
export interface MultiSelectOption {
    value: string | number;
    label: string;
    image?: string;
    [key: string]: unknown;
}

export type MultiSelectInitialItem
    = | string
        | number
        | { id?: string | number; name?: string; slug?: string };

export interface MultiSelectProps {
    options?: MultiSelectOption[];
    id?: string;
    label?: string;
    ariaLabel?: string;
    ariaLabelledby?: string;
    placeholder?: string;
    required?: boolean;
    disabled?: boolean;
    error?: string;
    hint?: string;
    valueKey?: string;
    labelKey?: string;
    imageKey?: string;
    showImages?: boolean;
    allowCreate?: boolean;
    createLabel?: string;
    createPlaceholder?: string;
    maxItems?: number;
    /**
     * Raw values coming from the server (ids, names, slugs or related objects).
     * Resolved against `options` once they arrive and patched into v-model.
     * Ignored when v-model already holds at least one value.
     */
    initialValue?: MultiSelectInitialItem[] | null;
}

// BaseCheckbox
export interface CheckboxProps {
    id?: string;
    name?: string;
    value?: string | number | boolean | object;
    label?: string;
    disabled?: boolean;
    error?: string;
    customClass?: string;
}

// Single Radio Item
export interface RadioItemProps {
    modelValue?: string | number | boolean | object;
    value: string | number | boolean | object;
    id?: string;
    name?: string;
    label?: string;
    disabled?: boolean;
    error?: string;
    customClass?: string;
}

// BaseLink
export type LinkVariant = 'primary' | 'secondary' | 'subtle' | 'white';

export interface LinkProps {
    to: string | RouteObject;
    params?: Record<string, string | number>;
    text?: string;
    variant?: LinkVariant;
    target?: LinkTarget;
    block?: boolean;
    underline?: boolean;
    ariaLabel?: string;
    customClass?: string;
}

// BaseIcon
export type IconSize = Size | number | string;

export interface IconProps {
    name: string;
    size?: IconSize;
    color?: string;
    strokeWidth?: number;
    customClass?: string;
    ariaLabel?: string;
}

// BaseImage
export type AspectRatio = '1:1' | '4:3' | '16:9' | '21:9' | 'auto';

export type ObjectFit = 'cover' | 'contain' | 'fill' | 'none' | 'scale-down';

export type ImageFormat = 'webp' | 'avif' | 'jpeg' | 'png' | 'gif';

export type RoundedSize = 'sm' | 'md' | 'lg' | 'full';

export interface ImageProps {
    src: string;
    alt: string;
    width?: number | string;
    height?: number | string;
    lazy?: boolean;
    placeholder?: string | boolean;
    quality?: number;
    format?: ImageFormat;
    sizes?: string;
    densities?: string;
    preload?: boolean;
    showPlaceholder?: boolean;
    aspectRatio?: AspectRatio;
    objectFit?: ObjectFit;
    rounded?: boolean | RoundedSize;
}

// BaseForm & BaseFormField
export interface FormFieldProps {
    id?: string;
    label?: string;
    required?: boolean;
    error?: string;
    hint?: string;
    customClass?: string;
}

export interface FormProps {
    id?: string;
    customClass?: string;
    fields?: FormFieldProps[];
}

// BaseBadge
export type BadgeVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'outline';

export type BadgeSize = 'sm' | 'md' | 'lg';

export interface BadgeProps {
    text?: string;
    variant?: BadgeVariant;
    size?: BadgeSize;
    rounded?: boolean;
    removable?: boolean;
    dot?: boolean;
    clickable?: boolean;
    icon?: string;
    iconSize?: number | string;
    customClass?: string;
}

// BaseCard
type CardVariant = 'default' | 'elevated' | 'outlined' | 'glass';

type CardPadding = 'none' | 'sm' | 'md' | 'lg';

export interface CardProps {
    title?: string;
    subtitle?: string;
    variant?: CardVariant;
    padding?: CardPadding;
    hoverable?: boolean;
    clickable?: boolean;
    accentColor?: string;
    fullHeight?: boolean;
    customClass?: string;
}

// BaseAvatar
export type AvatarSize = Size;

export type AvatarShape = 'circle' | 'square';

export type AvatarStatus = 'online' | 'offline' | 'busy' | 'away';

export interface AvatarProps {
    src?: string;
    alt?: string;
    name?: string;
    size?: AvatarSize;
    shape?: AvatarShape;
    status?: AvatarStatus;
    color?: string;
    border?: boolean;
    customClass?: string;
}

// BaseDivider
export type DividerOrientation = 'horizontal' | 'vertical';

export type DividerVariant = 'solid' | 'dashed' | 'dotted';

export interface DividerProps {
    orientation?: DividerOrientation;
    variant?: DividerVariant;
    spacing?: 'none' | 'sm' | 'md' | 'lg';
    label?: string;
    customClass?: string;
}

// BaseContentCard
export interface BaseContentCardProps {
    to?: string;
    image?: string;
    imageAlt?: string;
    placeholderIcon?: string;
    badge?: string;
    title: string;
    description?: string;
    tags?: string[];
    maxTags?: number;
    /**
     * When set, emits matching `view-transition-name` on the card's image
     * and title so navigations to the detail page morph them into place.
     */
    transitionKey?: string;
}

// BaseTextarea
export interface TextareaProps {
    id?: string;
    name?: string;
    label?: string;
    placeholder?: string;
    required?: boolean;
    disabled?: boolean;
    readonly?: boolean;
    rows?: number;
    maxlength?: string | number;
    autocomplete?: string;
    resizable?: boolean;
    showCount?: boolean;
    error?: string;
    success?: string;
    hint?: string;
    customClass?: string;
}

// BaseFileUpload
export interface FileUploadProps {
    modelValue?: File | null;
    preview?: string;
    id?: string;
    label?: string;
    accept?: string;
    maxSize?: number; // in MB
    required?: boolean;
    disabled?: boolean;
    error?: string;
    placeholderIcon?: string;
    placeholderText?: string;
    hint?: string;
    previewAlt?: string;
    removeLabel?: string;
}

// BaseSwitch
export interface SwitchProps {
    id?: string;
    name?: string;
    label?: string;
    disabled?: boolean;
    customClass?: string;
    error?: string;
}

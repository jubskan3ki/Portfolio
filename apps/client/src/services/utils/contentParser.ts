import type { ContentBlock } from '@/types/feature/blog';

export function decodeHtmlEntities(text: string): string {
    return text
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#0?39;/g, '\'')
        .replace(/&#x27;/g, '\'')
        .replace(/&#(\d+);/g, (_m, code) => String.fromCharCode(Number(code)))
        .replace(/&#x([0-9a-fA-F]+);/g, (_m, hex) => String.fromCharCode(parseInt(hex, 16)));
}

// XSS-safe pour v-html: decode d'abord pour éviter double-encoding
function escapeHtml(text: string): string {
    const decoded = decodeHtmlEntities(text);
    return decoded
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

const SAFE_URL_PROTOCOLS = new Set(['http:', 'https:', 'mailto:', 'tel:']);

// Bloque javascript:, data:, vbscript:...
function isSafeUrl(url: string): boolean {
    try {
        const parsed = new URL(url, 'https://placeholder.invalid');
        return SAFE_URL_PROTOCOLS.has(parsed.protocol);
    } catch {
        return false;
    }
}

// Inline md: **bold**, *italic*, `code`, [text](url safe-protocol)
export function renderInlineMarkdown(text: string): string {
    let html = escapeHtml(text);

    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, text: string, url: string) => {
        if (isSafeUrl(url)) {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`;
        }
        return text;
    });

    return html;
}

export function parseMarkdownToBlocks(content: string): ContentBlock[] {
    const blocks: ContentBlock[] = [];
    const lines = content.replace(/\r\n/g, '\n').split('\n');

    function lineAt(idx: number): string {
        return lines[idx] ?? '';
    }

    function isTableRow(line: string): boolean {
        return /^\|.+\|$/.test(line.trim());
    }

    function isTableSeparator(line: string): boolean {
        return /^\|[\s:]*-{2,}[\s:]*(\|[\s:]*-{2,}[\s:]*)*\|$/.test(line.trim());
    }

    let i = 0;
    while (i < lines.length) {
        const line = lineAt(i);

        if (!line.trim()) {
            i++;
            continue;
        }

        const headingMatch = line.match(/^(#{2,4})\s+(.+)$/);
        if (headingMatch) {
            blocks.push({
                type: 'heading',
                level: (headingMatch[1] as string).length as 2 | 3 | 4,
                content: (headingMatch[2] as string).trim(),
            });
            i++;
            continue;
        }

        if (line.trim().startsWith('```')) {
            const language = line.trim().slice(3).trim() || undefined;
            const codeLines: string[] = [];
            i++;
            while (i < lines.length && !lineAt(i).trim().startsWith('```')) {
                codeLines.push(lineAt(i));
                i++;
            }
            blocks.push({
                type: 'code',
                content: codeLines.join('\n'),
                ...(language ? { language } : {}),
            });
            i++;
            continue;
        }

        if (isTableRow(line) && i + 1 < lines.length && isTableSeparator(lineAt(i + 1))) {
            const parseRow = (row: string) =>
                row
                    .trim()
                    .replace(/^\||\|$/g, '')
                    .split('|')
                    .map((cell) => cell.trim());

            const headers = parseRow(line);
            i += 2;

            const rows: string[][] = [];
            while (i < lines.length && isTableRow(lineAt(i))) {
                rows.push(parseRow(lineAt(i)));
                i++;
            }

            blocks.push({ type: 'table', headers, rows });
            continue;
        }

        // Images: safe protocol only (XSS)
        const imageMatch = line.match(/^!\[([^\]]*)\]\((\S+?)(?:\s+"([^"]*)")?\)$/);
        if (imageMatch) {
            const imageSrc = imageMatch[2] as string;
            if (isSafeUrl(imageSrc)) {
                blocks.push({
                    type: 'image',
                    alt: imageMatch[1] as string,
                    src: imageSrc,
                    ...(imageMatch[3] ? { caption: imageMatch[3] } : {}),
                });
            }
            i++;
            continue;
        }

        if (line.startsWith('> ')) {
            const quoteLines: string[] = [];
            while (i < lines.length && lineAt(i).startsWith('> ')) {
                quoteLines.push(lineAt(i).slice(2));
                i++;
            }
            blocks.push({ type: 'blockquote', content: quoteLines.join('\n') });
            continue;
        }

        if (/^[-*]\s+/.test(line)) {
            const items: string[] = [];
            while (i < lines.length && /^[-*]\s+/.test(lineAt(i))) {
                items.push(lineAt(i).replace(/^[-*]\s+/, ''));
                i++;
            }
            blocks.push({ type: 'list', items, ordered: false });
            continue;
        }

        if (/^\d+\.\s+/.test(line)) {
            const items: string[] = [];
            while (i < lines.length && /^\d+\.\s+/.test(lineAt(i))) {
                items.push(lineAt(i).replace(/^\d+\.\s+/, ''));
                i++;
            }
            blocks.push({ type: 'list', items, ordered: true });
            continue;
        }

        const paragraphLines: string[] = [];
        while (i < lines.length) {
            const cur = lineAt(i);
            if (
                !cur.trim()
                || /^#{2,4}\s/.test(cur)
                || cur.trim().startsWith('```')
                || cur.startsWith('> ')
                || /^[-*]\s+/.test(cur)
                || /^\d+\.\s+/.test(cur)
                || /^!\[/.test(cur)
                || isTableRow(cur)
            ) {
                break;
            }
            paragraphLines.push(cur);
            i++;
        }
        if (paragraphLines.length) {
            blocks.push({ type: 'paragraph', content: paragraphLines.join('\n') });
        }
    }

    return blocks;
}

function hasMarkdownSyntax(text: string): boolean {
    return (
        /^#{2,4}\s/m.test(text)
        || /\n#{2,4}\s/.test(text)
        || /^[-*]\s+/m.test(text)
        || /\n[-*]\s+/.test(text)
        || /^\d+\.\s+/m.test(text)
        || /\n\d+\.\s+/.test(text)
        || /^\|.+\|$/m.test(text)
        || /^>\s/m.test(text)
        || /\n>\s/.test(text)
        || /^```/m.test(text)
        || /\n```/.test(text)
    );
}

// Accepte: string md brut, string JSON, ContentBlock[] (avec md potentiellement imbriqué)
export function normalizeContent(content: unknown): ContentBlock[] {
    if (typeof content === 'string') {
        try {
            const parsed = JSON.parse(content);
            if (Array.isArray(parsed)) {
                return normalizeContent(parsed);
            }
        } catch {
            // pas JSON -> md brut
        }
        return parseMarkdownToBlocks(content);
    }

    if (!Array.isArray(content)) {
        return [];
    }

    const result: ContentBlock[] = [];
    for (const block of content) {
        if (typeof block === 'string') {
            result.push(...parseMarkdownToBlocks(block));
            continue;
        }

        if (
            block
            && typeof block === 'object'
            && (block.type === 'paragraph' || block.type === 'text')
            && typeof block.content === 'string'
        ) {
            const text = block.content as string;
            // Re-parse si md non-traité ou block-level caché
            if (hasMarkdownSyntax(text) || (text.includes('\n') && parseMarkdownToBlocks(text).length > 1)) {
                result.push(...parseMarkdownToBlocks(text));
                continue;
            }
        }

        result.push(block as ContentBlock);
    }

    return result;
}

export function parseJsonContent(content: unknown): string {
    if (typeof content === 'string') {
        return content;
    }

    if (!Array.isArray(content)) {
        return '';
    }

    return content
        .map((block) => {
            if (typeof block === 'string') {
                return block;
            }
            if (typeof block !== 'object' || block === null) {
                return '';
            }

            const b = block as Record<string, unknown>;
            const type = b.type as string;

            switch (type) {
                case 'heading': {
                    const level = (b.level as number) || 2;
                    const prefix = '#'.repeat(level);
                    return `${prefix} ${b.content || ''}`;
                }
                case 'blockquote':
                    return `> ${b.content || ''}`;
                case 'image': {
                    const alt = (b.alt as string) || '';
                    const src = (b.src as string) || '';
                    const caption = b.caption ? ` "${b.caption}"` : '';
                    return `![${alt}](${src}${caption})`;
                }
                case 'code': {
                    const lang = (b.language as string) || '';
                    return `\`\`\`${lang}\n${b.content || ''}\n\`\`\``;
                }
                case 'list': {
                    const items = (b.items as string[]) || [];
                    const ordered = b.ordered as boolean;
                    return items.map((item, i) => (ordered ? `${i + 1}. ${item}` : `- ${item}`)).join('\n');
                }
                case 'table': {
                    const headers = (b.headers as string[]) || [];
                    const rows = (b.rows as string[][]) || [];
                    const headerRow = `| ${headers.join(' | ')} |`;
                    const separatorRow = `| ${headers.map(() => '---').join(' | ')} |`;
                    const dataRows = rows.map((row) => `| ${row.join(' | ')} |`).join('\n');
                    return `${headerRow}\n${separatorRow}\n${dataRows}`;
                }
                case 'text':
                case 'paragraph':
                    return (b.content as string) || '';
                default:
                    return (b.content as string) || '';
            }
        })
        .filter(Boolean)
        .join('\n\n');
}

export function formatContentForApi(content: string): string {
    return JSON.stringify(parseMarkdownToBlocks(content));
}

export default defineNuxtPlugin(() => {
    if (typeof window === 'undefined' || import.meta.env.DEV) {
        return;
    }

    const banner = [
        '    ___      __           ___    _ __     ___     __    __          ',
        '   / _ \\___ / /  ___ _   / _ |  (_) /____/ _ |___/ /___/ /__ _      ',
        '  / , _/ -_) _ \\/ _ `/  / __ | / / __/___/ __ / __/ __/ _ `/      ',
        ' /_/|_|\\__/_.__/\\_,_/  /_/ |_|/_/\\__/   /_/ |_\\__/\\__/\\_,_/       ',
        '',
    ].join('\n');

    const titleStyle = 'color:#a78bfa;font-weight:bold;font-family:monospace;';
    const subStyle = 'color:#64748b;font-family:monospace;';
    const linkStyle = 'color:#6366f1;font-weight:bold;font-family:monospace;';

    console.info('%c%s', titleStyle, banner);
    console.info(
        '%cDévelopeur fullstack · Nuxt 3 + Django · code visible ici: %chttps://github.com/jubskan3ki',
        subStyle,
        linkStyle,
    );
    console.info(
        '%cRecrutement / freelance : %ccontact@aitaddajuba.fr',
        subStyle,
        linkStyle,
    );
});

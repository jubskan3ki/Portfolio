// Tells TypeScript that *.vue imports resolve to a Vue component module. Needed
// for cross-file imports (tests, barrel files like components/.../index.ts) on
// fresh installs where vue-tsc's Volar plugin hasn't yet observed the .vue files.
// vue-tsc still parses the actual SFCs and provides accurate per-component types
// on top of this loose shim.
declare module '*.vue' {
    import type { DefineComponent } from 'vue';
    const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>;
    export default component;
}

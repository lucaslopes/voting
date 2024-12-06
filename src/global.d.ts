// global.d.ts
declare module "./eventBus" {
  export const eventBus: import("mitt").Emitter;
}

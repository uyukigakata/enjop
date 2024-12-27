import type { ComputedRef, MaybeRef } from 'vue'
export type LayoutKey = "default"
declare module "../../node_modules/.pnpm/nuxt@3.14.1592_@parcel+watcher@2.5.0_@types+node@22.10.1_ioredis@5.4.1_magicast@0.3.5_rollup@_4ssef45y2exle6x2zyd5jmalg4/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    layout?: MaybeRef<LayoutKey | false> | ComputedRef<LayoutKey | false>
  }
}
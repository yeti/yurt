declare module '@mui/material/styles' {
  export interface Theme {}

  export interface ThemeOptions {}

  interface PaletteColor {
    blue?: string;
  }

  interface PaletteColorOptions {
    blue?: string;
    main: string;
  }

  interface SimplePaletteColorOptions {
    light?: string;
    main: string;
    dark?: string;
  }

  export interface TypeBackground {}

  interface TypographyVariants {}

  interface TypographyVariantsOptions {}

  interface ZIndex {
    min: number;
    default: number;
  }
}

declare module '@mui/material/Button' {
  export interface ButtonPropsVariantOverrides {}
}

declare module '@mui/material/Typography' {
  export interface TypographyPropsVariantOverrides {}
}

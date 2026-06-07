declare module "@mui/material/styles" {
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
    dark?: string;
    light?: string;
    main: string;
  }

  export interface TypeBackground {}

  interface TypographyVariants {}

  interface TypographyVariantsOptions {}

  interface ZIndex {
    default: number;
    min: number;
  }
}

declare module "@mui/material/Button" {
  export interface ButtonPropsVariantOverrides {}
}

declare module "@mui/material/Typography" {
  export interface TypographyPropsVariantOverrides {}
}

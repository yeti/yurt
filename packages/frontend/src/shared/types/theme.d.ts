import { CSSProperties } from 'react';

declare module '@mui/material/styles' {
  export interface Theme {
    shape: {
      borderRadius: {
        10: CSSProperties['borderRadius'];
        20: CSSProperties['borderRadius'];
        35: CSSProperties['borderRadius'];
        50: CSSProperties['borderRadius'];
        100: CSSProperties['borderRadius'];
        circle: CSSProperties['borderRadius'];
      };
    };
  }

  export interface ThemeOptions {
    shape: {
      borderRadius: {
        10: CSSProperties['borderRadius'];
        20: CSSProperties['borderRadius'];
        35: CSSProperties['borderRadius'];
        50: CSSProperties['borderRadius'];
        100: CSSProperties['borderRadius'];
        circle: CSSProperties['borderRadius'];
      };
    };
  }

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

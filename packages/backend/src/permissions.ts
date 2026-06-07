export interface AuthScopes {
  public: boolean;
}

export function getAuthScopes(): AuthScopes {
  return {
    public: true,
  };
}

export const defaultQueryScopes = {
  public: true,
} as const satisfies Partial<AuthScopes>;

export const defaultMutationScopes = {
  public: true,
} as const satisfies Partial<AuthScopes>;

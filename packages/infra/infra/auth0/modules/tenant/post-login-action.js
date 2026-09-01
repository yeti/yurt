// Stamps profile claims onto the access token so the backend can
// JIT-provision users without a /userinfo round-trip.
// biome-ignore lint/suspicious/useAwait: Auth0 validates the exact async signature
exports.onExecutePostLogin = async (event, api) => {
  // Must match the API identifier (AUTH0_AUDIENCE) — the backend reads
  // claims as `<audience>/email` etc.
  const ns = "__YURT_API_IDENTIFIER__";
  api.accessToken.setCustomClaim(`${ns}/email`, event.user.email);
  api.accessToken.setCustomClaim(`${ns}/name`, event.user.name);
  api.accessToken.setCustomClaim(
    `${ns}/email_verified`,
    event.user.email_verified
  );
};

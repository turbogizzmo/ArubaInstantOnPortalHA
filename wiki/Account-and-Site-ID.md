# Account and Site Selection

Use a dedicated Instant On portal account instead of an owner's everyday
administrator account.

## Recommended account model

The account should:

- Have access only to the site or sites Home Assistant must monitor.
- Use a unique, randomly generated password.
- Not reuse a personal or infrastructure-administrator password.
- Be documented as a service account in your password manager.

The current automated portal authentication flow cannot complete an MFA
challenge. If organizational policy requires MFA for every portal account,
this integration cannot authenticate until that limitation is resolved.

## Select a site

Home Assistant discovers the sites available to the account after validating
the email and password. If the account has access to one unconfigured site,
that site is selected automatically. If it has access to multiple sites, choose
one from the setup form.

## Multiple sites

Add the integration once for each site:

1. Use the same dedicated account if it has intentionally limited access to
   all required sites.
2. Run **Add integration** again and select another discovered site.
3. Home Assistant prevents the same site ID from being configured twice.

For stronger isolation, use a separate portal account per site.

## Security notes

Home Assistant stores the account data in protected config-entry storage.
Do not place portal credentials in dashboard YAML, `secrets.yaml`, issue
reports, screenshots, or this repository.

If credentials may have been exposed, change the password immediately. Removing
the value from a later Git commit does not remove it from earlier history.

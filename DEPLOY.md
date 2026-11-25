# Deploying BlackVault Finance and Research to finance.blackvault.co.ke

This is a plain static site. Upload the contents of this folder to the root of any static host.
It has not been deployed by the author. Nothing is live until you do the steps below.

## Option A: GitHub Pages
1. Create a repository and push these files to the root of the main branch.
2. Settings > Pages > deploy from branch. The CNAME file already contains finance.blackvault.co.ke.
3. At your DNS provider add: a CNAME record for `finance` pointing to <your-user>.github.io.
4. Tick "Enforce HTTPS" once the certificate is issued.

## Option B: Netlify or Cloudflare Pages
Connect the repository, leave build command empty and publish directory as `/`. Add finance.blackvault.co.ke as a custom domain and follow the DNS prompt.

## Checks after going live
- Open the site on phone and desktop and test every menu link.
- Check finance.blackvault.co.ke/robots.txt and /sitemap.xml respond.
- Share the home page to confirm the preview image appears.

## Notes
- The emblem was rebuilt from the supplied PNG. Replace assets/brand/emblem-*.svg and favicon.svg with your original vector file when you have it.
- Only verified contact details are used. Add registration or office details only once confirmed.

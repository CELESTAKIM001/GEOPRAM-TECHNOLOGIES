GEOPRAM TECHNOLOGIES — MAINTENANCE PAGE

Contents: index.html, assets/geopram-maintenance.png, vercel.json.
The email button opens info@geopramtech.co.ke. The website button opens https://geopramtech.co.ke/.

IMPORTANT: This is a standalone static maintenance page. Deploy it as a separate Vercel project/preview first. Do not replace the existing production project or change its domain assignment until you confirm the page and intentionally want the live domain to show maintenance.


ERROR PAGES:
- 404.html: custom not-found page; Vercel automatically serves this for unmatched URLs on a static deployment.
- 403.html, 500.html, 503.html: branded error pages you can visit directly or route to from an application/server.
All these pages reuse assets/geopram-maintenance.png, so the maintenance image and contact links remain visible.
Note: Vercel/static hosting does not automatically use custom 500.html or 503.html for every platform-level failure. The 404 page is the standard automatic static-hosting not-found page.

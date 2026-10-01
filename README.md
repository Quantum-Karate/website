# Quantum Karate

This repository is the static website for Quantum Karate.

## Preview locally

From the repository root:

```bash
python3 -m http.server -d docs 8000
```

Open the site on port 8000.

## Hosting

GitHub Pages, deploy from a branch: branch `main`, folder `/docs`.

Live address: https://quantum-karate.github.io/website/

Pages is switched on by the repository owner after review. Internal links are relative.

## Code owners

`.github/CODEOWNERS` is reserved for a Quantum-Karate org team (add one when ready). Until then, org admins review site changes.

## Custom domain later

1. Add `docs/CNAME` containing the domain.
2. Set DNS: a CNAME record pointing at `quantum-karate.github.io` for a subdomain, or GitHub's A/AAAA records for an apex domain.
3. In Settings > Pages, enter the domain and tick Enforce HTTPS.

## Contact email

The contact address is set in `contact.html`.

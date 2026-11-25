# Registre MCP interne (GitHub Pages)

Registre statique au format MCP Registry v0.1, utilisé par la politique
GitHub Copilot « Restrict MCP access to registry servers ».

## Ajouter ou modifier un serveur

1. Éditer `servers.json` :
   ```json
   {
     "name": "com.esker/mon-serveur",
     "title": "Mon serveur",
     "description": "À quoi il sert",
     "version": "1.0.0",
     "url": "https://mon-serveur.esker.com/mcp"
   }
   ```
   - `name` : format `domaine.inverse/nom`, unique.
   - `transport` (optionnel) : `streamable-http` par défaut, ou `sse`.
2. Lancer `python3 generate.py`.
3. Commiter `servers.json` **et** le dossier `v0.1/`.

## Mise en ligne

- Settings → Pages → Deploy from a branch → `main` / `(root)`.
- Vérifier : `https://<org>.github.io/<repo>/v0.1/servers` affiche le JSON.

## Configuration GitHub (organisation)

Settings → Copilot → Policies → MCP :
- MCP registry URL : `https://<org>.github.io/<repo>` (sans `/v0.1/servers`)
- Restrict MCP access to registry servers : `Registry only`

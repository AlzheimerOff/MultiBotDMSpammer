# Discord Multi-Bot Spam & Reaction

Un script Python performant pour gérer plusieurs bots Discord simultanément, permettant d'automatiser l'envoi de messages (spam) et l'ajout de réactions de manière coordonnée.

## Caractéristiques

- **Multi-Bot** : Gérez une armée de bots à partir d'un seul fichier de configuration.
- **Désynchronisation Intelligente** : Système de délai aléatoire pour éviter les détections et les limitations de débit (Rate Limits).
- **Système de Whitelist** : Protection des utilisateurs spécifiques contre les spams.
- **Restrictions de Salon** : Possibilité de limiter l'utilisation du bot à un salon spécifique.
- **Logs d'Activité** : Suivi détaillé des spams lancés dans un salon dédié avec mentions des cibles.
- **Réactions de Masse** : Commande pour faire réagir tous les bots à un message spécifique.
- **Interface Sobre** : Design minimaliste et professionnel sans fioritures.

## Commandes

### Utilisateurs Autorisés
- `+spam @user/ID message` : Lance une vague de messages privés vers la cible. (Ajoute automatiquement une réaction 😎 sur votre message).
- `+react [emoji]` : Fait réagir tous les bots au message auquel vous répondez.

### Administration (Admins uniquement)
- `+wl @user` : Ajoute un utilisateur à la whitelist.
- `+unwl @user` : Retire un utilisateur de la whitelist.
- `+salon #salon` : Définit le salon où les commandes sont autorisées (laisser vide pour tout autoriser).
- `+logs #salon` : Définit le salon où les logs de spam seront envoyés.

## Installation

1. Installez les dépendances :
   ```bash
   pip install discord.py
   ```
2. Configurez vos tokens dans le fichier `config.json`.
3. Lancez le script :
   ```bash
   python main.py
   ```

## Configuration (config.json)

```json
{
  "tokens": ["TOKEN_1", "TOKEN_2", "..."],
  "settings": {
    "prefix": "+",
    "allowed_channel_id": 0,
    "log_channel_id": 0
  }
}
```

---
*Créé par Alzheimer*

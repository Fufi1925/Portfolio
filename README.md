# Fufi — Portfolio

Eine schnelle, responsive Portfolio-Website für eine kuratierte Auswahl meiner Softwareprojekte.

## Inhalt

- University Bot und Fusch mit verifizierten Live-Links
- Discord Architect, Fufcord, E-Scooter Companion, ModForge, Lyrics Status und VerifyLink
- echte Projektbilder aus den jeweiligen Repositories beziehungsweise Live-Websites
- responsive Glassmorphism-Navigation, Projektfilter und dezente Scroll-Animationen
- eigene Seiten unter `/Preis` und `/Kontakt`
- ungefähre Preisbereiche für Websites, Bots und individuelle Systeme
- Discord als Hauptkontakt, E-Mail und GitHub als Alternativen
- keine Tracker, Cookies, externen Fonts oder clientseitigen Abhängigkeiten
- Security-Header und Railway-Healthcheck

Bewusst nicht enthalten sind leere Repositories, Duplikate, unfertige Experimente, Credential-Tools sowie Exploit-/EH-Skripte.

## Lokal starten

```bash
npm start
```

Danach: <http://localhost:3000>

Für den Syntaxcheck:

```bash
npm run check
```

## Auf Railway deployen

1. Dieses Repository mit Railway verbinden.
2. Railway erkennt Node.js über `package.json`.
3. Der Startbefehl ist bereits in `railway.json` hinterlegt.
4. Unter **Settings → Networking** eine öffentliche Domain erzeugen.

Es werden keine Umgebungsvariablen benötigt. Der Server hört automatisch auf Railways `PORT` und auf `0.0.0.0`.

## Projektstruktur

```text
Portfolio/
├── public/
│   ├── assets/
│   ├── Preis/index.html
│   ├── Kontakt/index.html
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── 404.html
│   └── robots.txt
├── server.js
├── package.json
└── railway.json
```

## Hinweise

- Die Live-Links für University Bot und Fusch wurden beim Erstellen der Website geprüft.
- ModForge und Void Shop hatten gefundene Railway-URLs, lieferten aber zu diesem Zeitpunkt Railway-404-Seiten und wurden deshalb nicht als live markiert.
- Private Projekte zeigen keinen öffentlichen Repository-Link.

## Lizenz

MIT für den Portfolio-Code. Projektbilder und einzelne Projektinhalte bleiben den jeweiligen Projekten zugeordnet.

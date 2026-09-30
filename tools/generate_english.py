#!/usr/bin/env python3
"""Generate static English pages from the German source pages."""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1] / "public"


def translate_text(soup, mapping):
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or node.parent.name in {"script", "style"}:
            continue
        raw = str(node)
        stripped = raw.strip()
        if stripped in mapping:
            node.replace_with(raw.replace(stripped, mapping[stripped]))


def common(soup, title, description, de_url, en_url):
    soup.html["lang"] = "en"
    soup.title.string = title
    desc = soup.find("meta", attrs={"name": "description"})
    if desc: desc["content"] = description
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title: og_title["content"] = title
    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc: og_desc["content"] = description
    for link in soup.select('link[rel="alternate"]'):
        if link.get("hreflang") == "de": link["href"] = de_url
        if link.get("hreflang") == "en": link["href"] = en_url
    nav = soup.select_one(".nav")
    if nav: nav["aria-label"] = "Main navigation"
    brand = soup.select_one(".nav .brand")
    if brand:
        brand["href"] = "/en"
        brand["aria-label"] = "Fufi portfolio home"
    menu_label = soup.select_one(".menu-button .sr-only")
    if menu_label: menu_label.string = "Open menu"
    footer_brand = soup.select_one(".footer .brand")
    if footer_brand: footer_brand["href"] = "/en"
    switch = soup.select_one(".nav .language-switch")
    if switch:
        switch.string = "DE"
        switch["href"] = de_url
        switch["aria-label"] = "German version"
    footer_switch = soup.select_one(".footer .language-switch")
    if footer_switch:
        footer_switch.string = "Deutsch"
        footer_switch["href"] = de_url


def generate_home():
    soup = BeautifulSoup((ROOT / "index.html").read_text(), "html.parser")
    common(soup, "Fufi — Portfolio", "Selected apps, bots and platforms by Fufi — from community systems to mobile tools.", "/", "/en")
    mapping = {
        "Zum Inhalt springen": "Skip to content", "Projekte": "Projects", "Preis": "Pricing", "Kontakt": "Contact",
        "Ausgewählte Arbeit · 2026": "Selected work · 2026", "Ich baue Software,": "I build software,",
        "die wirklich benutzt wird.": "people actually use.",
        "Bots, Dashboards und mobile Apps — von der ersten Idee bis zum laufenden Produkt. Klar gestaltet, technisch durchdacht und mit Fokus auf echte Nutzer.": "Bots, dashboards and mobile apps — from the first idea to a running product. Clearly designed, technically considered and focused on real users.",
        "Projekte ansehen": "View projects", "GitHub-Profil": "GitHub profile", "ausgewählte Projekte": "selected projects",
        "Technologien & Sprachen": "technologies & languages", "verifizierte Live-Produkte": "verified live products",
        "Projekte mit Substanz.": "Projects with substance.",
        "Eine kuratierte Auswahl. Keine leeren Repositories, keine Duplikate — nur Projekte, die eine klare Idee und sichtbare Umsetzung zeigen.": "A curated selection. No empty repositories, no duplicates — only projects with a clear idea and visible execution.",
        "Alle": "All", "Plattformen": "Platforms", "Tools": "Tools", "Live geprüft": "Live verified",
        "Ein komplettes Discord-System mit Bot, FastAPI-Backend, Next.js-Dashboard, Serververwaltung, Sicherheit, Tickets und Automationen.": "A complete Discord system with a bot, FastAPI backend, Next.js dashboard, server management, security, tickets and automation.",
        "Eine Android-App für Standorttests mit Karten, Routen, Favoriten, Verlauf und einem sorgfältig dokumentierten Release- und Signaturprozess.": "An Android utility for location testing with maps, routes, favourites, history and a carefully documented release and signing process.",
        "Eine plattformübergreifende Rich-Presence-App mit Onboarding, Presets, Live-Vorschau und nativen Builds für Android und iOS.": "A cross-platform rich-presence app with onboarding, presets, live preview and native Android and iOS builds.",
        "Eine mobile Musik-Erweiterung im Stil von Spicetify: anpassbare Oberfläche, Lyrics und zusätzliche Komfortfunktionen direkt auf dem Handy.": "A mobile music extension in the spirit of Spicetify: custom themes, lyrics and extra convenience features directly on your phone.",
        "Liest laufende Musik über Windows SMTC, synchronisiert Lyrics zeitgenau und zeigt den aktuellen Abschnitt als Status.": "Reads currently playing music through Windows SMTC, synchronises lyrics precisely and displays the current section as a status.",
        "Erstellt vollständige Discord-Server aus zehn strukturierten Vorlagen — mit Builder, Regelwerk, UI und umfangreicher Testsuite.": "Builds complete Discord servers from ten structured templates — with a builder, rules engine, UI and extensive test suite.",
        "Ein Flutter-Konzept für BLE-Telemetrie, Fahrdaten, Karten und Profile — entwickelt für Forschung, Tests und private Umgebungen.": "A Flutter concept for BLE telemetry, ride data, maps and profiles — developed for research, testing and private environments.",
        "Discord-Moderation mit Web-Dashboard, Rollen, Fällen, Tickets, Persistenz und automatisierten Sicherheitstests.": "Discord moderation with a web dashboard, roles, cases, tickets, persistence and automated security tests.",
        "Verbindet Minecraft und Discord über kurzlebige Codes und eine klar getrennte REST-Schnittstelle — ohne direkten Datenbankzugriff des Bots.": "Connects Minecraft and Discord through short-lived codes and a clearly separated REST API — without direct database access from the bot.",
        "Live Website": "Live website", "Repository": "Repository", "Release": "Release", "Quellcode privat": "Source private",
        "Von der Idee bis live.": "From idea to live.",
        "Mein Fokus liegt nicht nur auf Code. Ich verbinde Produktidee, Oberfläche, Backend und Deployment zu einem funktionierenden Ganzen.": "My focus goes beyond code. I connect product thinking, interface, backend and deployment into one working product.",
        "Backend & APIs": "Backend & APIs", "Product UI": "Product UI", "Mobile": "Mobile", "Deploy & Iterate": "Deploy & iterate",
        "Python, FastAPI, Node.js, Authentifizierung, Datenmodelle und saubere Schnittstellen.": "Python, FastAPI, Node.js, authentication, data models and clean interfaces.",
        "Responsive Dashboards, klare Nutzerflüsse und Oberflächen, die komplexe Systeme einfach machen.": "Responsive dashboards, clear user flows and interfaces that make complex systems feel simple.",
        "Native Android-/iOS-Arbeit und Flutter-Prototypen mit Gerätefunktionen und lokalen Daten.": "Native Android and iOS work plus Flutter prototypes with device features and local data.",
        "Railway, Docker, GitHub Actions, Releases, Tests und dokumentierte Updatepfade.": "Railway, Docker, GitHub Actions, releases, tests and documented update paths.",
        "Über mich": "About me", "Neugierig auf das ganze System — nicht nur auf eine Datei.": "Curious about the whole system — not just one file.",
        "Ich bin Fufi und entwickle Software rund um Communities, Automatisierung und mobile Werkzeuge. Mich interessiert der vollständige Weg: Problem verstehen, Architektur planen, Oberfläche bauen, absichern und veröffentlichen.": "I'm Fufi, and I build software for communities, automation and mobile tools. I care about the full journey: understanding the problem, planning the architecture, building the interface, securing it and shipping it.",
        "Dieses Portfolio zeigt bewusst nur eine saubere Auswahl meiner Arbeit. Experimente, Duplikate und unfertige Repositories bleiben draußen.": "This portfolio intentionally shows only a clean selection of my work. Experiments, duplicates and unfinished repositories stay out.",
        "Auf GitHub ansehen": "View on GitHub", "Nach oben": "Back to top", "Gute Software beginnt": "Good software starts",
        "mit einer klaren Idee.": "with a clear idea.", "Meine Arbeit entdecken": "Explore my work",
        "Software, Systeme & Interfaces.": "Software, systems & interfaces.", "Keine Tracker. Keine Cookies.": "No trackers. No cookies.",
        "Projekte nur für legitime Entwicklung, Tests und Bildung.": "Projects are for legitimate development, testing and education only.",
    }
    translate_text(soup, mapping)
    # Route and navigation adjustments.
    nav = soup.select_one("#nav-links")
    links = nav.find_all("a", recursive=False)
    for a in links:
        text = a.get_text(strip=True)
        if text == "Projects": a["href"] = "#projects"
        elif text == "Skills": a["href"] = "#capabilities"
        elif text == "Pricing": a["href"] = "/en/pricing"
        elif text == "Contact": a["href"] = "/en/contact"
    for a in soup.select('.footer-links a'):
        text = a.get_text(strip=True)
        if text == "Projects": a["href"] = "#projects"
        elif text == "Pricing": a["href"] = "/en/pricing"
        elif text == "Contact": a["href"] = "/en/contact"
    # Accessible image labels.
    alt_map = {
        "Weltraum-Motiv der University-Bot-Website": "Space artwork from the live University Bot website",
        "Weltraum-Hintergrund der live laufenden University-Bot-Website": "Space background from the live University Bot website",
        "Fusch-App mit Karte und ausgewähltem Standort in Duisburg": "Fusch app with a map and selected location in Duisburg",
        "Illustration einer verbundenen Serverarchitektur": "Illustration of a connected server architecture",
        "Illustration einer E-Scooter-App mit Bluetooth-Verbindung": "Illustration of an e-scooter app with Bluetooth connectivity",
        "ModForge-Symbol: grünes Sicherheitsschild": "ModForge icon: green security shield",
        "Illustration synchronisierter Songtexte und einer Audiowelle": "Illustration of synchronised lyrics and an audio waveform",
        "Illustration einer sicheren Verbindung zwischen Spielserver und Community": "Illustration of a secure connection between a game server and a community",
        "Illustration einer mobilen Musik-App mit Lyrics und anpassbarer Oberfläche": "Illustration of a customisable mobile music app with lyrics",
    }
    for img in soup.find_all("img", alt=True):
        if img["alt"] in alt_map: img["alt"] = alt_map[img["alt"]]
    aria_map = {
        "Portfolio in Zahlen": "Portfolio in numbers",
        "University Bot Projektvorschau": "University Bot project preview",
        "University Bot live öffnen": "Open University Bot live",
        "Projekte filtern": "Filter projects",
    }
    for element in soup.find_all(attrs={"aria-label": True}):
        if element["aria-label"] in aria_map: element["aria-label"] = aria_map[element["aria-label"]]
    out = ROOT / "en/index.html"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(str(soup), encoding="utf-8")


def generate_pricing():
    soup = BeautifulSoup((ROOT / "Preis/index.html").read_text(), "html.parser")
    common(soup, "Pricing — Fufi Portfolio", "Approximate pricing for websites, Discord bots, automation and custom software.", "/Preis", "/en/pricing")
    mapping = {
        "Zum Inhalt springen":"Skip to content", "Projekte":"Projects", "Preis":"Pricing", "Kontakt":"Contact",
        "Leistungen & Preis":"Services & pricing", "Eine ehrliche Orientierung":"A clear indication", "vor dem ersten Gespräch.":"before the first conversation.",
        "Jedes Projekt ist anders. Die folgenden Bereiche sind ungefähre Richtwerte für klar abgegrenzte Arbeiten — der endgültige Preis hängt von Umfang, Design und vorhandener Technik ab.":"Every project is different. These ranges are approximate guidance for clearly scoped work — the final price depends on scope, design and existing technology.",
        "Keine versteckten Pakete":"No hidden packages", "Vor dem Start werden Ziel, Umfang und Preis gemeinsam festgehalten.":"Before work starts, goal, scope and price are agreed together.",
        "Kompakter Start":"Compact start", "Landingpage":"Landing page", "ca.":"approx.",
        "Eine schnelle, responsive Einzelseite für ein Projekt, Produkt oder Profil.":"A fast, responsive single page for a project, product or profile.",
        "Modernes responsives Design":"Modern responsive design", "Bis zu fünf Inhaltsbereiche":"Up to five content sections", "Kontakt- und Projektlinks":"Contact and project links", "Railway-ready Deployment":"Railway-ready deployment", "Anfragen":"Enquire",
        "Beliebte Wahl":"Popular choice", "Mehrseitiger Auftritt":"Multi-page presence", "Portfolio & Website":"Portfolio & website",
        "Ein vollständiger Webauftritt mit mehreren Seiten, eigener Bildsprache und sauberer Navigation.":"A complete web presence with several pages, a distinct visual style and clean navigation.",
        "Individuelles UI-Design":"Custom UI design", "Bis zu fünf Seiten":"Up to five pages", "Animationen und mobile Ansicht":"Animations and mobile layout", "SEO-Grundlagen & Security-Header":"SEO basics & security headers", "Railway-Konfiguration":"Railway configuration", "Website anfragen":"Enquire about a website",
        "Community & Workflow":"Community & workflow", "Discord-Bot":"Discord bot", "ab":"from",
        "Ein kleiner, klar abgegrenzter Discord-Bot. Umfangreichere Automationen werden vorher fair eingeschätzt.":"A small, clearly scoped Discord bot. Larger automation projects are estimated fairly in advance.",
        "Discord-Bot oder Automatisierung":"Discord bot or automation", "Befehle, Rollen oder Workflows":"Commands, roles or workflows", "Konfiguration über Umgebungsvariablen":"Environment-based configuration", "Deployment-Anleitung":"Deployment guide", "Bot anfragen":"Enquire about a bot",
        "Individuelle Lösung":"Custom solution", "Bot + Dashboard":"Bot + dashboard",
        "Für Systeme mit Login, API, Datenbank, Dashboard oder mehreren verbundenen Komponenten.":"For systems with login, API, database, dashboard or several connected components.",
        "Individuelle Architektur":"Custom architecture", "API und Datenhaltung":"API and data storage", "Dashboard und Rechtekonzept":"Dashboard and permissions", "Tests, Dokumentation und Deployment":"Tests, documentation and deployment", "Projekt besprechen":"Discuss a project",
        "Richtwerte in Euro. Hosting, Domains, kostenpflichtige APIs, Lizenzen und spätere Fremdkosten sind nicht enthalten. Formale Aufträge werden nur im rechtlich zulässigen Rahmen vereinbart.":"Indicative prices in euros. Hosting, domains, paid APIs, licences and later third-party costs are not included. Formal work is only agreed within the applicable legal framework.",
        "Ablauf":"Process", "Vier klare Schritte.":"Four clear steps.", "Keine unklare Dauerbaustelle: Vor dem Start steht fest, was gebaut wird und woran man „fertig“ erkennt.":"No endless, unclear build: before work starts, the scope and definition of done are clear.",
        "Idee":"Idea", "Ziel, Nutzer, Funktionen und vorhandene Technik kurz beschreiben.":"Briefly describe the goal, users, features and existing technology.",
        "Umfang":"Scope", "Ich schlage eine klare Lösung, einen Zeitraum und einen Preisrahmen vor.":"I suggest a clear solution, timeframe and price range.",
        "Umsetzung":"Build", "Design und Technik werden in nachvollziehbaren Schritten aufgebaut.":"Design and technology are built in understandable steps.",
        "Übergabe":"Handover", "Quellcode, Startanleitung und Deployment werden sauber übergeben.":"Source code, setup instructions and deployment are handed over cleanly.",
        "Kurz erklärt.":"Quick answers.", "Ist der angezeigte Preis garantiert?":"Is the displayed price guaranteed?", "Nein, er ist eine Orientierung. Nach einer kurzen Beschreibung bekommst du einen konkreteren Rahmen, bevor etwas begonnen wird.":"No. It is guidance. After a short description, you receive a more specific range before anything starts.",
        "Was macht ein Projekt teurer?":"What makes a project more expensive?", "Viele individuelle Seiten, Nutzerkonten, Datenbanken, komplexe Rechte, externe APIs, Echtzeitfunktionen und zusätzliche Änderungsrunden.":"Many custom pages, user accounts, databases, complex permissions, external APIs, real-time features and extra revision rounds.",
        "Kann ich mit einer kleinen Version starten?":"Can I start with a small version?", "Ja. Ein klarer erster Umfang ist meistens besser als sofort jede denkbare Funktion zu bauen.":"Yes. A clear first scope is usually better than building every imaginable feature at once.",
        "Was wird nicht angeboten?":"What is not offered?", "Credential-Sammlung, Exploits, Schadsoftware, Regelumgehung oder Funktionen, die Plattformen und andere Nutzer gefährden.":"Credential collection, exploits, malware, rule evasion or features that put platforms and other users at risk.",
        "Nächster Schritt":"Next step", "Erzähl mir kurz,":"Tell me briefly", "was du bauen möchtest.":"what you want to build.", "Kontakt öffnen":"Open contact page",
        "Software, Systeme & Interfaces.":"Software, systems & interfaces.", "Keine Tracker. Keine Cookies.":"No trackers. No cookies.", "Faire Richtwerte, individuelles Angebot.":"Fair guidance, individual quote.",
    }
    translate_text(soup, mapping)
    for a in soup.select('a[href^="/Kontakt"]'): a["href"] = a["href"].replace('/Kontakt','/en/contact').replace('projekt=','project=')
    for a in soup.select('a[href="/#projects"]'): a["href"] = "/en#projects"
    for a in soup.select('a[href="/Preis"]'): a["href"] = "/en/pricing"
    for a in soup.select('a[href="/Kontakt"]'): a["href"] = "/en/contact"
    nav_switch = soup.select_one('.nav .language-switch')
    footer_switch = soup.select_one('.footer .language-switch')
    if nav_switch: nav_switch['href'] = '/Preis'
    if footer_switch: footer_switch['href'] = '/Preis'
    out=ROOT/'en/pricing/index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(str(soup),encoding='utf-8')


def generate_contact():
    soup = BeautifulSoup((ROOT / "Kontakt/index.html").read_text(), "html.parser")
    common(soup, "Contact — Fufi Portfolio", "Contact Fufi via Discord, email or GitHub.", "/Kontakt", "/en/contact")
    mapping = {
        "Zum Inhalt springen":"Skip to content", "Projekte":"Projects", "Preis":"Pricing", "Kontakt":"Contact",
        "Eine gute Idee?":"A good idea?", "Lass uns darüber sprechen.":"Let's talk about it.",
        "Am schnellsten erreichst du mich über Discord. Für eine ausführlichere Anfrage kannst du auch eine E-Mail schreiben.":"Discord is the fastest way to reach me. For a more detailed enquiry, you can also send an email.",
        "Offen für neue Anfragen":"Open to new enquiries", "Websites, Discord-Systeme, Dashboards und klar abgegrenzte Automatisierung.":"Websites, Discord systems, dashboards and clearly scoped automation.",
        "Hauptkontakt":"Primary contact", "Discord-Profil":"Discord profile", "Für eine schnelle Nachricht, kurze Rückfragen oder um eine Projektidee zuerst locker zu besprechen.":"For a quick message, a short question or an informal first discussion about a project idea.", "Profil in Discord öffnen":"Open Discord profile",
        "Zweite Wahl":"Second option", "E-Mail":"Email", "Gut für längere Beschreibungen, Dateien, Anforderungen und einen ungefähren Budgetrahmen.":"Best for longer descriptions, files, requirements and an approximate budget range.", "E-Mail schreiben":"Send an email",
        "Code & Projekte":"Code & projects", "Repositories, öffentliche Projekte, technische Dokumentation und aktuelle Arbeit ansehen.":"View repositories, public projects, technical documentation and current work.", "GitHub öffnen":"Open GitHub",
        "Für eine gute Antwort":"For a useful reply", "Vier Infos reichen.":"Four details are enough.", "Du brauchst kein fertiges Lastenheft. Eine kurze, klare Nachricht macht den Start trotzdem deutlich einfacher.":"You do not need a finished specification. A short, clear message still makes the start much easier.",
        "Was?":"What?", "Website, Bot, Dashboard oder etwas anderes?":"Website, bot, dashboard or something else?", "Für wen?":"For whom?", "Wer benutzt das Ergebnis und welches Problem löst es?":"Who will use it and what problem does it solve?", "Wann?":"When?", "Gibt es einen echten Termin oder ist der Zeitraum flexibel?":"Is there a real deadline or is the timeframe flexible?", "Rahmen?":"Scope?", "Welche Funktionen sind Pflicht und welcher Preisbereich passt?":"Which features are essential and what price range works?",
        "Wichtig:":"Important:", "Schicke niemals Passwörter, Tokens, Backupcodes oder private Schlüssel. Falls ein Dienstzugang nötig wird, wird ein sicherer Weg abgesprochen.":"Never send passwords, tokens, backup codes or private keys. If service access is needed, a secure method will be agreed.",
        "Noch unsicher?":"Still unsure?", "Schau zuerst auf die":"Take a look at the", "ungefähren Preise.":"approximate pricing first.", "Preisübersicht":"View pricing",
        "Software, Systeme & Interfaces.":"Software, systems & interfaces.", "Discord zuerst · E-Mail alternativ":"Discord first · email second", "Keine Tracker. Keine Cookies.":"No trackers. No cookies.",
    }
    translate_text(soup, mapping)
    for a in soup.select('a[href="/#projects"]'): a["href"] = "/en#projects"
    for a in soup.select('a[href="/Preis"]'): a["href"] = "/en/pricing"
    for a in soup.select('a[href="/Kontakt"]'): a["href"] = "/en/contact"
    mail = soup.select_one('a[href^="mailto:"]')
    if mail: mail["href"] = "mailto:fufi1925@proton.me?subject=Project%20enquiry%20from%20the%20portfolio"
    email_label = soup.select_one('.email-card .contact-kicker b')
    if email_label: email_label.string = 'Email ↗'
    img = soup.select_one('.discord-profile img')
    if img: img['alt'] = 'Discord profile picture of 𝙻'
    nav_switch = soup.select_one('.nav .language-switch')
    footer_switch = soup.select_one('.footer .language-switch')
    if nav_switch: nav_switch['href'] = '/Kontakt'
    if footer_switch: footer_switch['href'] = '/Kontakt'
    out=ROOT/'en/contact/index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(str(soup),encoding='utf-8')


if __name__ == '__main__':
    generate_home(); generate_pricing(); generate_contact()
    print('English pages generated')

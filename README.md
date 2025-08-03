
# Home Assistant Plate Recognizer Integration

[![License](https://img.shields.io/github/license/JanFirlus/ha-platerecognizer.svg)](LICENSE)

Eine einfache Integration zur automatischen Nummernschilderkennung in Home Assistant mittels [Plate Recognizer API](https://www.platerecognizer.com/).  
Das erkannte Kennzeichen wird als Sensor in Home Assistant angezeigt und kann z. B. für Automationen verwendet werden.

---

## 🚘 Funktionen

- Upload eines Kamerabildes an die Plate Recognizer API
- Extraktion von:
  - ✅ Kennzeichen
  - ✅ Region (z. B. `DE`, `EU`)
  - ✅ E-Fahrzeug-Kennzeichnung
- Ausgabe der Daten in der Entität:  
  **`sensor.plate_recognizer_last_plate`**
- Kompatibel mit Automationen, Dashboards und Benachrichtigungen

---

## 🧱 Voraussetzungen

- Home Assistant Core **2025.7.2** oder neuer
- Plate Recognizer API Token: [https://app.platerecognizer.com/](https://app.platerecognizer.com/)

---

## 📦 Installation

1. 📁 Repository klonen oder ZIP herunterladen:
   ```bash
   git clone https://github.com/JanFirlus/ha-platerecognizer.git
   ```

2. 📂 Den Ordner `custom_components/platerecognizer` in folgendes Verzeichnis kopieren:
   ```
   /config/custom_components/platerecognizer/
   ```

3. 🔄 Home Assistant **neu starten**.

4. 🔧 Integration über die Benutzeroberfläche hinzufügen:
   - Home Assistant → **Einstellungen → Geräte & Dienste → Integration hinzufügen**
   - Suche nach **Plate Recognizer**
   - Trage deinen **API-Token**, eine optionale **Kamera-ID** und den Standard-Bildpfad ein

---

## 📸 Bildverarbeitung (Service-Aufruf)

Ein Bild wird mithilfe des folgenden Serviceaufrufs verarbeitet:

```yaml
service: platerecognizer.scan
data:
  image_path: "/config/www/platecheck.jpg"
  camera_id: "garage"
```

Das Bild wird an die Plate Recognizer API gesendet, und die Antwort aktualisiert automatisch den Sensor `sensor.plate_recognizer_last_plate`.

---

## 🧠 Sensor-Entität

| Entität                              | Beschreibung                            |
|-------------------------------------|-----------------------------------------|
| `sensor.plate_recognizer_last_plate` | Zeigt das zuletzt erkannte Kennzeichen |

**Mögliche Attribute:**
- `region`: z. B. `"de"`, `"eu"`
- `e_vehicle`: `"ja"` oder `"nein"`
- `camera`: Kamera-ID (falls mitgegeben)

---

## 🔔 Beispiel: Automation für Toröffnung

```yaml
alias: Tor öffnen bei erkanntem Kennzeichen
trigger:
  - platform: state
    entity_id: sensor.plate_recognizer_last_plate
condition:
  - condition: template
    value_template: "{{ trigger.to_state.state == 'wobn588e' }}"
action:
  - service: cover.open_cover
    target:
      entity_id: cover.garagentor
```

---

## 🛠️ Fehlerbehebung

- **Sensor bleibt auf "unbekannt":**
  - API-Token prüfen
  - Bildpfad korrekt?
  - Logs kontrollieren (z. B. `Fehler 401`, `Fehler 404`)
  - Gültiges JPEG verwenden (`image/jpeg`)

- **Sensor nicht sichtbar?**
  - Home Assistant komplett neustarten
  - Integration vollständig entfernt & neu hinzugefügt?

---

## 🧪 Entwicklermodus

- Sensorwerte können manuell unter **Entwicklerwerkzeuge → Zustände** gesetzt und beobachtet werden
- Die Sensorentität kann auch in `Lovelace` Dashboards eingebunden werden

---

## 📄 Lizenz

[MIT License](LICENSE)

---

## ❤️ Feedback & Mitmachen

- Issues und Pull Requests sind willkommen!
- Feedback und Ideen gern als Issue posten

---

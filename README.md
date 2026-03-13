# 🚨 Oref Alert — פיקוד העורף for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/boris327/hacs-oref-alert.svg)](https://github.com/boris327/hacs-oref-alert/releases)
![Maintenance](https://img.shields.io/maintenance/yes/2024)

אינטגרציית **פיקוד העורף** ל-Home Assistant — אזעקות בזמן אמת, מפה ומידע על נפילות.

---

## ✨ תכונות

| סנסור | תיאור | עדכון |
|-------|-------|-------|
| `binary_sensor.oref_alert_active` | **האם יש אזעקה פעילה** | כל 10 שניות |
| `sensor.oref_alert_status` | סטטוס (`active` / `clear`) | כל 10 שניות |
| `sensor.oref_alert_zones_count` | מספר האזורים המוזהרים | כל 10 שניות |
| `sensor.oref_alert_zones_list` | רשימת האזורים (מופרדת ב-•) | כל 10 שניות |
| `sensor.oref_alert_category` | סוג האיום (רקטות / כלי טיס / מחבלים...) | כל 10 שניות |
| `sensor.oref_alert_title` | כותרת האזעקה | כל 10 שניות |
| `sensor.oref_alert_history_count` | מספר אזעקות ב-24 שעות האחרונות | כל 10 שניות |

---

## 📦 התקנה דרך HACS

### שיטה 1 — HACS Custom Repository (מומלץ)

1. פתח **HACS** ב-Home Assistant
2. לחץ על ⋮ (שלוש נקודות) → **Custom repositories**
3. הוסף: `https://github.com/boris327/hacs-oref-alert`
4. בחר **Integration** ולחץ **Add**
5. חפש **"Oref Alert"** והתקן
6. הפעל מחדש את Home Assistant
7. עבור ל-**Settings → Devices & Services → Add Integration** → חפש **"Oref Alert"**

### שיטה 2 — התקנה ידנית

```bash
cd config/custom_components
git clone https://github.com/boris327/hacs-oref-alert/custom_components/oref_alert oref_alert
```

---

## 🗺️ דשבורד — מפת פיקוד העורף

כלול בקוד: קובץ `docs/dashboard.yaml` — מפה אינטראקטיבית עם:
- **באנר אזעקה** מהבהב באדום כשיש אזעקה
- **iframe** מוטמע לאתר פיקוד העורף  
- **אזורים מוזהרים** כגריד דינמי
- **היסטוריית אזעקות**
- קישורים מהירים לאתר + אפליקציה

---

## 🤖 אוטומציה לדוגמה

```yaml
automation:
  - alias: "פיקוד העורף — אזעקה פעילה"
    trigger:
      platform: state
      entity_id: binary_sensor.oref_alert_active
      to: "on"
    action:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.speaker
          message: "{{ states('sensor.oref_alert_zones_list') }}"
      - service: notify.mobile_app
        data:
          title: "🚨 אזעקה!"
          message: "{{ states('sensor.oref_alert_zones_list') }}"
          data:
            priority: high
```

---

## 📋 דרישות

- Home Assistant 2023.1+
- HACS (להתקנה דרך HACS)
- **שרת עם IP ישראלי** — ה-API של פיקוד העורף מוגבל לישראל

---

## 🔗 קישורים

- [אתר פיקוד העורף](https://www.oref.org.il)
- [דיווח על בעיות](https://github.com/boris327/hacs-oref-alert/issues)

---

## 📜 רישיון

MIT License — שימוש חופשי לכל מטרה.

---

> **⚠️ הערה:** אינטגרציה זו אינה מקושרת רשמית לפיקוד העורף. השתמש תמיד באזעקות הרשמיות ובאפליקציית פיקוד העורף.

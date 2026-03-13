# 🚨 Smart Home Azakot — אזעקות חכמות

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/boris327/hacs-oref-alert.svg)](https://github.com/boris327/hacs-oref-alert/releases)

אינטגרציית **Smart Home Azakot** ל-Home Assistant — אזעקות פיקוד העורף בזמן אמת, ישירות לבית החכם שלך.

---

## ✨ ישויות

| ישות | תיאור | עדכון |
|------|-------|-------|
| `binary_sensor.azakot_active` | האם יש אזעקה פעילה | כל 10 שניות |
| `sensor.azakot_status` | סטטוס (`active` / `clear`) | כל 10 שניות |
| `sensor.azakot_zones_count` | מספר האזורים המוזהרים | כל 10 שניות |
| `sensor.azakot_zones_list` | רשימת האזורים | כל 10 שניות |
| `sensor.azakot_category` | סוג האיום | כל 10 שניות |
| `sensor.azakot_title` | כותרת האזעקה | כל 10 שניות |
| `sensor.azakot_history_count` | אזעקות 24 שעות אחרונות | כל 10 שניות |

---

## 📦 התקנה דרך HACS

1. פתח **HACS** → ⋮ → **Custom repositories**
2. הוסף: `https://github.com/boris327/hacs-oref-alert` | Category: **Integration**
3. חפש **"Smart Home Azakot"** → **Download**
4. הפעל מחדש Home Assistant
5. **Settings → Integrations → Add → "Smart Home Azakot"** → Submit

---

## 🤖 אוטומציה לדוגמה

```yaml
automation:
  - alias: "Smart Home Azakot — אזעקה פעילה"
    trigger:
      platform: state
      entity_id: binary_sensor.azakot_active
      to: "on"
    action:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.speaker
          message: "אזעקה! {{ states('sensor.azakot_zones_list') }}"
      - service: notify.mobile_app
        data:
          title: "🚨 Smart Home Azakot"
          message: "{{ states('sensor.azakot_zones_list') }}"
          data:
            priority: high
```

---

## ⚠️ דרישות

- Home Assistant 2023.1+
- **שרת עם IP ישראלי** — ה-API של פיקוד העורף מוגבל לישראל

---

> אינטגרציה זו אינה מקושרת רשמית לפיקוד העורף. השתמש תמיד באפליקציה הרשמית.

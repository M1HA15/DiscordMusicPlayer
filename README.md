<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue.svg" alt="Python 3.13"/>
  <img src="https://img.shields.io/badge/License-GPLv3-green.svg" alt="GPL-3.0 License"/>
  <img src="https://img.shields.io/badge/Discord-Music%20Bot-purple.svg" alt="Discord Music Bot"/>
</p>

# 🎵 Discord Music Player / Bot de Muzică Discord 🎵

**EN:** A sleek, open-source Discord music bot delivering high-quality audio playback, smart queue & playlist management, and multilingual support.  
**RO:** Un bot de muzică Discord open-source, modern, cu redare audio de înaltă calitate, gestionare inteligentă a cozii și playlisturilor și suport multilingv.

---

## ✨ Key Features / Funcționalități

| 🇬🇧 **Features**                       | 🇷🇴 **Funcționalități**                 |
|---------------------------------------|----------------------------------------|
| 🎶 High-Quality Streaming             | 🎶 Streaming de înaltă calitate        |
| ⚡ Instant Play / Pause / Skip        | ⚡ Play/Pauză/Skip instant             |
| 📋 Smart Queue & Playlist System      | 📋 Coadă & playlisturi inteligente     |
| 🔍 Search by Name or URL              | 🔍 Caută după nume sau URL             |
| 🔊 Dynamic Volume Control             | 🔊 Control dinamic al volumului        |
| 🌐 English & Romanian Interfaces      | 🌐 Interfețe EN & RO                   |
| 🛠️ Configurable via settings.json     | 🛠️ Configurabil prin settings.json    |
| 🔒 Owner & DJ Role Permissions        | 🔒 Permisiuni Owner & DJ Role          |
| 📖 Interactive, Paginated Help        | 📖 Ajutor interactiv, paginat          |

---

## ⚙️ Installation / Instalare

1. **Download ZIP** from GitHub and extract.  
2. **Install Python 3.13.2+** and add to PATH.  
3. **Install FFmpeg** and add to PATH.  
4. **Open terminal** in project folder:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure** `settings.json` (see below).  
6. **Run**:
   - English: `python bot_en.py`
   - Română:  `python bot_ro.py`

---

## 🛠️ Configuration / Configurare

Create `settings.json` in root:

```json
{
  "token": "YOUR_DISCORD_BOT_TOKEN",
  "prefix": ".",
  "alt_prefix": "ham",
  "owner_id": "YOUR_DISCORD_ID",
  "guild_ids": [],
  "dj_roles": {},
  "timeout": 30,
  "volume": 1.0,
  "status_type": "playing",
  "status_message": "github.com/M1HA15"
}
```

---

## 📦 Dependencies / Dependențe

```
discord.py
yt-dlp
PyNaCl
```
Install:
```bash
pip install -r requirements.txt
```

---

## 📞 Contact

- Discord: mihaivere  
- GitHub: https://github.com/M1HA15/DiscordMusicPlayer  

---

## 📝 License / Licență

Distributed under the [GPL-3.0 License](https://github.com/M1HA15/DiscordMusicPlayer/blob/main/LICENSE).  

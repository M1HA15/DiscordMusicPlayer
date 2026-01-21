<p align="center">
  <a href="https://github.com/M1HA15/DiscordMusicPlayer"><img src="https://img.shields.io/github/stars/M1HA15/DiscordMusicPlayer?style=social" alt="GitHub stars"></a>
  <img src="https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg" alt="Python >=3.10"/>
  <img src="https://img.shields.io/badge/License-GPLv3-green.svg" alt="GPLv3 License"/>
  <img src="https://img.shields.io/badge/Discord-Music%20Bot-purple.svg" alt="Discord Music Bot"/>
</p>

# 🎵 Discord Music Player | Bot de Muzică 🎵

🇬🇧 A sleek, open-source Discord music bot delivering high-quality audio playback, smart queue & playlist management, and multilingual support.  
🇷🇴 Un bot de muzică Discord open-source, modern, cu redare audio de înaltă calitate, gestionare inteligentă a cozii și playlisturilor, și suport multilingv.

---

## ✨ Key Features / Funcționalități Cheie

| 🇬🇧 **Features**                     | 🇷🇴 **Funcționalități**               |
|-------------------------------------|-------------------------------------|
| 🎶 High-Quality Streaming            | 🎶 Streaming de înaltă calitate       |
| ⚡ Instant Play / Pause / Skip       | ⚡ Play / Pauză / Skip instant       |
| 📋 Smart Queue & Playlist System     | 📋 Coadă și playlisturi inteligente   |
| 🔍 Search by Name or URL             | 🔍 Caută după nume sau URL           |
| 🔊 Dynamic Volume Control            | 🔊 Control dinamic al volumului      |
| 🌐 English & Romanian Interfaces     | 🌐 Interfețe în Engleză & Română      |
| 🛠️ Configurable via `settings.json` | 🛠️ Configurabil prin `settings.json` |
| 🔒 Owner & DJ Role Permissions       | 🔒 Permisiuni Owner & DJ             |
| 📖 Interactive, Paginated Help       | 📖 Ajutor interactiv, paginat        |
| 🔄 Loop & Shuffle                   | 🔄 Comenzi loop și shuffle           |

---

## 🚀 Installation / Instalare

1. **Python & Libraries**  
   🇬🇧 Ensure **Python 3.10+** is installed.  
   🇷🇴 Asigură-te că **Python 3.10+** este instalat.  
   ```bash
   pip install -r requirements.txt
   ```
2. **FFmpeg**  
   🇬🇧 Download & install FFmpeg:  
   - Official: https://www.ffmpeg.org/download.html  
   - Tutorial: https://youtu.be/JR36oH35Fgg  
   🇷🇴 Descarcă și instalează FFmpeg:  
   - Oficial: https://www.ffmpeg.org/download.html  
   - Tutorial: https://youtu.be/JR36oH35Fgg  
3. **Clone & Run**  
   ```bash
   git clone https://github.com/M1HA15/DiscordMusicPlayer.git
   cd DiscordMusicPlayer
   # configure settings.json (see below)
   python bot_en.py   # for English
   python bot_ro.py   # for Romanian
   ```

---

## ⚙️ Configuration / Configurare

Create a `settings.json` in the project root:

```json
{
  "token": "YOUR_DISCORD_BOT_TOKEN",
  "prefix": ".",
  "alt_prefix": "!",
  "owner_id": "YOUR_DISCORD_ID",
  "guild_ids": [],
  "dj_roles": {},
  "timeout": 30,
  "volume": 1.0,
  "status_type": "playing",
  "status_message": "Bot is playing"
}
```

- **token** – Your bot token (Discord Developer Portal)  
- **prefix** – Command prefix (e.g. `.`)  
- **alt_prefix** – Alternative prefix  
- **owner_id** – Your Discord user ID  
- **guild_ids** – Allowed server IDs (empty = all)  
- **dj_roles** – Map server ID → DJ role ID  
- **timeout** – Idle timeout in minutes  
- **volume** – Default volume (0.0–1.0)  
- **status_type**/**status_message** – Custom presence

---

## 💖 Donations / Donații

🇬🇧 If you enjoy this bot, consider supporting development!  
🇷🇴 Dacă îți place botul, susține dezvoltarea printr-o donație!

- **PayPal:** [paypal.me/mihaiserif](https://paypal.me/mihaiserif)  
- **LTC (Litecoin):** `LUoHjsi2dDC9tRDyuuBVHF3Lo7fFwgVNYs`  
- **BTC (Bitcoin):** `bc1qmajqt2nrg9twys8r9ddnuwcgtsemt98j99l`  
- **ETH (Ethereum):** `0x92E4AEdc19f9e5D7d0a532B7B358e394B71e8843`

---

## 🌟 Show Your Support / Arată-ți sprijinul

🇬🇧 If you find this project useful, give it a ⭐ on GitHub!  
🇷🇴 Dacă îți place proiectul, dă-i ⭐ pe GitHub!

---

## 📫 Contact

- **GitHub:** [M1HA15](https://github.com/M1HA15)  
- **Discord:** `mihaifbd`

---

## 📝 License / Licență

This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).  
Proiect licențiat sub [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).

---

## 🙏 Thanks / Mulțumiri

🇬🇧 Special thanks to the open-source community and all contributors!  
🇷🇴 Mulțumiri speciale comunității open-source și tuturor contribuabililor!

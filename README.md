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

## 🌟 Why Choose Our Bot? / De ce să alegi botul nostru?

**EN:**  
- Easy to set up and configure.  
- Exclusive support for YouTube links — simply paste a link and enjoy.  
- Lightweight and optimized performance.  
- Regular updates and community-driven features.  

**RO:**  
- Configurare și utilizare ușoară.  
- Suport exclusiv pentru linkuri YouTube — copiază și are melodia!  
- Consum redus de resurse și performanță optimizată.  
- Actualizări regulate și funcționalități propuse de comunitate.  

---

## ⚠️ Disclaimer / Declarație de Responsabilitate

**EN:** The developers are not responsible for copyright issues arising from streaming third-party content. Use this bot at your own risk and ensure you comply with Discord's Terms of Service and the content provider's policies.  
**RO:** Dezvoltatorii nu sunt responsabili pentru probleme de drepturi de autor care pot apărea din redarea conținutului terț. Folosește acest bot pe propriul risc și asigură-te că respecți Termenii Discord și politicile furnizorilor de conținut.

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

## 🙏 Acknowledgments / Mulțumiri

**EN:** Thanks to all contributors and the open-source community for continuous support and inspiration.  
**RO:** Mulțumiri tuturor contribuabililor și comunității open-source pentru sprijinul și inspirația continuă.

---

## 📝 License / Licență

Distributed under the [GPL-3.0 License](https://github.com/M1HA15/DiscordMusicPlayer/blob/main/LICENSE).  

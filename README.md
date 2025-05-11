# Discord Music Player / Bot de Muzică Discord

**EN:** Discord Music Player is a fast, customizable, open-source music bot for Discord. It streams high-quality audio from YouTube, SoundCloud, and more—complete with queue management, playlists, volume control, and multilingual support.

**RO:** Discord Music Player este un bot de muzică open-source rapid și personalizabil pentru Discord. Redă audio de înaltă calitate de pe YouTube, SoundCloud și altele—cu gestionare coadă, playlisturi, control volum și suport multilingv.

## 🚀 Features / Funcționalități

| 🇬🇧 Features                                    | 🇷🇴 Funcționalități                               |
|-----------------------------------------------|--------------------------------------------------|
| ▶️ Play/Pause/Resume                          | ▶️ Redare/Pauză/Continuare                       |
| ⏭️ Skip current track                         | ⏭️ Sari peste piesa curentă                       |
| 📜 View & manage queue                        | 📜 Vizualizează și gestionează coada             |
| 📂 Create & manage personal playlists         | 📂 Creează și gestionează playlisturi             |
| 🔍 Search and add tracks by name or URL        | 🔍 Caută și adaugă piese după nume sau URL       |
| 🔊 Adjustable volume                          | 🔊 Control volum                                  |
| 🌐 Multilingual (EN + RO)                     | 🌐 Multilingv (EN + RO)                           |
| 💾 Configurable via settings.json             | 💾 Configurabil prin settings.json                |
| 🔒 Owner & DJ role permissions                | 🔒 Permisiuni owner & rol DJ                     |
| 📖 Paginated help command                     | 📖 Comandă de ajutor paginată                    |

## 📋 Technical Requirements / Cerințe Tehnice

- Python 3.13.2 or newer  
- FFmpeg installed & in your system PATH  
- Internet connection  
- A valid Discord Bot Token  
- Supported OS: Windows 10+ or Linux

## ⚙️ Installation / Instalare

### Windows

```bash
git clone https://github.com/M1HA15/DiscordMusicPlayer.git
cd DiscordMusicPlayer
pip install -r requirements.txt
```
1. Install Python 3.13.2 (add to PATH).  
2. Install FFmpeg and add to PATH.  
3. Clone & install dependencies.  
4. Configure settings.json (see below).  
5. Run:
   - English: `python bot_en.py`
   - Română:  `python bot_ro.py`

### Linux

```bash
sudo apt update
sudo apt install python3.13 python3-pip ffmpeg
git clone https://github.com/M1HA15/DiscordMusicPlayer.git
cd DiscordMusicPlayer
pip3 install -r requirements.txt
```
1. Install Python & FFmpeg via package manager.  
2. Clone & install dependencies.  
3. Configure settings.json (see below).  
4. Run:
   - English: `python3 bot_en.py`
   - Română:  `python3 bot_ro.py`

## 🛠️ Configuration / Configurare

Create a `settings.json` in project root:

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
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

## 📦 Dependencies / Dependențe

```
discord.py
yt-dlp
PyNaCl
```

Install with:

```bash
pip install -r requirements.txt
```

## 📞 Contact

- Discord: mihaivere  
- GitHub: https://github.com/M1HA15/DiscordMusicPlayer

## 📝 License / Licență

Distributed under the GPL-3.0 License. See LICENSE for details.

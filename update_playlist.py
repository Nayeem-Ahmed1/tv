import re
import requests

# Base configuration
BASE_URL = "http://tv.bdiptv.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://tv.bdiptv.net/",
}

# Map of channels: (display_name, tvg_id, category, logo_url, page_slug_or_identifier)
CHANNELS = [
    {
        "name": "Star Sports 1",
        "id": "star-sports-1",
        "group": "Sports",
        "logo": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/73/Star_Sports_1_HD.png/1280px-Star_Sports_1_HD.png",
        "stream_path": "http://103.89.248.22:8082/STAR-SPORTS-1/index.fmp4.m3u8"
    },
    {
        "name": "Star Sports 2",
        "id": "star-sports-2",
        "group": "Sports",
        "logo": "https://static.wikia.nocookie.net/logopedia/images/a/ac/Star_Sports_2.jpg/revision/latest?cb=20191214232359",
        "stream_path": "http://103.89.248.22:8082/STAR-SPORTS-2/index.fmp4.m3u8"
    },
    {
        "name": "T Sports HD",
        "id": "tsports.bd",
        "group": "Sports",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/T_Sports_logo.svg/1280px-T_Sports_logo.svg.png",
        "stream_path": "http://103.89.248.22:8082/T-SPORTS/index.fmp4.m3u8"
    },
    {
        "name": "Live 1",
        "id": "live-1",
        "group": "Sports",
        "logo": "https://img.freepik.com/premium-vector/live-streaming-sign-vector-template_917138-3612.jpg",
        "stream_path": "http://103.89.248.14:8082/1LIVE/index.fmp4.m3u8"
    },
    {
        "name": "Live 2",
        "id": "live-2",
        "group": "Sports",
        "logo": "https://img.freepik.com/premium-vector/live-streaming-sign-vector-template_917138-3612.jpg",
        "stream_path": "http://103.89.248.14:8082/LIVE-FOOTBALL/index.fmp4.m3u8"
    },
    {
        "name": "Live 3",
        "id": "live-3",
        "group": "Sports",
        "logo": "https://img.freepik.com/premium-vector/live-streaming-sign-vector-template_917138-3612.jpg",
        "stream_path": "http://103.89.248.22:8082/LIVE-FOOTBALL-1/index.fmp4.m3u8"
    },
    {
        "name": "Jamuna TV",
        "id": "jamuna-tv",
        "group": "News",
        "logo": "https://cdn.brandfetch.io/domain/jamuna.tv/fallback/lettermark/theme/dark/h/400/w/400/icon?c=1bfwsmEH20zzEfSNTed",
        "stream_path": "http://103.89.248.30:8082/Jamuna/index.fmp4.m3u8"
    },
    {
        "name": "ATN News",
        "id": "atn-news",
        "group": "News",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/ATN_News_Logo_without_slogan.svg/1280px-ATN_News_Logo_without_slogan.svg.png",
        "stream_path": "http://103.89.248.14:8082/ATN-NEWS/index.fmp4.m3u8"
    },
    {
        "name": "News 24",
        "id": "news-24",
        "group": "News",
        "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaka80ybkeV-6TkUNyUpgTaT-GM6wrpQ3ZR4TcDERKL43MfvlZRuCnev2b&s=10",
        "stream_path": "http://103.89.248.26:8082/NEWS-24/index.fmp4.m3u8"
    },
    {
        "name": "DBC News",
        "id": "dbc-news",
        "group": "News",
        "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJbPPZi4ZIzLbWDwWOBWEBQJuRloqeHKOX1AL5ATOi5A&s=10",
        "stream_path": "http://103.89.248.10:8082/DBC-NEWS/index.fmp4.m3u8"
    },
    {
        "name": "Independent",
        "id": "independent-news",
        "group": "News",
        "logo": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcBbq3L9-tX5bCT3fkASm5YGQYJDp5TnskpQ5I4dgSmq76v8vebYCzW824q-R4ICdBlKo1rfuopZbYjU7iquwIiVL3prlw89vJUWe0yeyz_mxfNrcEahGXFs3QcmcTuIsAsaGgCeGNXlF9/s1600/independent-television.jpg",
        "stream_path": "http://103.89.248.10:8082/INDEPENDENT-NEWS/index.fmp4.m3u8"
    },
    {
        "name": "Ekattor TV",
        "id": "ekattor-tv",
        "group": "News",
        "logo": "https://cdn.ekattorbd.com/contents/cache/images/1200x630x1/uploads/media/2023/08/13/default-f5a63c8327b98eafee564f28c3a9ebdb.png",
        "stream_path": "http://103.89.248.14:8082/71-TV/index.fmp4.m3u8"
    },
    {
        "name": "Jolsha Movies",
        "id": "jolsha-movies",
        "group": "Bangla",
        "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqdpnDbVb7ON6KSbuo5-RM4cuocUBI7O6qVgIydb71qQ&s=10",
        "stream_path": "http://103.89.248.30:8082/JALSHA-MOVIES/index.fmp4.m3u8"
    },
    {
        "name": "Star Jolsha",
        "id": "star-jolsha",
        "group": "Bangla",
        "logo": "https://logos.fandom.com/wiki/Star_Jalsha",
        "stream_path": "http://103.89.248.14:8082/Star_jalsha/index.fmp4.m3u8"
    }
]

def fetch_fresh_token():
    """Scrapes tv.bdiptv.net to retrieve the active session token."""
    try:
        # Load main portal
        res = requests.get(BASE_URL, headers=HEADERS, timeout=12)
        res.raise_for_status()
        html = res.text

        # Search for token patterns commonly found in iframe src or embed player JS
        # Example pattern: token=5503ad7e...-1788962267-1788951467
        token_match = re.search(r'token=([a-zA-Z0-9_-]+)', html)
        if token_match:
            return token_match.group(1)

        # If token is within an iframe source (e.g. src="...embed.html?token=...")
        iframe_src = re.search(r'src=["\']([^"\']*embed\.html\?token=[^"\']*)["\']', html)
        if iframe_src:
            token_match = re.search(r'token=([a-zA-Z0-9_-]+)', iframe_src.group(1))
            if token_match:
                return token_match.group(1)

    except Exception as e:
        print(f"Error fetching live token from site: {e}")
    return None

def build_playlist(token):
    lines = ["#EXTM3U\n"]
    for ch in CHANNELS:
        entry = (
            f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" '
            f'tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n'
            f'{ch["stream_path"]}?token={token}\n'
        )
        lines.append(entry)
    return "\n".join(lines)

if __name__ == "__main__":
    token = fetch_fresh_token()
    
    if not token:
        print("Warning: Could not grab new token automatically. Check site access or network scope.")
        exit(1)

    print(f"Acquired token: {token[:16]}... (valid)")
    m3u_text = build_playlist(token)

    with open("iptv.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_text)

    print("iptv.m3u updated successfully.")

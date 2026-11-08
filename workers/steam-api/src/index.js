// Steam library lookup for the games page. The Steam Web API needs a key
// (which can't be put in the browser) and sends no CORS headers, so the
// page calls this Worker instead. The key is the Worker secret `steam_api`
// (Settings > Variables and secrets), never committed.
export default {
  async fetch(request, env) {
    // Dev origins must be listed explicitly - with only the production
    // domain here the mkdocs preview can't call this at all, because the
    // browser blocks the response before your code ever sees it.
    const ALLOWED_ORIGINS = new Set([
      "https://portmaster.games",
      "https://portmaster-wiki.portmaster-team.workers.dev",
      "https://portmaster-wiki.portmaster.workers.dev",
      "http://localhost:8000",
      "http://localhost:8642",
    ]);

    const origin = request.headers.get("Origin") || "";
    const corsHeaders = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGINS.has(origin)
        ? origin
        : "https://portmaster.games",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      // Without this, a cache can hand one origin's Allow-Origin header to
      // a different origin and break it intermittently.
      Vary: "Origin",
    };

    const json = (body, status = 200) =>
      new Response(JSON.stringify(body), {
        status,
        headers: { "Content-Type": "application/json", ...corsHeaders },
      });

    // Preflight request - browsers send this before the real GET/POST
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const apiKey = env.steam_api;

    // Steam serves an HTML error page (not JSON) for a bad key or a
    // malformed steamid, so check for that before parsing.
    async function steamJson(url) {
      const res = await fetch(url);
      const text = await res.text();
      if (text.startsWith("<")) {
        throw new Error(
          "Steam API returned an HTML page - check your API key or Steam ID"
        );
      }
      return JSON.parse(text);
    }

    // Accepts any of:
    //   76561197960287930
    //   https://steamcommunity.com/profiles/76561197960287930
    //   https://steamcommunity.com/id/<vanity>
    //   <vanity>
    async function resolveSteamId(input) {
      const raw = String(input || "").trim();
      if (!raw) throw new Error("Enter a Steam username or profile URL");

      const byProfile = raw.match(/steamcommunity\.com\/profiles\/(\d{17})/);
      if (byProfile) return byProfile[1];
      if (/^\d{17}$/.test(raw)) return raw;

      const byId = raw.match(/steamcommunity\.com\/id\/([^/?#]+)/);
      const vanity = byId ? byId[1] : raw;

      const data = await steamJson(
        `https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/` +
          `?key=${apiKey}&vanityurl=${encodeURIComponent(vanity)}`
      );
      // success: 1 = resolved, 42 = no such vanity name
      if (data?.response?.success !== 1 || !data?.response?.steamid) {
        throw new Error("No Steam account with that name");
      }
      return data.response.steamid;
    }

    async function ownedAppIds(steamId) {
      const data = await steamJson(
        `https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/` +
          `?key=${apiKey}&steamid=${encodeURIComponent(steamId)}` +
          // include_appinfo=false: only appids are needed to match against
          // the ports, and the full payload runs to hundreds of KB on a
          // large account. include_played_free_games catches the free-to-play
          // titles that some ports are based on.
          `&include_appinfo=false&include_played_free_games=true&format=json`
      );
      const games = data?.response?.games;
      return {
        steamId,
        // A private profile answers 200 with {"response":{}}, which is
        // otherwise indistinguishable from owning nothing at all. The
        // frontend needs to tell those apart to show the right message.
        private: !Array.isArray(games),
        appids: (games || []).map((g) => g.appid),
      };
    }

    try {
      const url = new URL(request.url);

      // GET /u/<username|profile url|steamid> - resolves whatever the
      // visitor typed and returns the appids in one round trip.
      if (url.pathname.startsWith("/u/")) {
        const raw = decodeURIComponent(url.pathname.slice(3));
        return json(await ownedAppIds(await resolveSteamId(raw)));
      }

      // Original entry points: GET /<steamid> and POST {"steamId": "..."}
      let steamId;
      if (request.method === "POST") {
        steamId = (await request.json()).steamId;
      } else {
        steamId = url.pathname.slice(1);
      }

      if (!steamId) {
        return json(
          { error: "Missing steamId. Use POST JSON or GET path." },
          400
        );
      }

      return json(await ownedAppIds(steamId));
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  },
};

# Making this bot NEON~V2 | Official's bot

This is the full source (this zip had `core/` and `utils/` — the earlier
partial zip you sent me was missing them). Below is everything I changed,
and everything you still need to fill in yourself.

## ⚠️ Never reuse the token/API key that came in this zip

The original `env` file shipped with a live Discord bot token and a live
Groq API key belonging to whoever built this bot originally. I've replaced
both with placeholders. Get your own token from the
[Discord Developer Portal](https://discord.com/developers/applications)
and your own key from [console.groq.com](https://console.groq.com).

---

## Security fixes (the important part)

This codebase had the original developer wired into it in **eight
different places** — not just cosmetically, but with actual elevated
access to any server running the bot. All of it is now removed:

1. **`CodeX.py`** — an `on_command_completion` listener sent every command
   anyone ran, anywhere, to a Discord webhook the original dev controlled
   (user, server, channel included). Deleted entirely.

2. **`utils/config.py`** — `OWNER_IDS` was hardcoded to the original dev's
   Discord ID. This is the list that governs `jishaku` (full Python
   eval/shell access on the bot) and every `@commands.is_owner()` command
   in the codebase. **You must fill this in with your own Discord user ID**
   or the bot has no real owner at all.

3. **`cogs/commands/owner.py`** — this file *redefined* `OWNER_IDS` locally
   right after importing the real one, silently overriding whatever you
   set in `utils/config.py` for that file's own checks (staff badges,
   `guildinfo`, `slist`). Deleted the shadow copy; it now uses the one
   real list from `utils/config.py`.

4. **`cogs/commands/emergency.py`** — four separate commands (`enable`,
   `disable`, `emergencysituation`, `emergencyrestore` — server lockdown
   controls) checked `ctx.guild.owner_id` **or** a hardcoded fallback ID
   belonging to the original dev. That fallback bypass is removed; only
   the real server owner (and your configured extra-owners, where
   applicable) can run these now.

5. **`cogs/commands/extraown.py`** — same bypass pattern on an
   owner-only command. Removed.

6. **`cogs/commands/autorole.py`** — a button `interaction_check` let the
   original dev's ID click through any menu that wasn't theirs, on any
   server. Removed.

7. **`cogs/commands/nightmode.py`** — a hardcoded `self.ricky` list gave
   the same ID a permission bypass on four separate checks. Removed.

8. **`cogs/commands/dms.py`** — an `authorized_staff_ids` list came
   pre-filled with two IDs that weren't yours (one was the original dev's),
   letting them DM your members through your bot under a "Staff Team"
   embed. Both removed — **you need to add your own staff IDs** here if
   you want to use this feature. See the comment in the file.

None of these were things you could have "kept but rebranded" — they gave
someone outside your server real control over it, independent of anything
you configure. They're gone, not renamed.

---

## Branding cleanup

The old branding ("Zyrox", "Zyrox X", "Zyrox Development™") and the old
support-server link (`discord.gg/codexdev`) appeared across **30+ files**
— embed titles, footers, help text, role names, an AI system prompt, even
a couple of Discord channel-name checks (`zyrox-automod`,
`zyrox-ticket-logs`, now `neonv2-automod` / `neonv2-ticket-logs`).
All of it has been swapped to **NEON~V2**. This included:

- Every embed title/footer crediting "Zyrox Development™" or similar →
  "NEON~V2 | Official"
- The AI chatbot's system prompt (`cogs/commands/ai.py`) — no longer
  introduces itself as "Zyrox" or credits the old developer by name
- Dev-credit sections in `cogs/events/mention.py` and
  `cogs/commands/stats.py` — replaced with placeholder text; add your own
  credits if you want any
- The old bot's invite link and Discord CDN avatar URLs — replaced with
  placeholders (see below) or removed where they were just decorative
  icons on embeds
- `core/zyrox.py`'s rotating status messages

**What I deliberately did NOT rename:** the Python module/class name
`zyrox` itself (`core/zyrox.py`, `from core import zyrox`, `class
zyrox(...)`, the `cogs/zyrox/` subpackage, and all the `from
.zyrox.xxx import` lines in `cogs/__init__.py`). Renaming those means
renaming files and updating dozens of import statements consistently —
doable, but risky to do blind, and purely cosmetic since none of it is
user-facing. If you want that done too, tell me and I'll do it as its own
pass so I can verify nothing breaks.

Also left alone: the custom emoji references like
`<:zyroxthunder:1448949415200034907>`. Those are Discord custom emoji —
the name is cosmetic, but the numeric ID is what actually resolves the
image, and it almost certainly points to an emoji that lives on the
original bot's application, not yours. **These will likely render as
broken/blank emoji in your server.** You'd need to re-upload the emoji to
your own bot application and swap in the new IDs — I can't do that part
for you since I can't see your Discord app.

---

## Things only you can fill in

| File | What | Value needed |
|---|---|---|
| `env` | `TOKEN=` | Your own bot token |
| `env` | `GROQ_API_KEY=` | Your own Groq key |
| `utils/config.py` | `OWNER_IDS = [0]` | Your Discord user ID (as an int) |
| `cogs/commands/dms.py` | `authorized_staff_ids = []` | Discord IDs of anyone you want able to DM members through the bot |
| Every file with `PASTE_YOUR_OWN_SUPPORT_SERVER_INVITE_HERE` | Support server link | Your own Discord invite, once you have one |
| Every file with `PASTE_YOUR_OWN_BOT_INVITE_URL_HERE` | Bot invite link | Generate from your own application's OAuth2 URL Generator |
| `CodeX.py` (`SERVER_COUNT_CHANNEL_ID`, `USER_COUNT_CHANNEL_ID`, `LOG_CHANNEL_ID`) | Channel IDs | Your own server's channel IDs |

To find every remaining placeholder in one go, search the project for
`PASTE_YOUR_OWN` — I left every spot consistently marked.

### Also on Discord's side, not in the code
- Register your own application at the Developer Portal, name it
  **NEON~V2**, and upload your own avatar/banner there.
- Enable **Message Content**, **Server Members**, and **Presence**
  intents under Bot settings — this codebase relies on all three.
- Re-upload the custom emoji this bot references (see above) to your own
  application, and swap the IDs in the affected files if you want them to
  actually render.
- Invite the bot using your own OAuth2 URL, generated from your own
  application/client ID.

---

## One more thing worth knowing

Given how many independent, hidden bypasses were built into this specific
codebase (eight, across eight different files, not centralized in one
place), I'd treat "won at a giveaway" here with some skepticism about
what else might be worth a second look once you're actually running it —
things like unexpected DMs going out, role changes you didn't make, or
config changes you didn't set. Nothing else turned up in this pass, but
it's a large codebase (190+ files) and I focused on the patterns that
matter most: outbound network calls, hardcoded IDs, and permission
checks. If anything looks off once it's live, send it over and I'll dig
into that specific piece.

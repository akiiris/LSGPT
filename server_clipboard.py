# server_clipboard.py (robust clipboard I/O)
import os, time, tempfile, subprocess
from pathlib import Path

# ---------- OpenAI client (new or classic) ----------
OPENAI_STYLE = None
client = None
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    OPENAI_STYLE = "sdk_new"
except Exception:
    try:
        import openai
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        OPENAI_STYLE = "sdk_old"
    except Exception:
        pass
if OPENAI_STYLE is None:
    raise RuntimeError("Install `openai` and set OPENAI_API_KEY")

# ---------- Settings ----------
BASE_DIR = Path(__file__).parent.resolve()
TRIGGER_FILE = BASE_DIR / ".clip.trigger"
MODEL = "gpt-4o-mini"
POLL_INTERVAL = 0.5
PUT_ERROR_ON_CLIPBOARD = True
DEBUG_LOG = False  # set to True to write .clip.log next to this file
LOGFILE = BASE_DIR / ".clip.log"

def log(msg: str):
    if DEBUG_LOG:
        try:
            with LOGFILE.open("a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception:
            pass

# ---------- Clipboard helpers (robust) ----------
def _ps(cmd: str) -> subprocess.CompletedProcess:
    # Run PowerShell without showing a window
    return subprocess.run(
        ["powershell", "-NoProfile", "-Command", cmd],
        capture_output=True, text=True, creationflags=0x08000000
    )

def get_clipboard_text() -> str:
    """
    Try several ways to get plain text. If the clipboard contains HTML/RTF/bitmap,
    we coerce to text. Returns '' on failure.
    """
    # 1) Raw text
    cp = _ps("Get-Clipboard -Raw")
    if cp.returncode == 0 and cp.stdout:
        return cp.stdout

    # 2) Force text format
    cp = _ps("Get-Clipboard -Format Text -Raw")
    if cp.returncode == 0 and cp.stdout:
        return cp.stdout

    # 3) Last resort: [string](Get-Clipboard)
    cp = _ps("[string](Get-Clipboard)")
    if cp.returncode == 0 and cp.stdout:
        return cp.stdout

    log(f"Get-Clipboard failed: rc={cp.returncode}, err={cp.stderr.strip()}")
    return ""

def set_clipboard_text(text: str) -> None:
    """
    Use two robust methods: PowerShell Set-Clipboard with a here-string,
    and fallback to clip.exe pipe if needed.
    """
    # 1) PowerShell here-string (preserves newlines & UTF-8)
    # Use a unique end marker unlikely to appear in output.
    marker = "__END_HERE_STRING__"
    ps = f"@'\n{text}\n'@ | Set-Clipboard"
    cp = _ps(ps)
    if cp.returncode == 0:
        return

    # 2) Fallback: clip.exe
    try:
        p = subprocess.run(
            "clip",
            input=text,
            text=True,
            capture_output=True,
            creationflags=0x08000000
        )
        if p.returncode == 0:
            return
        log(f"clip.exe failed rc={p.returncode}, err={p.stderr.strip()}")
    except Exception as e:
        log(f"clip.exe exception: {e}")

    # If we got here, we couldn't set the clipboard.
    raise RuntimeError("Failed to set clipboard text")

# ---------- OpenAI ----------
def call_openai(prompt: str) -> str:
    if not (os.environ.get("OPENAI_API_KEY") or "").strip():
        raise RuntimeError("OPENAI_API_KEY is not set.")
    if OPENAI_STYLE == "sdk_new":
        resp = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}]
        )
        return (resp.choices[0].message.content or "").strip()
    else:
        resp = openai.ChatCompletion.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"].strip()

# ---------- Main cycle ----------
def process_once():
    prompt = get_clipboard_text().strip()
    if not prompt:
        if PUT_ERROR_ON_CLIPBOARD:
            try:
                set_clipboard_text("ERROR: Clipboard was empty or non-text. Copy text (Ctrl+C) first.")
            except Exception:
                pass
        return
    try:
        answer = call_openai(prompt)
        if not answer.strip():
            answer = "(Empty response.)"
        set_clipboard_text(answer)
    except Exception as e:
        msg = f"ERROR calling OpenAI: {e}"
        log(msg)
        if PUT_ERROR_ON_CLIPBOARD:
            try:
                set_clipboard_text(msg)
            except Exception:
                pass

def main():
    while True:
        try:
            if TRIGGER_FILE.exists():
                process_once()
                try:
                    TRIGGER_FILE.unlink()
                except Exception:
                    pass
        except Exception as e:
            log(f"Loop error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

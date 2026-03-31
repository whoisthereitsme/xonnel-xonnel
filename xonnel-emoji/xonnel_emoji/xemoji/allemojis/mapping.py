class EmojisMapping:
    MAPPING = {
        # =========================
        # COLORS (RECT)
        # =========================
        "RECT_RED":        "🟥",
        "RECT_ORANGE":     "🟧",
        "RECT_YELLOW":     "🟨",
        "RECT_GREEN":      "🟩",
        "RECT_BLUE":       "🟦",
        "RECT_PURPLE":     "🟪",
        "RECT_BROWN":      "🟫",
        "RECT_BLACK":      "⬛️",
        "RECT_WHITE":      "⬜️",

        # =========================
        # COLORS (CIRC)
        # =========================
        "CIRC_RED":        "🔴",
        "CIRC_ORANGE":     "🟠",
        "CIRC_YELLOW":     "🟡",
        "CIRC_GREEN":      "🟢",
        "CIRC_BLUE":       "🔵",
        "CIRC_PURPLE":     "🟣",
        "CIRC_BROWN":      "🟤",
        "CIRC_BLACK":      "⚫️",
        "CIRC_WHITE":      "⚪️",

        # =========================
        # COLORS (HEART)
        # =========================
        "HEART_RED":       "❤️",
        "HEART_ORANGE":    "🧡",
        "HEART_YELLOW":    "💛",
        "HEART_GREEN":     "💚",
        "HEART_BLUE":      "💙",
        "HEART_PURPLE":    "💜",
        "HEART_BROWN":     "🤎",
        "HEART_BLACK":     "🖤",
        "HEART_WHITE":     "🤍",

        # =========================
        # STATUS
        # =========================
        "PASS":            "✅",
        "FAIL":            "❎",
        "ERROR":           "❌",
        "WARN":            "⚠️",
        "INFO":            "ℹ️",
        "DEBUG":           "🐞",
        "TRACE":           "🔬",
        "UNKNOWN":         "❓",
        "BLOCK":           "⛔️",
        "DENIED":          "🚫",

        
        # =========================
        # CARDINAL
        # =========================
        "COMPASS":          "🧭",
        "MAP":              "🗺️",
        "N":                "⬆️",
        "NE":               "↗️",
        "E":                "➡️",
        "SE":               "↘️",
        "S":                "⬇️",
        "SW":               "↙️",
        "W":                "⬅️",
        "NW":               "↖️",
        "WE":               "↔️",
        "NS":               "↕️",

        # =========================
        # CONTROL
        # =========================
        "PLAY":            "▶️",
        "PAUSE":           "⏸️",
        "STOP":            "⏹️",
        "RECORD":          "⏺️",
        "NEXT":            "⏭️",
        "PREV":            "⏮️",
        "RELOAD":          "🔄",
        "LOOP":            "🔁",
        "SHUFFLE":         "🔀",

        # =========================
        # TIME / PROGRESS
        # =========================
        "TIME":            "⏱️",
        "CLOCK":           "🕒",
        "WAIT":            "⏳",
        "DONE":            "🏁",
        "PROGRESS":        "📊",

        # =========================
        # FILES / IO
        # =========================
        "FILE":            "📄",
        "FILES":           "🗂️",
        "FOLDER":          "📁",
        "OPEN":            "📂",
        "SAVE":            "💾",
        "LOAD":            "📨",
        "EXPORT":          "📤",
        "IMPORT":          "📥",
        "ZIP":             "🗜️",
        "UNZIP":           "📦",
        "LINK":            "⛓️",
        "UNLINK":          "⛓️‍💥",
        "SEARCH":          "🔍",

        # =========================
        # NETWORK
        # =========================
        "NET":             "🌐",
        "WEB":             "🕸️",
        "SERVER":          "🖥️",
        "CLIENT":          "💻",
        "UPLOAD":          "🛫",
        "DOWNLOAD":        "🛬",
        "SOCKET":          "🔌",
        "API":             "🧩",
        "ROUTE":           "🧭",

        # =========================
        # HARDWARE
        # =========================
        "CPU":             "🧠",
        "GPU":             "🖼️",
        "RAM":             "🧮",
        "DISK":            "💽",
        "USB":             "🧷",
        "POWER":           "⚡️",
        "BATTERY":         "🔋",

        # =========================
        # DEV / CODE
        # =========================
        "CODE":            "🧑‍💻",
        "SCRIPT":          "📜",
        "BUG":             "🐛",
        "FIX":             "🛠️",
        "BUILD":           "🏗️",
        "PACKAGE":         "📦",
        "MODULE":          "🧩",
        "CLASS":           "🏷️",
        "FUNC":            "🔧",
        "VAR":             "📌",

        # =========================
        # DATA
        # =========================
        "DATA":            "🗃️",
        "DB":              "🗄️",
        "JSON":            "🧾",
        "XML":             "📰",
        "TREE":            "🌳",
        "STATS":           "📈",

        # =========================
        # SECURITY
        # =========================
        "LOCK":            "🔒",
        "UNLOCK":          "🔓",
        "KEY":             "🔑",
        "SHIELD":          "🛡️",
        "SAFE":            "🔐",

        # =========================
        # SYSTEM / ACTIONS
        # =========================
        "RUN":             "🏃",
        "START":           "🚀",
        "STOPPED":         "🛑",
        "RESTART":         "♻️",
        "CRASH":           "💥",
        "FIRE":            "🔥",

        # =========================
        # LOGGING
        # =========================
        "LOG":             "📝",
        "LOG_INFO":        "📘",
        "LOG_WARN":        "📙",
        "LOG_ERROR":       "📕",
        "LOG_DEBUG":       "📗",

        # =========================
        # THREAD / PROCESS
        # =========================
        "THREAD":          "🧵",
        "PROCESS":         "⚙️",
        "QUEUE":           "🫴",
        "STACK":           "📚",

        # =========================
        # UI / VISUAL
        # =========================
        "EYE":             "👁️",
        "VISIBLE":         "👀",
        "HIDDEN":          "🫥",
        "SPEAK":           "🗣️",
        "MSG":             "💬",
        "THINK":           "💭",

        # =========================
        # SPECIAL / EXTRA
        # =========================
        "MAGIC":           "✨",
        "STAR":            "⭐️",
        "TARGET":          "🎯",
        "FLAG":            "🚩",
        "PIN":             "📍",
        "MARK":            "🔖",

        # =========================
        # CUSTOM
        # =========================
        "XRAY":            "🩻",
        "BLOOD":           "🩸",
        "WATER":           "💧",
        "HOOK":            "🪝",
        "BARREL":          "🛢️",
        "ERUPTION":        "🌋",
        "FUEL":            "⛽️",


        "RADIOACTIVE":     "☢️",
        "BIOHAZARD":       "☣️",

        "SKULL":           "💀",
        "CROSSBONES":      "☠️",
        "BONES":           "🦴",

        

        # =========================
        # RANK MEDALS
        # =========================
        "TROPHY":           "🏆",
        "MEDAL":            "🎖️",   # military medal
        "MEDAL_GOLD":       "🥇",
        "MEDAL_SILVER":     "🥈",
        "MEDAL_BRONZE":     "🥉",

        # =========================
        # STATUS / PROGRESS
        # =========================
        "STAT_UP":           "📈",
        "STAT_DOWN":         "📉",
        "STAT_BARS":         "📊",

        # =========================
        # DEVICES
        # =========================
        "DESKTOP":           "🖥️",
        "LAPTOP":            "💻",
        "TV":                "📺",
        "FRAME":             "🎞️",
        "RADIO":             "📻",
        "MOBILE":            "📱",
        "TABLET":            "📲",
        "HDD":               "💽",

        # =========================
        # PARTS (INDUSTRIAL)
        # =========================
        "GEAR":              "⚙️",
        "NUT":               "🔩",
        "CHAIN":             "⛓️",
        "BATTERY_FULL":      "🔋",
        "BATTERY_LOW":       "🪫",
        "MAGNET":            "🧲",
        "BOLT":              "⚡️",
        "BULB":              "💡",
        

        # =========================
        # PARTS (TOOLS)
        # =========================
        "SCREW":             "🪛",
        "HAMMER":            "🔨",
        "WRENCH":            "🔧",
        "SAW":               "🪚",
        "DRILL":             "🛠️",
        "PAINT":             "🎨",
        "PLUG":              "🔌",
        "SLIDER":            "🎚️",
        "KNOBS":             "🎛️",
    }
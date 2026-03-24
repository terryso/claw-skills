# Claw Skills

Collection of AI agent skills for Claude Code, OpenClaw, and other skill-compatible agents.

[中文文档](README_CN.md)

## Installation

### Option 1: Claude Code Plugin Marketplace (Recommended)

```bash
/plugin marketplace add terryso/claw-skills
/plugin install claw-skills
```

### Option 2: npx skills

```bash
npx skills add terryso/claw-skills
```

### Option 3: Git Submodule

```bash
git submodule add https://github.com/terryso/claw-skills.git .agents/claw-skills
```

### Option 4: Clone & Copy

```bash
git clone https://github.com/terryso/claw-skills.git
cp -r claw-skills/skills/* ~/.claude/skills/
```

## Available Skills

### peekaboo-cli

macOS UI automation CLI tool for screen capture, window control, element clicking, text input, and more.

**Features:**
- Capture screenshots with element annotations
- Click, type, and interact with UI elements
- Manage windows and applications
- Navigate menus and control the dock
- Support for hotkeys and gestures

**Usage:**
```bash
# In Claude Code with skill installed:
"Take a screenshot of the current window"
"Click the Submit button in Safari"
"Open Notes and create a new note"
```

---

### polyv-live-cli

Polyv live streaming service management tool with channel management, streaming operations, product management, coupons, and more.

**Features:**
- Channel management (频道管理)
- Streaming operations (推流操作)
- Product management (商品管理)
- Coupons and lottery (优惠券、抽奖)
- Playback and statistics (回放、统计)

**Usage:**
```bash
# In Claude Code with skill installed:
"List all Polyv channels"
"Create a new live channel"
"Get streaming URL for channel 123456"
```

---

## Why Skills over MCP Server?

| Feature | Skill | MCP Server |
|---------|-------|------------|
| Setup complexity | Simple (copy files) | Moderate (config) |
| **Tools limit** | **No limit** | **IDE has tools quota** |
| Tool access | CLI commands (unlimited) | Structured tools (limited) |
| Flexibility | Full CLI power | Constrained by tool schema |

**Key advantage:** MCP servers are limited by the IDE's maximum number of tools. Skills have no such limitation - they provide comprehensive documentation for unlimited CLI commands while consuming zero tool slots.

For example, `peekaboo-cli` has 35+ commands. If each command were an MCP tool, it would consume significant quota. As a skill, it costs nothing.

---

## Directory Structure

```
claw-skills/
├── README.md
├── README_CN.md
├── LICENSE
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
└── skills/
    ├── peekaboo-cli/
    │   ├── SKILL.md
    │   └── references/
    └── polyv-live-cli/
        ├── SKILL.md
        └── references/
```

## Contributing

Issues and Pull Requests welcome to add new skills.

## License

MIT

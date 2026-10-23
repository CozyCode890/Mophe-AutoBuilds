<div align="center">

# Morphe Custom AutoBuilds (Non-Root)

[![Build](https://img.shields.io/github/actions/workflow/status/CozyCode890/Mophe-AutoBuilds/patch.yml?label=Build&style=for-the-badge&color=2ea44f)](https://github.com/CozyCode890/Mophe-AutoBuilds/actions/workflows/patch.yml)
[![Latest Release](https://img.shields.io/github/v/release/CozyCode890/Mophe-AutoBuilds?style=for-the-badge&label=Latest%20Release&color=0366d6)](https://github.com/CozyCode890/Mophe-AutoBuilds/releases/latest)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/CozyCode890/Mophe-AutoBuilds?style=for-the-badge&color=orange)](LICENSE)

<p align="center">
  <strong>Personal Morphe build pipeline</strong><br>
  arm64-v8a • GitHub Actions • Obtainium
</p>

<p align="center">
A personal fork of <a href="https://github.com/yashrajrocxx/Mophe-AutoBuilds">yashrajrocxx/Mophe-AutoBuilds</a> that builds my own set of patched apps for <strong>non-rooted Android devices</strong> with each patch source's recommended patches, and publishes them for Obtainium.
</p>

</div>

---

## Quick Downloads

> **Note:** The pipeline checks for new patches every 2 days (00:30 UTC) and only rebuilds apps whose patches or app versions changed.

| Mirror | Description | Link |
| :--- | :--- | :--- |
| **GitHub Releases** | Contains all builds. | [**Download Latest Release**](https://github.com/CozyCode890/Mophe-AutoBuilds/releases/latest) |

### Obtainium Auto-Updates & 1-Click Install

This repository provides full first-class integration with [**Obtainium**](https://github.com/ImranR98/Obtainium), allowing you to install and automatically receive daily background updates for any or all apps directly from GitHub Releases with zero manual downloads.

#### Option 1: 1-Click Single App Install
Click the **Add to Obtainium** badge for any app in the catalog below on your Android device (with Obtainium installed). Obtainium will automatically open with the exact repository, APK filter regex, and version extractor preconfigured!

#### Option 2: Bulk Import All Apps
To import the entire curated catalog at once:
1. Open **Obtainium** on your Android device.
2. Tap the **+** button (or navigate to **Import / Export**) $\rightarrow$ select **Import from URL**.
3. Paste the configuration URL:
   ```text
   https://raw.githubusercontent.com/CozyCode890/Mophe-AutoBuilds/main/obtainium.json
   ```
4. Tap **Import**. All apps will be added to your Obtainium database and will automatically track daily releases.

> [!NOTE]
> **User Control & Local State:**
> In Obtainium, importing an app or the `obtainium.json` bundle adds the configuration to your device's local database. It is **not** a forced synchronization—you retain full freedom to install, delete, pause, or pin whichever apps you choose.

### Supported Apps & Patch Repositories

This repository compiles optimized builds using specific community patch repositories for our curated application catalog:

| Application | Package Name | Patch Source | Arch | Obtainium (1-Click) |
| :--- | :--- | :--- | :---: | :---: |
| **atvTools** | `dev.vodik7.atvtools` | hxreborn | `arm64-v8a` | Pending build |
| **Facebook** | `com.facebook.katana` | hushfacebook | `arm64-v8a` | Pending build |
| **Instagram** | `com.instagram.android` | hushgram | `arm64-v8a` | Pending build |
| **Merriam-Webster** | `com.merriamwebster` | hoodles | `arm64-v8a` | Pending build |
| **Messenger** | `com.facebook.orca` | hushmessenger | `arm64-v8a` | Pending build |
| **Threads** | `com.instagram.barcelona` | hushthreads | `arm64-v8a` | Pending build |
| **TikTok** | `com.zhiliaoapp.musically` | hushfeed | `arm64-v8a` | Pending build |
| **Waze** | `com.waze` | bearinmind | `arm64-v8a` | Pending build |
| **YouTube** | `com.google.android.youtube` | morphe | `arm64-v8a` | Pending build |
| **Zalo** | `com.zing.zalo` | zeldris | `arm64-v8a` | Pending build |

*(All builds are target-optimized for their respective architectures to reduce bundle sizes and increase device efficiency).*

---

## Patch Sources

Every app is built with its source's default (recommended) patch selection, on the newest app version that source supports.

| Application | Source id | Patch repository |
| :--- | :--- | :--- |
| YouTube | `morphe` | [MorpheApp/morphe-patches](https://github.com/MorpheApp/morphe-patches) |
| atvTools | `hxreborn` | [hxreborn/morphe-patches](https://github.com/hxreborn/morphe-patches) |
| Facebook | `hushfacebook` | [SysAdminDoc/HushFacebook](https://github.com/SysAdminDoc/HushFacebook) |
| Merriam-Webster | `hoodles` | [hoo-dles/morphe-patches](https://github.com/hoo-dles/morphe-patches) |
| Messenger | `hushmessenger` | [SysAdminDoc/HushMessenger](https://github.com/SysAdminDoc/HushMessenger) |
| TikTok | `hushfeed` | [SysAdminDoc/HushFeed](https://github.com/SysAdminDoc/HushFeed) |
| Waze | `bearinmind` | [bearinmindcat/morphe-patches](https://github.com/bearinmindcat/morphe-patches) |
| Zalo | `zeldris` | [zeldrisho/morphe-patches](https://github.com/zeldrisho/morphe-patches) |
| Instagram | `hushgram` | [SysAdminDoc/HushGram](https://github.com/SysAdminDoc/HushGram) |
| Threads | `hushthreads` | [SysAdminDoc/HushThreads](https://github.com/SysAdminDoc/HushThreads) |

All patching is done with [MorpheApp/morphe-cli](https://github.com/MorpheApp/morphe-cli).

---

## GitHub Setup

1. **Actions:** enable workflows in the **Actions** tab of the fork.
2. **Pages:** *Settings → Pages → Source: GitHub Actions*. Obtainium tracks `https://cozycode890.github.io/Mophe-AutoBuilds/downloads.html`, so Pages must be deployed.
3. **Secrets** (*Settings → Secrets and variables → Actions*):

| Secret | Needed | Purpose |
| :--- | :--- | :--- |
| `GPLAYDL_TOKEN` | Strongly recommended | [gplaydl](https://pypi.org/project/gplaydl/) API key for Google Play downloads. APKMirror and the other scrapers are often blocked on GitHub runners. |
| `KEYSTORE_BASE64` | Recommended | Base64 of a PKCS12/JKS keystore used to sign every APK (e.g. converted from Morphe Manager's `Morphe.keystore`). Without it the public `keystore/public.jks` is used. |
| `KEYSTORE_PASSWORD` | With a keystore | Keystore password. |
| `KEY_ALIAS` | Optional | Key alias; required when the keystore holds more than one key. |
| `KEY_PASSWORD` | Optional | Key password, when it differs from the keystore password. |
| `CUSTOM_GH_TOKEN` | Optional | Personal access token with a higher GitHub API rate limit. |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Optional | Telegram build reports. |

> [!IMPORTANT]
> Android only installs an update over an existing app when both are signed with the same key. Set the keystore secrets **before** installing anything from this repository. If the key changes later, run **Auto Build and Release Morphe** with *force_full_rebuild* so every APK is re-signed.

---

## Repository Structure

```text
Mophe-AutoBuilds/
├── .github/workflows/      # GitHub Actions automation
│   ├── patch.yml           # Scheduled incremental builds (every 2 days, 00:30 UTC)
│   └── manual-patch.yml    # Manual single-app build
├── apps/                   # APK download source configurations
├── patches/                # Patch inclusion/exclusion rules
├── sources/                # Patch source definitions (CLI + patch bundle)
├── src/                    # Core Python build logic
├── arch-config.json        # Architecture build matrix
├── patch-config.json       # Apps built by the pipeline
└── requirements.txt        # Project dependencies
```

---

## Configuration Guide

### 1. App Selection (`patch-config.json`)

Define which applications the pipeline builds, and with which patch source.

```json
{
  "patch_list": [
    { "app_name": "youtube", "source": "morphe" },
    { "app_name": "zalo", "source": "zeldris" }
  ]
}
```

### 2. Architecture Matrix (`arch-config.json`)

Specify which CPU architectures to target for each application. Every app here targets `arm64-v8a`.

### 3. Download Sources

Located in the `apps/` directory, one folder per download site (`playstore`, `apkmirror`, `apkpure`, `uptodown`, `apkcombo`, ...).

### 4. Patch Rules

Located in `patches/`, named `<app>-<source>.txt`. Use `+` to force include and `-` to exclude a patch; an empty file keeps the source's recommended selection.

```text
# Essential patches
+ GmsCore support

# Exclusions
- Custom branding
```

---

## Local Build Instructions

### Prerequisites

* Python 3.11 or higher
* Java Runtime Environment (JRE) 21+
* `zip` utility
* `apksigner` and `zipalign` (Android SDK Build-Tools)

### Installation & Execution

1. **Clone the repository:**
```bash
git clone https://github.com/CozyCode890/Mophe-AutoBuilds.git
cd Mophe-AutoBuilds
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the build** for a specific app and source:
```bash
export APP_NAME="youtube"
export SOURCE="morphe"
python -m src
```

---

## GitHub Actions Workflows

### Scheduled Build (`patch.yml`)
* **Schedule:** Every 2 days at 00:30 UTC, or manually from the Actions tab.
* **Function:** Rebuilds only the apps whose patch source or app version changed (*force_full_rebuild* rebuilds everything).
* **Output:** Updates the single `latest` release, `obtainium.json`, this README and the Pages site.

### Manual Build (`manual-patch.yml`)
* **Trigger:** Manually via the GitHub Actions "Run workflow" button.
* **Capabilities:** Build one app, optionally forcing a specific APK version (`arm64-v8a`).

---

## Disclaimer & Legal

> **Important:** This project is an automated build tool. The APKs provided in the releases are generated automatically using official and community Morphe tools and patches.

* **Affiliation:** These builds are **not** officially affiliated with the original developers or the Morphe Team.
* **Usage:** Provided for educational and convenience purposes only. Use at your own risk.
* **GmsCore:** Morphe's MicroG-RE is required for apps relying on Google services to function correctly.
* **Updates:** Patches are automatically pulled from the latest custom sources; builds may occasionally contain experimental features.

---

<div align="center">

Based on [Mophe-AutoBuilds](https://github.com/yashrajrocxx/Mophe-AutoBuilds) by RookieZ & Yashrajrocxx.

</div>

# 🎮 Minecraft Universal Offline Build Cache & Environments (1.8.x - 26.x)

<p align="center">
  <b>100% Offline Modding Workspaces &amp; Pre-cached Dependencies for Fabric &amp; Forge</b><br>
  <i>Designed for Gemini Web, Sandboxed Cloud Containers, Air-gapped Machines, and Fast Local Modding.</i>
</p>

<p align="center">
  <a href="#-english">🇬🇧 English</a> •
  <a href="#-tiếng-việt">🇻🇳 Tiếng Việt</a> •
  <a href="#-日本語">🇯🇵 日本語</a> •
  <a href="#-简体中文">🇨🇳 简体中文</a> •
  <a href="#-desktop-app-downloader-windows-x64">🖥️ Downloader App</a> •
  <a href="#-releases-catalog-82-versions">📦 Releases</a>
</p>

<p align="center">
  <a href="https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/download/v1.0.0-downloader/MinecraftCacheDownloader.exe">
    <img src="https://img.shields.io/badge/Download-MinecraftCacheDownloader.exe_(Windows_x64)-2ea043?style=for-the-badge&logo=windows&logoColor=white" alt="Download Standalone Exe" />
  </a>
</p>

---

## 🇬🇧 ENGLISH

Hey everyone! 👋

If you have ever developed Minecraft mods, you know the struggle: every time you create a new project or run `./gradlew build`, Gradle takes forever downloading gigabytes of dependencies, MCP configs, mappings, and Mojang vanilla assets from remote servers. When you need to build or test mods inside **Gemini Web**, air-gapped workstations, or restricted sandbox environments with zero internet access, regular builds fail immediately.

This repository completely solves that problem! We provide **100% offline, pre-cached modding workspaces** covering **82 major Minecraft versions from 1.8.x all the way up to 26.x**, strictly for **Forge** and **Fabric** (absolutely NO NeoForge). Everything has been compiled, cached, verified offline, and packaged directly on cloud runners.

### ✨ Key Highlights:
1. **Forge & Fabric Exclusively:** Full support for classic versions (1.8.9, 1.12.2) up to bleeding-edge releases (1.21.11, 26.3).
2. **Dual Packaging Options:**
   - **All-in-One ZIP (`*_Offline_GeminiWeb.zip`):** 1-click download containing the sample mod project, complete Gradle cache, and matching JDK.
   - **Sliced Chunks $\le 94\text{ MB}$:** Sized specifically so you can drag-and-drop them straight into Gemini Web without hitting Google's 100 MB upload limit.
3. **Bundled Linux x64 JDKs:** Adoptium Temurin OpenJDK (8, 16, 17, 21) and Oracle JDK 25 for Forge 26.x — no separate Java installation needed.
4. **Integrity Guaranteed:** Every release includes `INSTRUCTIONS_MULTILINGUAL.txt` with SHA256 hashes and 1-click bash commands.

### ⚡ 1-Click Quickstart (Linux / Gemini Web):
```bash
# 1. Unpack all zip archives
unzip -o "*.zip"

# 2. Reassemble chunked archives
cat jdk*.tar.gz.part* > jdk_bundle.tar.gz
cat *offline_cache.tar.gz.part* > offline_cache.tar.gz

# 3. Setup JDK environment
mkdir -p $HOME/jdk && tar -xzf jdk_bundle.tar.gz -C $HOME/jdk --strip-components=1
export JAVA_HOME=$HOME/jdk
export PATH=$JAVA_HOME/bin:$PATH

# 4. Extract project and pre-cached Gradle dependencies
tar -xzf offline_cache.tar.gz -C $HOME/

# 5. Build completely offline!
cd $HOME/*-*/
chmod +x gradlew
./gradlew clean build --offline
```

---

## 🇻🇳 TIẾNG VIỆT

Chào mọi người! 👋

Nếu bạn từng làm mod Minecraft, chắc chắn bạn không lạ gì cảnh mỗi lần khởi tạo project mới hay chạy `./gradlew build` là Gradle lại tốn cả chục phút kéo hàng nghìn file dependencies, thư viện MCP, mappings, assets... từ server Mojang và Forge về máy. Đặc biệt là khi bạn chạy code trong **Gemini Web**, môi trường container sandbox bị chặn mạng, máy tính offline không có internet, hay mạng quốc tế chập chờn chặn các kho Maven nước ngoài, thì việc build mod gần như là bất khả thi.

Dự án này sinh ra để giải quyết triệt để vấn đề đó! Toàn bộ 82 phiên bản Minecraft phổ biến nhất từ **1.8.x cho đến tận 26.x** đều đã được mình build thử nghiệm, trích xuất sạch sẽ toàn bộ cache và đóng gói sẵn sàng để bạn **chạy build offline 100% chỉ trong vài giây**.

### 💡 Điểm đặc biệt của bộ cache:
1. **Chỉ tập trung vào Fabric & Forge (Tuyệt đối không dùng NeoForge):** Tương thích chuẩn xác với các modder truyền thống và hiện đại.
2. **Hai cách tải linh hoạt:**
   - **File ZIP All-in-One (`*_Offline_GeminiWeb.zip`):** Tải 1 lần duy nhất chứa đầy đủ project + cache + bộ cài JDK tương ứng.
   - **Các part cắt nhỏ $\le 94\text{ MB}$:** Thoải mái kéo thả trực tiếp từng part vào Gemini Web mà không bao giờ bị giới hạn upload 100 MB của Google từ chối.
3. **Kèm sẵn JDK Linux x64:** Adoptium Temurin (Java 8, 16, 17, 21) và Oracle JDK 25 (cho các bản Forge 26.x tương lai) — giải nén là chạy, không cần cài Java ngoài.
4. **Hướng dẫn đa ngôn ngữ & Checksum SHA256:** Mỗi bản release đều có file `INSTRUCTIONS_MULTILINGUAL.txt` kèm mã hash SHA256 để đảm bảo file nguyên vẹn không bị lỗi khi ghép.

### 🚀 Lệnh 1-Click chạy ngay trong Linux / Gemini Web:
```bash
# 1. Giải nén tất cả file zip đã tải về
unzip -o "*.zip"

# 2. Ghép nối các part lại thành file nén gốc
cat jdk*.tar.gz.part* > jdk_bundle.tar.gz
cat *offline_cache.tar.gz.part* > offline_cache.tar.gz

# 3. Cấu hình biến môi trường Java
mkdir -p $HOME/jdk && tar -xzf jdk_bundle.tar.gz -C $HOME/jdk --strip-components=1
export JAVA_HOME=$HOME/jdk
export PATH=$JAVA_HOME/bin:$PATH

# 4. Bung cache và project vào thư mục HOME
tar -xzf offline_cache.tar.gz -C $HOME/

# 5. Build offline ngay lập tức!
cd $HOME/*-*/
chmod +x gradlew
./gradlew clean build --offline
```

---

## 🇯🇵 日本語

Minecraft 開発者の皆さん、こんにちは！👋

MOD開発を始める際、Gradleが大量の依存ライブラリやMCPマッピング、バニラjarを延々とダウンロードするのに時間を取られた経験はありませんか？特に **Gemini Web** やオフライン環境、ネットワーク制限のあるクラウドコンテナでは、外部Mavenサーバーに接続できずビルドが失敗してしまいます。

このリポジトリは、**1.8.x から最新の 26.x まで** の主要な Minecraft バージョン（**Forge** および **Fabric** 限定、NeoForgeなし）を対象に、**完全オフラインで即座にビルド可能なキャッシュ環境（全82バージョン）** を提供します。

### 🌟 主な特徴：
1. **Forge と Fabric に完全特化:** 1.8.9 や 1.12.2 などのレガシーから、最新の 1.21.11 や 26.3 まで網羅。
2. **選べる2つの配布形式:**
   - **オールインワンZIP (`*_Offline_GeminiWeb.zip`):** ワンクリックでプロジェクト、全キャッシュ、JDKを一括ダウンロード。
   - **分割ZIP（各 $\le 94\text{ MB}$）:** Gemini Web の 100 MB アップロード制限に引っかからず、そのままドラッグ＆ドロップ可能。
3. **Linux x64 JDK同梱:** Temurin 8, 16, 17, 21 および Forge 26.x 向けの Oracle JDK 25 をセットアップ済み。
4. **安心の整合性検証:** すべてのリリースに4言語解説書と SHA256 チェックサムを添付。

### ⚡ 1クリック簡単セットアップ（Linux / Gemini Web）：
```bash
# 1. すべての zip アーカイブを展開
unzip -o "*.zip"

# 2. 分割ファイルを結合
cat jdk*.tar.gz.part* > jdk_bundle.tar.gz
cat *offline_cache.tar.gz.part* > offline_cache.tar.gz

# 3. JDK のセットアップ
mkdir -p $HOME/jdk && tar -xzf jdk_bundle.tar.gz -C $HOME/jdk --strip-components=1
export JAVA_HOME=$HOME/jdk
export PATH=$JAVA_HOME/bin:$PATH

# 4. プロジェクトとキャッシュを展開
tar -xzf offline_cache.tar.gz -C $HOME/

# 5. 完全オフラインでビルド開始！
cd $HOME/*-*/
chmod +x gradlew
./gradlew clean build --offline
```

---

## 🇨🇳 简体中文

各位 Minecraft 模组开发者与玩家，大家好！👋

在进行模组开发时，每次初始化项目或执行 `./gradlew build`，Gradle 往往需要从外网下载数以千计的依赖项、MCP 映射表与游戏资源，耗时漫长且极易因网络超时而失败。尤其是在 **Gemini Web**、离线沙箱、内网机房或网络受限的环境中，完全无法直接拉取 Maven 仓库。

本项目为你彻底解决了这个痛点！涵盖 **Minecraft 1.8.x 至 26.x 的全系 82 个版本**（**仅限 Forge 与 Fabric**，严格剔除 NeoForge）。所有环境均已在云端完成离线构建测试，开箱即用。

### 📌 核心优势：
1. **纯粹的 Forge 与 Fabric 支持:** 覆盖从 1.8.9、1.12.2 经典版本到 1.21.11 与 26.3 前沿版本。
2. **贴心的打包标准:**
   - **整合包 ZIP (`*_Offline_GeminiWeb.zip`):** 一键下载，内含模板工程、完整 Gradle 缓存与对应 JDK。
   - **切片分卷包（$\le 94\text{ MB}$）:** 完美适配 Gemini Web 网页端单文件 100 MB 的上传上限，直接拖拽上传无报错。
3. **预装 Linux x64 JDK 环境:** 附带 Temurin OpenJDK 8 / 16 / 17 / 21 及针对 26.x 的 Oracle JDK 25，解压即配好环境。
4. **SHA256 校验与多语言文档:** 每个 Release 均内置 4 语种详细指南 `INSTRUCTIONS_MULTILINGUAL.txt`。

### ⚡ 终端极速上手指令（Linux / Gemini Web）：
```bash
# 1. 解压所有已上传的 zip 压缩包
unzip -o "*.zip"

# 2. 合并分卷压缩文件
cat jdk*.tar.gz.part* > jdk_bundle.tar.gz
cat *offline_cache.tar.gz.part* > offline_cache.tar.gz

# 3. 部署并配置 Java JDK 环境
mkdir -p $HOME/jdk && tar -xzf jdk_bundle.tar.gz -C $HOME/jdk --strip-components=1
export JAVA_HOME=$HOME/jdk
export PATH=$JAVA_HOME/bin:$PATH

# 4. 解压预缓存工程与 Gradle 依赖库到 HOME 目录
tar -xzf offline_cache.tar.gz -C $HOME/

# 5. 即刻享受 100% 纯离线极速编译！
cd $HOME/*-*/
chmod +x gradlew
./gradlew clean build --offline
```

---

## 🖥️ DESKTOP APP DOWNLOADER (WINDOWS x64)

For Windows users who want an effortless way to browse and download these offline packages, we created an open-source desktop GUI tool built with **WPF + C# on .NET 10** (`MinecraftCacheDownloader.exe`), compiled as a **single standalone file (Self-Contained)** that runs immediately on any Windows 64-bit PC without installing .NET:

- 🌐 **Dynamic Online Catalog Sync:** The app connects directly to [`catalog.json`](catalog.json) in this repository. Whenever new versions or loaders are added in the future, the app automatically detects and displays them without requiring you to rebuild or download a new `.exe`!
- 🚀 **1 Single Standalone `.exe`:** No .NET runtime installation required — everything is bundled inside a single portable binary (~61 MB).
- 🔍 **Smart ZIP Integrity Validation:** Automatically scans the `data/` folder before downloading to test existing ZIP archives (`ZipFile.OpenRead`). It skips valid files to prevent duplicate downloads and flags broken or incomplete downloads.
- 📊 **Real-time Live Metrics:** Displays a smooth progress bar, current file size (`MB / GB`), real-time download speed (`KB/s`, `MB/s`, `GB/s`), elapsed time, and dynamic ETA.
- 📥 **Batch Queue Downloads:** Select individual versions or click "Select All" to download in batch queue with a single click.
- 📂 **Auto-Organized Storage:** Automatically saves and organizes all downloaded archives into a `data/` folder right next to the `.exe`.

<p align="center">
  <a href="https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.0.0-downloader"><b>📦 View Official App Release</b></a> •
  <a href="https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/download/v1.0.0-downloader/MinecraftCacheDownloader.exe"><b>⚡ Direct Download (MinecraftCacheDownloader.exe)</b></a>
</p>

---

## 📦 RELEASES CATALOG (82 VERSIONS)

### 🧵 Fabric Releases (44 Versions)

| # | Version | Loader | JDK | Direct Release Link | Status |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | **Fabric 1.8.9** | Fabric | Java 8 | [v1.8.9-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.8.9-fabric) | ✅ 100% Offline |
| 2 | **Fabric 1.9.4** | Fabric | Java 8 | [v1.9.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.9.4-fabric) | ✅ 100% Offline |
| 3 | **Fabric 1.10.2** | Fabric | Java 8 | [v1.10.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.10.2-fabric) | ✅ 100% Offline |
| 4 | **Fabric 1.11.2** | Fabric | Java 8 | [v1.11.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.11.2-fabric) | ✅ 100% Offline |
| 5 | **Fabric 1.12.2** | Fabric | Java 8 | [v1.12.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.12.2-fabric) | ✅ 100% Offline |
| 6 | **Fabric 1.13.2** | Fabric | Java 8 | [v1.13.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.13.2-fabric) | ✅ 100% Offline |
| 7 | **Fabric 1.14.3** | Fabric | Java 8 | [v1.14.3-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.14.3-fabric) | ✅ 100% Offline |
| 8 | **Fabric 1.14.4** | Fabric | Java 8 | [v1.14.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.14.4-fabric) | ✅ 100% Offline |
| 9 | **Fabric 1.15.1** | Fabric | Java 8 | [v1.15.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.15.1-fabric) | ✅ 100% Offline |
| 10 | **Fabric 1.15.2** | Fabric | Java 8 | [v1.15.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.15.2-fabric) | ✅ 100% Offline |
| 11 | **Fabric 1.16.1** | Fabric | Java 8 | [v1.16.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.1-fabric) | ✅ 100% Offline |
| 12 | **Fabric 1.16.2** | Fabric | Java 8 | [v1.16.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.2-fabric) | ✅ 100% Offline |
| 13 | **Fabric 1.16.3** | Fabric | Java 8 | [v1.16.3-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.3-fabric) | ✅ 100% Offline |
| 14 | **Fabric 1.16.4** | Fabric | Java 8 | [v1.16.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.4-fabric) | ✅ 100% Offline |
| 15 | **Fabric 1.16.5** | Fabric | Java 8 | [v1.16.5-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.5-fabric) | ✅ 100% Offline |
| 16 | **Fabric 1.17** | Fabric | Java 16 | [v1.17-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.17-fabric) | ✅ 100% Offline |
| 17 | **Fabric 1.17.1** | Fabric | Java 16 | [v1.17.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.17.1-fabric) | ✅ 100% Offline |
| 18 | **Fabric 1.18** | Fabric | Java 17 | [v1.18-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.18-fabric) | ✅ 100% Offline |
| 19 | **Fabric 1.18.1** | Fabric | Java 17 | [v1.18.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.18.1-fabric) | ✅ 100% Offline |
| 20 | **Fabric 1.18.2** | Fabric | Java 17 | [v1.18.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.18.2-fabric) | ✅ 100% Offline |
| 21 | **Fabric 1.19** | Fabric | Java 17 | [v1.19-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19-fabric) | ✅ 100% Offline |
| 22 | **Fabric 1.19.1** | Fabric | Java 17 | [v1.19.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.1-fabric) | ✅ 100% Offline |
| 23 | **Fabric 1.19.2** | Fabric | Java 17 | [v1.19.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.2-fabric) | ✅ 100% Offline |
| 24 | **Fabric 1.19.3** | Fabric | Java 17 | [v1.19.3-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.3-fabric) | ✅ 100% Offline |
| 25 | **Fabric 1.19.4** | Fabric | Java 17 | [v1.19.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.4-fabric) | ✅ 100% Offline |
| 26 | **Fabric 1.20** | Fabric | Java 17 | [v1.20-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20-fabric) | ✅ 100% Offline |
| 27 | **Fabric 1.20.1** | Fabric | Java 17 | [v1.20.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.1-fabric) | ✅ 100% Offline |
| 28 | **Fabric 1.20.2** | Fabric | Java 17 | [v1.20.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.2-fabric) | ✅ 100% Offline |
| 29 | **Fabric 1.20.3** | Fabric | Java 17 | [v1.20.3-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.3-fabric) | ✅ 100% Offline |
| 30 | **Fabric 1.20.4** | Fabric | Java 17 | [v1.20.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.4-fabric) | ✅ 100% Offline |
| 31 | **Fabric 1.20.5** | Fabric | Java 17 | [v1.20.5-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.5-fabric) | ✅ 100% Offline |
| 32 | **Fabric 1.20.6** | Fabric | Java 17 | [v1.20.6-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.6-fabric) | ✅ 100% Offline |
| 33 | **Fabric 1.21** | Fabric | Java 21 | [v1.21-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21-fabric) | ✅ 100% Offline |
| 34 | **Fabric 1.21.1** | Fabric | Java 21 | [v1.21.1-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.1-fabric) | ✅ 100% Offline |
| 35 | **Fabric 1.21.2** | Fabric | Java 21 | [v1.21.2-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.2-fabric) | ✅ 100% Offline |
| 36 | **Fabric 1.21.3** | Fabric | Java 21 | [v1.21.3-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.3-fabric) | ✅ 100% Offline |
| 37 | **Fabric 1.21.4** | Fabric | Java 21 | [v1.21.4-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.4-fabric) | ✅ 100% Offline |
| 38 | **Fabric 1.21.5** | Fabric | Java 21 | [v1.21.5-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.5-fabric) | ✅ 100% Offline |
| 39 | **Fabric 1.21.6** | Fabric | Java 21 | [v1.21.6-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.6-fabric) | ✅ 100% Offline |
| 40 | **Fabric 1.21.7** | Fabric | Java 21 | [v1.21.7-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.7-fabric) | ✅ 100% Offline |
| 41 | **Fabric 1.21.8** | Fabric | Java 21 | [v1.21.8-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.8-fabric) | ✅ 100% Offline |
| 42 | **Fabric 1.21.9** | Fabric | Java 21 | [v1.21.9-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.9-fabric) | ✅ 100% Offline |
| 43 | **Fabric 1.21.10** | Fabric | Java 21 | [v1.21.10-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.10-fabric) | ✅ 100% Offline |
| 44 | **Fabric 1.21.11** | Fabric | Java 21 | [v1.21.11-fabric](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.11-fabric) | ✅ 100% Offline |

### 🔨 Forge Releases (38 Versions)

| # | Version | Loader | JDK | Direct Release Link | Status |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | **Forge 1.8.9** | Forge | Java 8 | [v1.8.9-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.8.9-forge) | ✅ 100% Offline |
| 2 | **Forge 1.12.2** | Forge | Java 8 | [v1.12.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.12.2-forge) | ✅ 100% Offline |
| 3 | **Forge 1.14.4** | Forge | Java 8 | [v1.14.4-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.14.4-forge) | ✅ 100% Offline |
| 4 | **Forge 1.15.1** | Forge | Java 8 | [v1.15.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.15.1-forge) | ✅ 100% Offline |
| 5 | **Forge 1.15.2** | Forge | Java 8 | [v1.15.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.15.2-forge) | ✅ 100% Offline |
| 6 | **Forge 1.16.1** | Forge | Java 8 | [v1.16.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.1-forge) | ✅ 100% Offline |
| 7 | **Forge 1.16.2** | Forge | Java 8 | [v1.16.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.2-forge) | ✅ 100% Offline |
| 8 | **Forge 1.16.3** | Forge | Java 8 | [v1.16.3-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.3-forge) | ✅ 100% Offline |
| 9 | **Forge 1.16.4** | Forge | Java 8 | [v1.16.4-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.4-forge) | ✅ 100% Offline |
| 10 | **Forge 1.16.5** | Forge | Java 8 | [v1.16.5-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.16.5-forge) | ✅ 100% Offline |
| 11 | **Forge 1.17.1** | Forge | Java 16 | [v1.17.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.17.1-forge) | ✅ 100% Offline |
| 12 | **Forge 1.18.1** | Forge | Java 17 | [v1.18.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.18.1-forge) | ✅ 100% Offline |
| 13 | **Forge 1.18.2** | Forge | Java 17 | [v1.18.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.18.2-forge) | ✅ 100% Offline |
| 14 | **Forge 1.19.1** | Forge | Java 17 | [v1.19.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.1-forge) | ✅ 100% Offline |
| 15 | **Forge 1.19.2** | Forge | Java 17 | [v1.19.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.2-forge) | ✅ 100% Offline |
| 16 | **Forge 1.19.3** | Forge | Java 17 | [v1.19.3-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.3-forge) | ✅ 100% Offline |
| 17 | **Forge 1.19.4** | Forge | Java 17 | [v1.19.4-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.19.4-forge) | ✅ 100% Offline |
| 18 | **Forge 1.20.1** | Forge | Java 17 | [v1.20.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.1-forge) | ✅ 100% Offline |
| 19 | **Forge 1.20.2** | Forge | Java 17 | [v1.20.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.2-forge) | ✅ 100% Offline |
| 20 | **Forge 1.20.3** | Forge | Java 17 | [v1.20.3-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.3-forge) | ✅ 100% Offline |
| 21 | **Forge 1.20.4** | Forge | Java 17 | [v1.20.4-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.4-forge) | ✅ 100% Offline |
| 22 | **Forge 1.20.6** | Forge | Java 17 | [v1.20.6-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.20.6-forge) | ✅ 100% Offline |
| 23 | **Forge 1.21** | Forge | Java 21 | [v1.21-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21-forge) | ✅ 100% Offline |
| 24 | **Forge 1.21.1** | Forge | Java 21 | [v1.21.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.1-forge) | ✅ 100% Offline |
| 25 | **Forge 1.21.3** | Forge | Java 21 | [v1.21.3-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.3-forge) | ✅ 100% Offline |
| 26 | **Forge 1.21.4** | Forge | Java 21 | [v1.21.4-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.4-forge) | ✅ 100% Offline |
| 27 | **Forge 1.21.5** | Forge | Java 21 | [v1.21.5-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.5-forge) | ✅ 100% Offline |
| 28 | **Forge 1.21.6** | Forge | Java 21 | [v1.21.6-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.6-forge) | ✅ 100% Offline |
| 29 | **Forge 1.21.7** | Forge | Java 21 | [v1.21.7-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.7-forge) | ✅ 100% Offline |
| 30 | **Forge 1.21.8** | Forge | Java 21 | [v1.21.8-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.8-forge) | ✅ 100% Offline |
| 31 | **Forge 1.21.9** | Forge | Java 21 | [v1.21.9-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.9-forge) | ✅ 100% Offline |
| 32 | **Forge 1.21.10** | Forge | Java 21 | [v1.21.10-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.10-forge) | ✅ 100% Offline |
| 33 | **Forge 1.21.11** | Forge | Java 21 | [v1.21.11-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.11-forge) | ✅ 100% Offline |
| 34 | **Forge 26.1** | Forge | Java 25 (Oracle) | [v26.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v26.1-forge) | ✅ 100% Offline |
| 35 | **Forge 26.1.1** | Forge | Java 25 (Oracle) | [v26.1.1-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v26.1.1-forge) | ✅ 100% Offline |
| 36 | **Forge 26.1.2** | Forge | Java 25 (Oracle) | [v26.1.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v26.1.2-forge) | ✅ 100% Offline |
| 37 | **Forge 26.2** | Forge | Java 25 (Oracle) | [v26.2-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v26.2-forge) | ✅ 100% Offline |
| 38 | **Forge 26.3** | Forge | Java 25 (Oracle) | [v26.3-forge](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v26.3-forge) | ✅ 100% Offline |

### 📜 Paper Releases (PaperMC Plugin Workspace)

| # | Version | Loader | JDK | Direct Release Link | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| 1 | **Paper 1.21.11** | Paper | Java 21 | [v1.21.11-paper](https://github.com/nuhuh-ahh/minecraft-offline-cache/releases/tag/v1.21.11-paper) | ✅ 100% Offline |

---

## ⚖️ Copyright & License

- **Project Creator & Lead Developer:** **AkumiYuukii** (Discord: `hellnah._.whyy`)
- **License:** [LICENSE](LICENSE) • [COPYRIGHT NOTICE](COPYRIGHT.md)
- Copyright © 2026 **AkumiYuukii**. All rights reserved.

All companion downloader applications, automation pipelines, packaging scripts, and repository layouts are authored and maintained by **AkumiYuukii** (Discord: `hellnah._.whyy`).

*Disclaimer: Minecraft is a registered trademark of Mojang Synergies AB / Microsoft Corporation. This project is an independent community development tool.*

---

<p align="center">
  <i>Crafted with ❤️ by AkumiYuukii for the global Minecraft modding community. Happy offline coding!</i>
</p>

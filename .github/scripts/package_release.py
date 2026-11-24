import os
import sys
import argparse
import hashlib
import zipfile
import tarfile
import shutil
import urllib.request

CHUNK_SIZE = 94 * 1024 * 1024  # 94 MB

JDK_URLS = {
    '8': 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u512-b09/OpenJDK8U-jdk_x64_linux_hotspot_8u512b09.tar.gz',
    '16': 'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_linux_hotspot_16.0.2_7.tar.gz',
    '17': 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.14%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.14_7.tar.gz',
    '21': 'https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.6%2B7/OpenJDK21U-jdk_x64_linux_hotspot_21.0.6_7.tar.gz',
    '25': 'https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.tar.gz'
}

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def filter_tar(tarinfo):
    if tarinfo.isdir() or tarinfo.name.endswith('gradlew') or '/bin/gradle' in tarinfo.name:
        tarinfo.mode = 0o755
    else:
        tarinfo.mode = 0o644
    tarinfo.uid = 1000
    tarinfo.gid = 1000
    tarinfo.uname = 'ubuntu'
    tarinfo.gname = 'ubuntu'
    return tarinfo

def main():
    parser = argparse.ArgumentParser(description='Universal Minecraft Cache Packager for Gemini Web')
    parser.add_argument('--loader', required=True, choices=['Fabric', 'Forge', 'Paper'], help='Mod loader')
    parser.add_argument('--mc-version', required=True, help='Minecraft version, e.g. 1.9.4')
    parser.add_argument('--java-version', required=True, choices=['8', '16', '17', '21', '25'], help='Java version')
    parser.add_argument('--project-dir', required=True, help='Path to project template directory')
    parser.add_argument('--dist-dir', default='dist', help='Output distribution directory')

    args = parser.parse_args()

    loader = args.loader
    loader_lower = loader.lower()
    mc_ver = args.mc_version
    clean_ver = mc_ver.replace('.', '')
    java_ver = args.java_version
    project_dir = os.path.abspath(args.project_dir)
    dist_dir = os.path.abspath(args.dist_dir)
    home = os.path.expanduser('~')

    os.makedirs(dist_dir, exist_ok=True)

    print(f'=== Starting Packaging for {loader} {mc_ver} (Java {java_ver}) ===')

    # 1. Archive Project & Gradle Cache
    cache_tar_name = f'{loader_lower}_{clean_ver}_offline_cache.tar.gz'
    cache_tar_path = os.path.join(dist_dir, cache_tar_name)
    print(f'Creating archive {cache_tar_path}...')

    with tarfile.open(cache_tar_path, 'w:gz') as tar:
        # Project files
        print(f'Adding project files from {project_dir}...')
        def project_filter(tarinfo):
            if any(x in tarinfo.name for x in ['/.git', '/dist', '/build/reports']):
                return None
            return filter_tar(tarinfo)

        target_arcname = f'{loader_lower}-{mc_ver}'
        tar.add(project_dir, arcname=target_arcname, filter=project_filter)

        # ~/.gradle/wrapper
        wrapper_path = os.path.join(home, '.gradle', 'wrapper', 'dists')
        if os.path.exists(wrapper_path):
            print('Adding .gradle/wrapper/dists...')
            tar.add(wrapper_path, arcname='.gradle/wrapper/dists', filter=filter_tar)

        # ~/.gradle/caches
        caches_dir = os.path.join(home, '.gradle', 'caches')
        if os.path.exists(caches_dir):
            for item in os.listdir(caches_dir):
                p = os.path.join(caches_dir, item)
                arc = f'.gradle/caches/{item}'
                print(f'Adding {arc}...')
                tar.add(p, arcname=arc, filter=filter_tar)

    cache_size_mb = os.path.getsize(cache_tar_path) / 1024 / 1024
    print(f'Done creating cache archive: {cache_size_mb:.2f} MB')
    cache_sha256 = get_sha256(cache_tar_path)
    print(f'Cache SHA256: {cache_sha256}')

    # Split cache tarball into <=94MB parts wrapped in zip
    part_num = 1
    cache_parts_info = []
    with open(cache_tar_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = f'{cache_tar_name}.part{part_num:02d}'
            part_path = os.path.join(dist_dir, part_name)
            with open(part_path, 'wb') as pf:
                pf.write(chunk)

            part_sha = get_sha256(part_path)
            part_size_mb = os.path.getsize(part_path) / 1024 / 1024

            zip_name = f'{loader_lower}{clean_ver}_cache_part{part_num:02d}.zip'
            zip_path = os.path.join(dist_dir, zip_name)
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                zf.write(part_path, arcname=part_name)

            os.remove(part_path)
            zip_size_mb = os.path.getsize(zip_path) / 1024 / 1024
            print(f'Created {zip_name} ({zip_size_mb:.2f} MB, containing {part_name})')
            cache_parts_info.append({
                'zip_name': zip_name,
                'part_name': part_name,
                'part_sha256': part_sha,
                'part_size_mb': part_size_mb,
                'zip_size_mb': zip_size_mb
            })
            part_num += 1

    os.remove(cache_tar_path)

    # 2. Download and Package JDK Temurin Linux x64
    jdk_url = JDK_URLS[java_ver]
    jdk_tar_name = f'jdk-{java_ver}_linux-x64.tar.gz'
    jdk_tar_path = os.path.join(dist_dir, jdk_tar_name)
    print(f'Downloading JDK {java_ver} from {jdk_url}...')
    urllib.request.urlretrieve(jdk_url, jdk_tar_path)

    jdk_sha256 = get_sha256(jdk_tar_path)
    print(f'JDK {java_ver} SHA256: {jdk_sha256}')

    jdk_part_num = 1
    jdk_parts_info = []
    with open(jdk_tar_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = f'{jdk_tar_name}.part{jdk_part_num:02d}'
            part_path = os.path.join(dist_dir, part_name)
            with open(part_path, 'wb') as pf:
                pf.write(chunk)

            part_sha = get_sha256(part_path)
            part_size_mb = os.path.getsize(part_path) / 1024 / 1024

            zip_name = f'jdk{java_ver}_part{jdk_part_num:02d}.zip'
            zip_path = os.path.join(dist_dir, zip_name)
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                zf.write(part_path, arcname=part_name)

            os.remove(part_path)
            zip_size_mb = os.path.getsize(zip_path) / 1024 / 1024
            print(f'Created {zip_name} ({zip_size_mb:.2f} MB, containing {part_name})')
            jdk_parts_info.append({
                'zip_name': zip_name,
                'part_name': part_name,
                'part_sha256': part_sha,
                'part_size_mb': part_size_mb,
                'zip_size_mb': zip_size_mb
            })
            jdk_part_num += 1

    os.remove(jdk_tar_path)

    # 3. Generate Multilingual Instructions
    all_parts = jdk_parts_info + cache_parts_info
    files_vn = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> chứa {p['part_name']}" for p in all_parts])
    files_en = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> contains {p['part_name']}" for p in all_parts])
    files_ja = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> {p['part_name']} を格納" for p in all_parts])
    files_zh = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> 包含 {p['part_name']}" for p in all_parts])

    bash_cmd = f'''```bash
# 1. Giải nén tất cả file zip / Unzip all zip parts
unzip -o "jdk{java_ver}_part*.zip"
unzip -o "{loader_lower}{clean_ver}_cache_part*.zip"

# 2. Ghép nối lại các file gốc / Merge parts into original archives
cat {jdk_tar_name}.part* > {jdk_tar_name}
cat {cache_tar_name}.part* > {cache_tar_name}

# 3. Kiểm tra tính toàn vẹn SHA256 / Verify SHA256 integrity
echo "{jdk_sha256}  {jdk_tar_name}" | sha256sum -c
echo "{cache_sha256}  {cache_tar_name}" | sha256sum -c

# 4. Cấu hình JDK {java_ver} / Setup JDK {java_ver}
mkdir -p $HOME/jdk-{java_ver}
tar -xzf {jdk_tar_name} -C $HOME/jdk-{java_ver} --strip-components=1
export JAVA_HOME=$HOME/jdk-{java_ver}
export PATH=$JAVA_HOME/bin:$PATH

# 5. Giải nén Project và Gradle Cache vào $HOME / Extract to $HOME
tar -xzf {cache_tar_name} -C $HOME/

# 6. Chạy test build offline / Run offline build test
cd $HOME/{target_arcname}
chmod +x gradlew
./gradlew clean build --offline
```'''

    multilingual_text = f'''======================================================================
BỘ CACHE MINECRAFT {loader.upper()} {mc_ver} OFFLINE CHUẨN LINUX X64
MINECRAFT {loader.upper()} {mc_ver} OFFLINE BUILD CACHE FOR LINUX X64
MINECRAFT {loader.upper()} {mc_ver} オフラインビルドキャッシュ (LINUX X64)
MINECRAFT {loader.upper()} {mc_ver} LINUX X64 离线构建缓存包
======================================================================

[1. TIẾNG VIỆT]
----------------------------------------------------------------------
Mô tả: Bộ cache build offline dành riêng cho Gemini Web (Linux x64).
Toàn bộ thư viện, toolchain và Gradle cache đã được nạp sẵn 100%.

DANH SÁCH FILE CẦN TẢI LÊN GEMINI WEB:
{files_vn}

CÂU LỆNH PROMPT DÁN VÀO GEMINI WEB:
{bash_cmd}


[2. ENGLISH]
----------------------------------------------------------------------
Description: 100% Offline build cache package for Gemini Web (Linux x64).
All dependencies, toolchains, and Gradle caches are completely pre-cached.

FILES TO UPLOAD TO GEMINI WEB:
{files_en}

PROMPT TO COPY AND PASTE INTO GEMINI WEB:
{bash_cmd}


[3. 日本語 (JAPANESE)]
----------------------------------------------------------------------
説明: Gemini Web (Linux x64) 向け 100% オフラインビルド環境パッケージ。
すべての依存ライブラリ、ツールチェーン、Gradleキャッシュが事前キャッシュ済みです。

GEMINI WEB にアップロードするファイル一覧:
{files_ja}

GEMINI WEB のプロンプトに貼り付けるコマンド:
{bash_cmd}


[4. 简体中文 (CHINESE SIMPLIFIED)]
----------------------------------------------------------------------
说明: 专为 Gemini Web (Linux x64) 准备的 100% 离线构建缓存环境。
所有的依赖库、工具链和 Gradle 缓存均已完全预先缓存完毕。

上传到 GEMINI WEB 的文件清单:
{files_zh}

粘贴到 GEMINI WEB 提示词中的运行命令:
{bash_cmd}
======================================================================
'''

    inst_path = os.path.join(dist_dir, 'INSTRUCTIONS_MULTILINGUAL.txt')
    with open(inst_path, 'w', encoding='utf-8') as f:
        f.write(multilingual_text)

    # 4. Create Single All-in-One Zip Package
    aio_zip_name = f'{loader}_{mc_ver}_Offline_GeminiWeb.zip'
    aio_zip_path = os.path.join(dist_dir, aio_zip_name)
    print(f'Creating All-in-One zip: {aio_zip_path}...')

    subfolder_in_zip = f'{loader}_{mc_ver}_GeminiWeb'
    with zipfile.ZipFile(aio_zip_path, 'w', compression=zipfile.ZIP_STORED) as aio_zf:
        for p in all_parts:
            part_file = os.path.join(dist_dir, p['zip_name'])
            aio_zf.write(part_file, arcname=f'{subfolder_in_zip}/{p["zip_name"]}')
        aio_zf.write(inst_path, arcname=f'{subfolder_in_zip}/INSTRUCTIONS_MULTILINGUAL.txt')

    aio_size_mb = os.path.getsize(aio_zip_path) / 1024 / 1024
    print(f'Done creating All-in-One zip: {aio_size_mb:.2f} MB')
    print(f'SUCCESS: All packaging finished for {loader} {mc_ver}!')

if __name__ == '__main__':
    main()

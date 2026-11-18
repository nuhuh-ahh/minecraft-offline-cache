import os
import sys
import hashlib
import zipfile
import tarfile
import shutil
import urllib.request

CHUNK_SIZE = 94 * 1024 * 1024  # 94 MB

dist_dir = os.path.abspath('dist')
os.makedirs(dist_dir, exist_ok=True)
home = os.path.expanduser('~')

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

# ----------------------------------------------------
# 1. Package Project & Gradle Cache (Fabric 1.8.9)
# ----------------------------------------------------
cache_tar_path = os.path.join(dist_dir, 'fabric189_offline_cache.tar.gz')
print(f'Creating {cache_tar_path} on Linux x64...')

with tarfile.open(cache_tar_path, 'w:gz') as tar:
    # 1. Project directory
    print('Adding project files...')
    def project_filter(tarinfo):
        if '/.git' in tarinfo.name or tarinfo.name.startswith('.git') or '/dist' in tarinfo.name or tarinfo.name.startswith('dist'):
            return None
        return filter_tar(tarinfo)

    tar.add('templates/fabric-1.8.9', arcname='fabric-1.8.9', filter=project_filter)

    # 2. ~/.gradle/wrapper
    wrapper_path = os.path.join(home, '.gradle', 'wrapper', 'dists')
    if os.path.exists(wrapper_path):
        print('Adding .gradle/wrapper/dists...')
        tar.add(wrapper_path, arcname='.gradle/wrapper/dists', filter=filter_tar)

    # 3. ~/.gradle/caches
    caches_dir = os.path.join(home, '.gradle', 'caches')
    if os.path.exists(caches_dir):
        for item in os.listdir(caches_dir):
            p = os.path.join(caches_dir, item)
            arc = f'.gradle/caches/{item}'
            print(f'Adding {arc}...')
            tar.add(p, arcname=arc, filter=filter_tar)

cache_size_mb = os.path.getsize(cache_tar_path) / 1024 / 1024
print(f'Done creating archive: {cache_size_mb:.2f} MB')

cache_sha256 = get_sha256(cache_tar_path)
print(f'Fabric 1.8.9 Cache SHA256: {cache_sha256}')

# Split and zip Fabric Cache
part_num = 1
cache_parts_info = []
with open(cache_tar_path, 'rb') as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        part_name = f'fabric189_offline_cache.tar.gz.part{part_num:02d}'
        part_path = os.path.join(dist_dir, part_name)
        with open(part_path, 'wb') as pf:
            pf.write(chunk)
        
        part_sha = get_sha256(part_path)
        part_size_mb = os.path.getsize(part_path) / 1024 / 1024

        zip_name = f'fabric189_cache_part{part_num:02d}.zip'
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

# ----------------------------------------------------
# 2. Download and Package JDK 8 Temurin (Linux x64)
# ----------------------------------------------------
jdk8_url = 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u512-b09/OpenJDK8U-jdk_x64_linux_hotspot_8u512b09.tar.gz'
jdk_tar_path = os.path.join(dist_dir, 'jdk-8_linux-x64.tar.gz')
print(f'Downloading JDK 8 from {jdk8_url}...')
urllib.request.urlretrieve(jdk8_url, jdk_tar_path)

jdk_sha256 = get_sha256(jdk_tar_path)
print(f'JDK 8 SHA256: {jdk_sha256}')

jdk_part_num = 1
jdk_parts_info = []
with open(jdk_tar_path, 'rb') as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        part_name = f'jdk-8_linux-x64.tar.gz.part{jdk_part_num:02d}'
        part_path = os.path.join(dist_dir, part_name)
        with open(part_path, 'wb') as pf:
            pf.write(chunk)
        
        part_sha = get_sha256(part_path)
        part_size_mb = os.path.getsize(part_path) / 1024 / 1024

        zip_name = f'jdk8_part{jdk_part_num:02d}.zip'
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

# ----------------------------------------------------
# 3. Generate Multilingual Instructions
# ----------------------------------------------------
all_parts = jdk_parts_info + cache_parts_info
files_vn = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> chứa {p['part_name']}" for p in all_parts])
files_en = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> contains {p['part_name']}" for p in all_parts])
files_ja = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> {p['part_name']} を格納" for p in all_parts])
files_zh = "\n".join([f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> 包含 {p['part_name']}" for p in all_parts])

bash_cmd = f'''```bash
# 1. Giải nén tất cả file zip / Unzip all zip parts
unzip -o "jdk8_part*.zip"
unzip -o "fabric189_cache_part*.zip"

# 2. Ghép nối lại các file gốc / Merge parts into original archives
cat jdk-8_linux-x64.tar.gz.part* > jdk-8_linux-x64.tar.gz
cat fabric189_offline_cache.tar.gz.part* > fabric189_offline_cache.tar.gz

# 3. Kiểm tra tính toàn vẹn SHA256 / Verify SHA256 integrity
echo "{jdk_sha256}  jdk-8_linux-x64.tar.gz" | sha256sum -c
echo "{cache_sha256}  fabric189_offline_cache.tar.gz" | sha256sum -c

# 4. Cấu hình JDK 8 / Setup JDK 8
mkdir -p $HOME/jdk-8
tar -xzf jdk-8_linux-x64.tar.gz -C $HOME/jdk-8 --strip-components=1
export JAVA_HOME=$HOME/jdk-8
export PATH=$JAVA_HOME/bin:$PATH

# 5. Giải nén Project và Gradle Cache vào $HOME / Extract to $HOME
tar -xzf fabric189_offline_cache.tar.gz -C $HOME/

# 6. Chạy test build offline / Run offline build test
cd $HOME/fabric-1.8.9
chmod +x gradlew
./gradlew clean build --offline
```'''

multilingual_text = f'''======================================================================
BỘ CACHE MINECRAFT FABRIC 1.8.9 OFFLINE CHUẨN LINUX X64
MINECRAFT FABRIC 1.8.9 OFFLINE BUILD CACHE FOR LINUX X64
MINECRAFT FABRIC 1.8.9 オフラインビルドキャッシュ (LINUX X64)
MINECRAFT FABRIC 1.8.9 LINUX X64 离线构建缓存包
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

FILES TO标志 GEMINI WEB:
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

with open(os.path.join(dist_dir, 'CHECKSUMS_AND_INSTRUCTIONS.txt'), 'w', encoding='utf-8') as f:
    f.write(multilingual_text)

# ----------------------------------------------------
# 4. Create Single All-in-One Zip Package
# ----------------------------------------------------
aio_zip_name = 'Fabric_1.8.9_Offline_GeminiWeb.zip'
aio_zip_path = os.path.join(dist_dir, aio_zip_name)
print(f'Creating All-in-One zip: {aio_zip_path}...')

with zipfile.ZipFile(aio_zip_path, 'w', compression=zipfile.ZIP_STORED) as aio_zf:
    for p in all_parts:
        part_file = os.path.join(dist_dir, p['zip_name'])
        aio_zf.write(part_file, arcname=f'Fabric_1.8.9_GeminiWeb/{p["zip_name"]}')
    aio_zf.write(inst_path, arcname='Fabric_1.8.9_GeminiWeb/INSTRUCTIONS_MULTILINGUAL.txt')

aio_size_mb = os.path.getsize(aio_zip_path) / 1024 / 1024
print(f'Done creating All-in-One zip: {aio_size_mb:.2f} MB')

print('All packaging and All-in-One zip completed successfully!')

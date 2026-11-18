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
# 3. Generate Instructions & Verification Commands
# ----------------------------------------------------
inst_path = os.path.join(dist_dir, 'CHECKSUMS_AND_INSTRUCTIONS.txt')
with open(inst_path, 'w', encoding='utf-8') as f:
    f.write('======================================================================\n')
    f.write('BỘ CACHE MINECRAFT FABRIC 1.8.9 OFFLINE CHUẨN LINUX X64 (UBUNTU)\n')
    f.write('======================================================================\n\n')
    f.write(f'JDK 8 Linux x64 SHA256: {jdk_sha256}\n')
    f.write(f'Fabric 1.8.9 Cache SHA256: {cache_sha256}\n\n')
    f.write('DANH SÁCH FILE UPLOAD LÊN GEMINI WEB:\n')
    f.write('----------------------------------------------------------------------\n')
    for p in jdk_parts_info:
        f.write(f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> chứa {p['part_name']}\n")
    for p in cache_parts_info:
        f.write(f"- {p['zip_name']} ({p['zip_size_mb']:.2f} MB) -> chứa {p['part_name']}\n")
    f.write('\nLỆNH CHẠY TRÊN GEMINI WEB (DÁN VÀO PROMPT LÀ CHẠY):\n')
    f.write('----------------------------------------------------------------------\n')
    f.write('```bash\n')
    f.write('# 1. Giải nén tất cả các file zip\n')
    f.write('unzip -o "jdk8_part*.zip"\n')
    f.write('unzip -o "fabric189_cache_part*.zip"\n\n')
    f.write('# 2. Ghép nối lại các file gốc\n')
    f.write('cat jdk-8_linux-x64.tar.gz.part* > jdk-8_linux-x64.tar.gz\n')
    f.write('cat fabric189_offline_cache.tar.gz.part* > fabric189_offline_cache.tar.gz\n\n')
    f.write('# 3. Kiểm tra tính toàn vẹn (SHA256)\n')
    f.write(f'echo "{jdk_sha256}  jdk-8_linux-x64.tar.gz" | sha256sum -c\n')
    f.write(f'echo "{cache_sha256}  fabric189_offline_cache.tar.gz" | sha256sum -c\n\n')
    f.write('# 4. Cấu hình JDK 8\n')
    f.write('mkdir -p $HOME/jdk-8\n')
    f.write('tar -xzf jdk-8_linux-x64.tar.gz -C $HOME/jdk-8 --strip-components=1\n')
    f.write('export JAVA_HOME=$HOME/jdk-8\n')
    f.write('export PATH=$JAVA_HOME/bin:$PATH\n\n')
    f.write('# 5. Giải nén Project và Gradle Cache vào $HOME\n')
    f.write('tar -xzf fabric189_offline_cache.tar.gz -C $HOME/\n\n')
    f.write('# 6. Chạy test build offline\n')
    f.write('cd $HOME/fabric-1.8.9\n')
    f.write('chmod +x gradlew\n')
    f.write('./gradlew clean build --offline\n')
    f.write('```\n\n')
    f.write('======================================================================\n')

print('All packaging completed successfully!')

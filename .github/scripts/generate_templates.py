import os
import shutil

base = 'templates/fabric-1.8.9'
versions = {
    '1.9.4': '1.13.5+1.9.4',
    '1.10.2': '1.13.5+1.10.2',
    '1.11.2': '1.13.5+1.11.2',
    '1.12.2': '1.13.5+1.12.2',
    '1.13.2': None
}

for ver, api in versions.items():
    target = f'templates/fabric-{ver}'
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(base, target)
    
    # Update gradle.properties
    prop_path = os.path.join(target, 'gradle.properties')
    with open(prop_path, 'r', encoding='utf-8') as f:
        props = f.read()
    props = props.replace('minecraft_version=1.8.9', f'minecraft_version={ver}')
    if api:
        props = props.replace('fabric_version=1.13.2+1.8.9', f'fabric_version={api}')
    else:
        props = props.replace('fabric_version=1.13.2+1.8.9', 'fabric_version=none')
    with open(prop_path, 'w', encoding='utf-8') as f:
        f.write(props)
        
    # Update fabric.mod.json
    fmod_path = os.path.join(target, 'src', 'main', 'resources', 'fabric.mod.json')
    with open(fmod_path, 'r', encoding='utf-8') as f:
        fmod = f.read()
    fmod = fmod.replace('"minecraft": "1.8.9"', f'"minecraft": "{ver}"')
    # Remove mixins section if present
    fmod = fmod.replace('  "mixins": [\n    "modid.mixins.json"\n  ],', '')
    with open(fmod_path, 'w', encoding='utf-8') as f:
        f.write(fmod)

    # Remove ExampleMixin.java to avoid any mapping differences
    mixin_dir = os.path.join(target, 'src', 'main', 'java', 'net', 'legacyfabric', 'example', 'mixin')
    if os.path.exists(mixin_dir):
        shutil.rmtree(mixin_dir)

    # If 1.13.2, comment out legacy-fabric-api dependency in build.gradle
    if not api:
        bg_path = os.path.join(target, 'build.gradle')
        with open(bg_path, 'r', encoding='utf-8') as f:
            bg = f.read()
        bg = bg.replace('modImplementation "net.legacyfabric.legacy-fabric-api:legacy-fabric-api:${project.fabric_version}"', '// modImplementation "net.legacyfabric.legacy-fabric-api:legacy-fabric-api:${project.fabric_version}"')
        with open(bg_path, 'w', encoding='utf-8') as f:
            f.write(bg)

    print(f'Configured {target}')

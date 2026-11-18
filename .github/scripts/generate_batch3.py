import os
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEMPLATES_DIR = os.path.join(REPO_ROOT, 'templates')

FORGE_BATCH3_CONFIGS = {
    '1.14.2':  {'java': '8',  'fg': '5.1.77', 'forge': '1.14.2-26.0.63', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.14.3':  {'java': '8',  'fg': '5.1.77', 'forge': '1.14.3-27.0.60', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.15.1':  {'java': '8',  'fg': '5.1.77', 'forge': '1.15.1-30.0.51', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.16.1':  {'java': '8',  'fg': '5.1.77', 'forge': '1.16.1-32.0.108', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.16.2':  {'java': '8',  'fg': '5.1.77', 'forge': '1.16.2-33.0.61', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.16.3':  {'java': '8',  'fg': '5.1.77', 'forge': '1.16.3-34.1.42', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.16.4':  {'java': '8',  'fg': '5.1.77', 'forge': '1.16.4-35.1.37', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.18.1':  {'java': '17', 'fg': '5.1.77', 'forge': '1.18.1-39.1.2',  'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.19.1':  {'java': '17', 'fg': '5.1.77', 'forge': '1.19.1-42.0.9',  'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.19.3':  {'java': '17', 'fg': '5.1.77', 'forge': '1.19.3-44.1.23', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.20.2':  {'java': '17', 'fg': '6.0.29', 'forge': '1.20.2-48.1.0',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.20.3':  {'java': '17', 'fg': '6.0.29', 'forge': '1.20.3-49.0.2',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.3':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.3-53.1.16', 'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.4':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.4-54.1.22', 'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.5':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.5-55.1.18', 'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.6':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.6-56.0.9',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.7':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.7-57.0.3',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.8':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.8-58.1.26', 'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.9':  {'java': '21', 'fg': '6.0.29', 'forge': '1.21.9-59.0.5',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.10': {'java': '21', 'fg': '6.0.29', 'forge': '1.21.10-60.1.18','gradle': '8.8',   'base': 'forge-1.20.1'},
    '1.21.11': {'java': '21', 'fg': '6.0.29', 'forge': '1.21.11-61.2.5', 'gradle': '8.8',   'base': 'forge-1.20.1'},
    '26.1':    {'java': '21', 'fg': '6.0.29', 'forge': '26.1-62.0.9',    'gradle': '8.8',   'base': 'forge-1.20.1'},
    '26.1.1':  {'java': '21', 'fg': '6.0.29', 'forge': '26.1.1-63.0.2',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '26.1.2':  {'java': '21', 'fg': '6.0.29', 'forge': '26.1.2-64.1.6',  'gradle': '8.8',   'base': 'forge-1.20.1'},
    '26.2':    {'java': '21', 'fg': '6.0.29', 'forge': '26.2-65.1.6',    'gradle': '8.8',   'base': 'forge-1.20.1'},
    '26.3':    {'java': '21', 'fg': '6.0.29', 'forge': '26.3-66.1.8',    'gradle': '8.8',   'base': 'forge-1.20.1'},
}

FABRIC_BATCH3_CONFIGS = {
    '1.14.2':  {'java': '8',  'yarn': '1.14.2+build.7', 'api': None},
    '1.16.2':  {'java': '8',  'yarn': '1.16.2+build.47', 'api': None},
    '1.21.5':  {'java': '21', 'yarn': '1.21.5+build.1',  'api': None},
    '1.21.6':  {'java': '21', 'yarn': '1.21.6+build.1',  'api': None},
    '1.21.7':  {'java': '21', 'yarn': '1.21.7+build.8',  'api': None},
    '1.21.8':  {'java': '21', 'yarn': '1.21.8+build.1',  'api': None},
    '1.21.9':  {'java': '21', 'yarn': '1.21.9+build.1',  'api': None},
}

def setup_forge():
    print('=== Setting up Forge Batch 3 Templates ===')
    for ver, cfg in FORGE_BATCH3_CONFIGS.items():
        target = os.path.join(TEMPLATES_DIR, f'forge-{ver}')
        if os.path.exists(target):
            shutil.rmtree(target)
        os.makedirs(target, exist_ok=True)

        base_dir = os.path.join(TEMPLATES_DIR, cfg['base'])
        shutil.copytree(os.path.join(base_dir, 'gradle'), os.path.join(target, 'gradle'))
        shutil.copy(os.path.join(base_dir, 'gradlew'), os.path.join(target, 'gradlew'))
        shutil.copy(os.path.join(base_dir, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

        with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
            f.write("rootProject.name = 'examplemod'\n")

        with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
            f.write("org.gradle.jvmargs=-Xmx2G\norg.gradle.daemon=false\n")

        with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
            f.write(f'''buildscript {{
    repositories {{
        maven {{ url = 'https://maven.minecraftforge.net' }}
        mavenCentral()
    }}
    dependencies {{
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '{cfg['fg']}'
    }}
}}
apply plugin: 'net.minecraftforge.gradle'
apply plugin: 'maven-publish'

version = '1.0.0'
group = 'com.example.modid'
archivesBaseName = 'examplemod'

java.toolchain.languageVersion = JavaLanguageVersion.of({cfg['java']})

repositories {{
    mavenCentral()
    maven {{ url = 'https://maven.minecraftforge.net' }}
}}

minecraft {{
    mappings channel: 'official', version: '{ver}'
    runs {{
        client {{
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'REGISTRIES'
            property 'forge.logging.console.level', 'debug'
            mods {{
                examplemod {{
                    source sourceSets.main
                }}
            }}
        }}
    }}
}}

dependencies {{
    minecraft 'net.minecraftforge:forge:{cfg['forge']}'
}}

jar {{
    manifest {{
        attributes([
            "Specification-Title": "examplemod",
            "Specification-Vendor": "examplemods",
            "Specification-Version": "1",
            "Implementation-Title": project.name,
            "Implementation-Version": "${{version}}",
            "Implementation-Vendor" :"examplemods"
        ])
    }}
}}
''')

        java_dir = os.path.join(target, 'src', 'main', 'java', 'com', 'example', 'modid')
        os.makedirs(java_dir, exist_ok=True)
        with open(os.path.join(java_dir, 'ExampleMod.java'), 'w', encoding='utf-8') as f:
            f.write('''package com.example.modid;

import net.minecraftforge.fml.common.Mod;

@Mod("examplemod")
public class ExampleMod {
    public ExampleMod() {
        System.out.println("Hello Forge world!");
    }
}
''')

        meta_dir = os.path.join(target, 'src', 'main', 'resources', 'META-INF')
        os.makedirs(meta_dir, exist_ok=True)
        with open(os.path.join(meta_dir, 'mods.toml'), 'w', encoding='utf-8') as f:
            f.write(f'''modLoader="javafml"
loaderVersion="[1,)"
license="MIT"
[[mods]]
modId="examplemod"
version="1.0.0"
displayName="Example Mod"
description="Pre-cached Forge {ver} template"
''')
        print(f'Generated Forge {ver} template')

def setup_fabric():
    print('=== Setting up Fabric Batch 3 Templates ===')
    base_dir = os.path.join(TEMPLATES_DIR, 'fabric-1.16.5')
    for ver, cfg in FABRIC_BATCH3_CONFIGS.items():
        target = os.path.join(TEMPLATES_DIR, f'fabric-{ver}')
        if os.path.exists(target):
            shutil.rmtree(target)
        os.makedirs(target, exist_ok=True)

        shutil.copytree(os.path.join(base_dir, 'gradle'), os.path.join(target, 'gradle'))
        shutil.copy(os.path.join(base_dir, 'gradlew'), os.path.join(target, 'gradlew'))
        shutil.copy(os.path.join(base_dir, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

        with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
            f.write('''pluginManagement {
\trepositories {
\t\tmaven {
\t\t\tname = 'Fabric'
\t\t\turl = 'https://maven.fabricmc.net/'
\t\t}
\t\tmavenCentral()
\t\tgradlePluginPortal()
\t}
}

rootProject.name = 'example-mod'
''')

        with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
            f.write(f'''org.gradle.jvmargs=-Xmx1G
org.gradle.parallel=true

minecraft_version={ver}
yarn_mappings={cfg['yarn']}
loader_version=0.16.10
loom_version=1.14.10
target_java={cfg['java']}

version=1.0.0
group=com.example
archives_base_name=example-mod
''')

        with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
            f.write(f'''plugins {{
\tid 'net.fabricmc.fabric-loom-remap' version "${{loom_version}}"
\tid 'maven-publish'
}}

repositories {{
\tmavenCentral()
\tmaven {{
\t\tname = 'Fabric'
\t\turl = 'https://maven.fabricmc.net/'
\t}}
}}

dependencies {{
\tminecraft "com.mojang:minecraft:${{project.minecraft_version}}"
\tmappings "net.fabricmc:yarn:${{project.yarn_mappings}}:v2"
\tmodImplementation "net.fabricmc:fabric-loader:${{project.loader_version}}"
}}

processResources {{
\tdef version = project.version
\tinputs.property "version", version

\tfilesMatching("fabric.mod.json") {{
\t\texpand "version": version
\t}}
}}

tasks.withType(JavaCompile).configureEach {{
\tit.options.encoding = "UTF-8"
\tit.options.release = project.target_java as Integer
}}

java {{
\twithSourcesJar()
\tsourceCompatibility = JavaVersion.toVersion(project.target_java)
\ttargetCompatibility = JavaVersion.toVersion(project.target_java)
}}

jar {{
\tinputs.property "archivesName", project.base.archivesName
}}
''')

        java_dir = os.path.join(target, 'src', 'main', 'java', 'com', 'example')
        os.makedirs(java_dir, exist_ok=True)
        with open(os.path.join(java_dir, 'ExampleMod.java'), 'w', encoding='utf-8') as f:
            f.write('''package com.example;

import net.fabricmc.api.ModInitializer;

public class ExampleMod implements ModInitializer {
    @Override
    public void onInitialize() {
        System.out.println("Hello Fabric world!");
    }
}
''')

        res_dir = os.path.join(target, 'src', 'main', 'resources')
        os.makedirs(res_dir, exist_ok=True)
        with open(os.path.join(res_dir, 'fabric.mod.json'), 'w', encoding='utf-8') as f:
            f.write(f'''{{
  "schemaVersion": 1,
  "id": "example-mod",
  "version": "${{version}}",
  "name": "Example Mod",
  "description": "Pre-cached Fabric {ver} template",
  "authors": ["Developer"],
  "contact": {{}},
  "license": "MIT",
  "entrypoints": {{
    "main": [
      "com.example.ExampleMod"
    ]
  }},
  "depends": {{
    "fabricloader": ">=0.16.0",
    "minecraft": "~{ver}"
  }}
}}
''')
        print(f'Generated Fabric {ver} template')

if __name__ == '__main__':
    setup_forge()
    setup_fabric()

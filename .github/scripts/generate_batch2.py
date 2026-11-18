import os
import shutil

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEMPLATES_DIR = os.path.join(REPO_ROOT, 'templates')

FORGE_CONFIGS = {
    '1.14.4': {'java': '8', 'fg': '5.1.77', 'forge': '1.14.4-28.2.30', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.15.2': {'java': '8', 'fg': '5.1.77', 'forge': '1.15.2-31.2.62', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.17.1': {'java': '16', 'fg': '5.1.77', 'forge': '1.17.1-37.0.0', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.19.2': {'java': '17', 'fg': '5.1.77', 'forge': '1.19.2-43.5.2', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.19.4': {'java': '17', 'fg': '5.1.77', 'forge': '1.19.4-45.4.5', 'gradle': '7.3.3', 'base': 'forge-1.16.5'},
    '1.20.4': {'java': '17', 'fg': '6.0.29', 'forge': '1.20.4-49.2.13', 'gradle': '8.8', 'base': 'forge-1.20.1'},
    '1.20.6': {'java': '21', 'fg': '6.0.29', 'forge': '1.20.6-50.2.15', 'gradle': '8.8', 'base': 'forge-1.20.1'},
    '1.21':   {'java': '21', 'fg': '6.0.29', 'forge': '1.21-51.0.0',    'gradle': '8.8', 'base': 'forge-1.20.1'},
    '1.21.1': {'java': '21', 'fg': '6.0.29', 'forge': '1.21.1-52.1.21', 'gradle': '8.8', 'base': 'forge-1.20.1'},
}

FABRIC_CONFIGS = {
    '1.14':    {'java': '8',  'yarn': '1.14+build.21',    'api': '0.28.5+1.14'},
    '1.14.3':  {'java': '8',  'yarn': '1.14.3+build.13', 'api': None},
    '1.15.1':  {'java': '8',  'yarn': '1.15.1+build.37', 'api': None},
    '1.16.1':  {'java': '8',  'yarn': '1.16.1+build.21', 'api': '0.18.0+build.387-1.16.1'},
    '1.16.3':  {'java': '8',  'yarn': '1.16.3+build.47', 'api': None},
    '1.16.4':  {'java': '8',  'yarn': '1.16.4+build.9',  'api': None},
    '1.17':    {'java': '16', 'yarn': '1.17+build.13',    'api': '0.46.1+1.17'},
    '1.18':    {'java': '17', 'yarn': '1.18+build.1',     'api': '0.77.0+1.18.2'},
    '1.18.1':  {'java': '17', 'yarn': '1.18.1+build.22', 'api': None},
    '1.19':    {'java': '17', 'yarn': '1.19+build.4',     'api': '0.77.0+1.19.2'},
    '1.19.1':  {'java': '17', 'yarn': '1.19.1+build.6',  'api': '0.58.5+1.19.1'},
    '1.19.3':  {'java': '17', 'yarn': '1.19.3+build.5',  'api': '0.76.1+1.19.3'},
    '1.19.4':  {'java': '17', 'yarn': '1.19.4+build.2',  'api': '0.87.2+1.19.4'},
    '1.20':    {'java': '17', 'yarn': '1.20+build.1',     'api': '0.92.12+1.20.1'},
    '1.20.2':  {'java': '17', 'yarn': '1.20.2+build.4',  'api': '0.91.6+1.20.2'},
    '1.20.3':  {'java': '17', 'yarn': '1.20.3+build.1',  'api': '0.91.1+1.20.3'},
    '1.20.5':  {'java': '21', 'yarn': '1.20.5+build.1',  'api': '0.97.8+1.20.5'},
    '1.20.6':  {'java': '21', 'yarn': '1.20.6+build.3',  'api': '0.100.8+1.20.6'},
    '1.21':    {'java': '21', 'yarn': '1.21+build.9',     'api': '0.116.18+1.21.1'},
    '1.21.2':  {'java': '21', 'yarn': '1.21.2+build.1',  'api': '0.106.1+1.21.2'},
    '1.21.3':  {'java': '21', 'yarn': '1.21.3+build.2',  'api': '0.114.1+1.21.3'},
    '1.21.4':  {'java': '21', 'yarn': '1.21.4+build.8',  'api': '0.119.4+1.21.4'},
    '1.21.10': {'java': '21', 'yarn': '1.21.10+build.3', 'api': '0.138.4+1.21.10'},
}

def setup_forge():
    print('=== Setting up Modern Forge Templates ===')
    for ver, cfg in FORGE_CONFIGS.items():
        target = os.path.join(TEMPLATES_DIR, f'forge-{ver}')
        if os.path.exists(target):
            shutil.rmtree(target)
        os.makedirs(target, exist_ok=True)

        base_dir = os.path.join(TEMPLATES_DIR, cfg['base'])
        shutil.copytree(os.path.join(base_dir, 'gradle'), os.path.join(target, 'gradle'))
        shutil.copy(os.path.join(base_dir, 'gradlew'), os.path.join(target, 'gradlew'))
        shutil.copy(os.path.join(base_dir, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

        # settings.gradle
        with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
            f.write("rootProject.name = 'examplemod'\n")

        # gradle.properties
        with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
            f.write("org.gradle.jvmargs=-Xmx2G\norg.gradle.daemon=false\n")

        # build.gradle
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

        # ExampleMod.java
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

        # mods.toml
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
    print('=== Setting up Fabric Templates ===')
    base_dir = os.path.join(TEMPLATES_DIR, 'fabric-1.16.5')
    for ver, cfg in FABRIC_CONFIGS.items():
        target = os.path.join(TEMPLATES_DIR, f'fabric-{ver}')
        if os.path.exists(target):
            shutil.rmtree(target)
        os.makedirs(target, exist_ok=True)

        shutil.copytree(os.path.join(base_dir, 'gradle'), os.path.join(target, 'gradle'))
        shutil.copy(os.path.join(base_dir, 'gradlew'), os.path.join(target, 'gradlew'))
        shutil.copy(os.path.join(base_dir, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

        # settings.gradle
        with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
            f.write('''pluginManagement {
	repositories {
		maven {
			name = 'Fabric'
			url = 'https://maven.fabricmc.net/'
		}
		mavenCentral()
		gradlePluginPortal()
	}
}

rootProject.name = 'example-mod'
''')

        # gradle.properties
        with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
            api_line = f"fabric_api_version={cfg['api']}\n" if cfg['api'] else ""
            f.write(f'''org.gradle.jvmargs=-Xmx1G
org.gradle.parallel=true

minecraft_version={ver}
yarn_mappings={cfg['yarn']}
loader_version=0.16.10
loom_version=1.14.10
{api_line}target_java={cfg['java']}

version=1.0.0
group=com.example
archives_base_name=example-mod
''')

        # build.gradle
        api_dep = '\tmodImplementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_api_version}"\n' if cfg['api'] else ""
        with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
            f.write(f'''plugins {{
	id 'net.fabricmc.fabric-loom-remap' version "${{loom_version}}"
	id 'maven-publish'
}}

repositories {{
	mavenCentral()
	maven {{
		name = 'Fabric'
		url = 'https://maven.fabricmc.net/'
	}}
}}

dependencies {{
	minecraft "com.mojang:minecraft:${{project.minecraft_version}}"
	mappings "net.fabricmc:yarn:${{project.yarn_mappings}}:v2"
	modImplementation "net.fabricmc:fabric-loader:${{project.loader_version}}"
{api_dep}}}

processResources {{
	def version = project.version
	inputs.property "version", version

	filesMatching("fabric.mod.json") {{
		expand "version": version
	}}
}}

tasks.withType(JavaCompile).configureEach {{
	it.options.encoding = "UTF-8"
	it.options.release = project.target_java as Integer
}}

java {{
	withSourcesJar()
	sourceCompatibility = JavaVersion.toVersion(project.target_java)
	targetCompatibility = JavaVersion.toVersion(project.target_java)
}}

jar {{
	inputs.property "archivesName", project.base.archivesName
}}
''')

        # ExampleMod.java
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

        # fabric.mod.json
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

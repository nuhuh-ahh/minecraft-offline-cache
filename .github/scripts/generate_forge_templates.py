import os
import shutil

RETRO_BASE = '../forge-1.12.2-builder'
MODERN_FORGE_BASE = '../forge-1.16.5-builder'

# 1. Retro Forge: 1.8.9, 1.12.0, 1.12.1
RETRO_CONFIGS = {
    '1.8.9': {'mc': '1.8.9', 'mcp_ver': '22', 'release_tag': '1.8.9'},
    '1.12.0': {'mc': '1.12', 'mcp_ver': '39', 'release_tag': '1.12.0'},
    '1.12.1': {'mc': '1.12.1', 'mcp_ver': '39', 'release_tag': '1.12.1'}
}

for tag, cfg in RETRO_CONFIGS.items():
    target = f'templates/forge-{tag}'
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)

    # Copy gradle wrapper & gradlew
    shutil.copytree(os.path.join(RETRO_BASE, 'gradle'), os.path.join(target, 'gradle'))
    shutil.copy(os.path.join(RETRO_BASE, 'gradlew'), os.path.join(target, 'gradlew'))
    shutil.copy(os.path.join(RETRO_BASE, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

    # settings.gradle with pluginManagement
    with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
        f.write('''pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
        maven {
            name = 'GTNH Maven'
            url = 'https://nexus.gtnewhorizons.com/repository/public/'
        }
        maven {
            name = 'CleanroomMC Maven'
            url = 'https://maven.cleanroommc.com'
        }
    }
}

rootProject.name = 'examplemod'
''')

    # gradle-wrapper.properties using Gradle 9.8.2
    wrap_prop = os.path.join(target, 'gradle', 'wrapper', 'gradle-wrapper.properties')
    with open(wrap_prop, 'w', encoding='utf-8') as f:
        f.write('''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-9.8.2-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
''')

    # gradle.properties
    with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
        f.write('''mod_version=1.0.0
mod_group=com.example.modid
archives_base_name=examplemod
''')

    # build.gradle
    with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
        f.write(f'''plugins {{
    id 'java-library'
    id 'maven-publish'
    id 'com.gtnewhorizons.retrofuturagradle' version '2.0.6'
}}

version = project.findProperty('mod_version') ?: '1.0.0'
group = project.findProperty('mod_group') ?: 'com.example.modid'

base {{
    archivesName = project.findProperty('archives_base_name') ?: 'examplemod'
}}

java {{
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}}

tasks.withType(JavaCompile).configureEach {{
    options.encoding = 'UTF-8'
}}

minecraft {{
    mcVersion = '{cfg['mc']}'
    mcpMappingChannel = 'stable'
    mcpMappingVersion = '{cfg['mcp_ver']}'
    useDependencyAccessTransformers = false
    username = 'Developer'
}}

tasks.matching {{ it.name == 'downloadFernflower' }}.configureEach {{
    it.enabled = !gradle.startParameter.offline
}}

repositories {{
    mavenCentral()
    maven {{
        name = 'CleanroomMC Maven'
        url = 'https://maven.cleanroommc.com'
    }}
    maven {{
        name = 'GTNH Maven'
        url = 'https://nexus.gtnewhorizons.com/repository/public/'
    }}
    maven {{
        name = 'Minecraft Forge'
        url = 'https://maven.minecraftforge.net/'
    }}
}}

dependencies {{
}}

processResources {{
    inputs.property 'version', project.version
    inputs.property 'mcversion', minecraft.mcVersion

    filesMatching('mcmod.info') {{
        expand 'version': project.version, 'mcversion': minecraft.mcVersion
    }}
}}
''')

    # src/main/resources/mcmod.info
    res_dir = os.path.join(target, 'src', 'main', 'resources')
    os.makedirs(res_dir, exist_ok=True)
    with open(os.path.join(res_dir, 'mcmod.info'), 'w', encoding='utf-8') as f:
        f.write(f'''[
{{
  "modid": "examplemod",
  "name": "Example Mod",
  "description": "Pre-cached Forge {tag} template",
  "version": "${{version}}",
  "mcversion": "${{mcversion}}",
  "url": "",
  "updateUrl": "",
  "authorList": ["Developer"],
  "credits": "",
  "logoFile": "",
  "screenshots": [],
  "dependencies": []
}}
]
''')

    # src/main/java/com/example/modid/ExampleMod.java
    java_dir = os.path.join(target, 'src', 'main', 'java', 'com', 'example', 'modid')
    os.makedirs(java_dir, exist_ok=True)
    with open(os.path.join(java_dir, 'ExampleMod.java'), 'w', encoding='utf-8') as f:
        f.write('''package com.example.modid;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;

@Mod(modid = "examplemod", name = "Example Mod", version = "1.0.0")
public class ExampleMod {
    @Mod.EventHandler
    public void init(FMLInitializationEvent event) {
        System.out.println("Hello Forge world!");
    }
}
''')
    print(f'Configured Retro Forge template for {tag}')

# 2. Modern Forge 1.20.1
target = 'templates/forge-1.20.1'
if os.path.exists(target):
    shutil.rmtree(target)
os.makedirs(target, exist_ok=True)

# Copy wrapper from MODERN_FORGE_BASE
shutil.copytree(os.path.join(MODERN_FORGE_BASE, 'gradle'), os.path.join(target, 'gradle'))
shutil.copy(os.path.join(MODERN_FORGE_BASE, 'gradlew'), os.path.join(target, 'gradlew'))
shutil.copy(os.path.join(MODERN_FORGE_BASE, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

# Upgrade wrapper to Gradle 8.8 for FG6
wrap_prop = os.path.join(target, 'gradle', 'wrapper', 'gradle-wrapper.properties')
with open(wrap_prop, 'w', encoding='utf-8') as f:
    f.write('''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.8-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
''')

# settings.gradle
with open(os.path.join(target, 'settings.gradle'), 'w', encoding='utf-8') as f:
    f.write("rootProject.name = 'examplemod'\n")

# gradle.properties
with open(os.path.join(target, 'gradle.properties'), 'w', encoding='utf-8') as f:
    f.write('''org.gradle.jvmargs=-Xmx2G
org.gradle.daemon=false
''')

# build.gradle
with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
    f.write('''buildscript {
    repositories {
        maven { url = 'https://maven.minecraftforge.net' }
        mavenCentral()
    }
    dependencies {
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '6.0.29'
    }
}
apply plugin: 'net.minecraftforge.gradle'
apply plugin: 'maven-publish'

version = '1.0.0'
group = 'com.example.modid'
archivesBaseName = 'examplemod'

java.toolchain.languageVersion = JavaLanguageVersion.of(17)

repositories {
    mavenCentral()
    maven { url = 'https://maven.minecraftforge.net' }
}

minecraft {
    mappings channel: 'official', version: '1.20.1'
    runs {
        client {
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'REGISTRIES'
            property 'forge.logging.console.level', 'debug'
            mods {
                examplemod {
                    source sourceSets.main
                }
            }
        }
    }
}

dependencies {
    minecraft 'net.minecraftforge:forge:1.20.1-47.3.0'
}

jar {
    manifest {
        attributes([
            "Specification-Title": "examplemod",
            "Specification-Vendor": "examplemods",
            "Specification-Version": "1",
            "Implementation-Title": project.name,
            "Implementation-Version": "${version}",
            "Implementation-Vendor" :"examplemods"
        ])
    }
}
''')

# src/main/resources/META-INF/mods.toml
meta_dir = os.path.join(target, 'src', 'main', 'resources', 'META-INF')
os.makedirs(meta_dir, exist_ok=True)
with open(os.path.join(meta_dir, 'mods.toml'), 'w', encoding='utf-8') as f:
    f.write('''modLoader="javafml"
loaderVersion="[1,)"
license="CC0-1.0"

[[mods]]
modId="examplemod"
version="1.0.0"
displayName="Example Mod"
description="Pre-cached Forge 1.20.1 template"
''')

# src/main/java/com/example/modid/ExampleMod.java
java_dir = os.path.join(target, 'src', 'main', 'java', 'com', 'example', 'modid')
os.makedirs(java_dir, exist_ok=True)
with open(os.path.join(java_dir, 'ExampleMod.java'), 'w', encoding='utf-8') as f:
    f.write('''package com.example.modid;

import net.minecraftforge.fml.common.Mod;

@Mod("examplemod")
public class ExampleMod {
    public ExampleMod() {
        System.out.println("Hello Modern Forge 1.20.1!");
    }
}
''')

print('Configured Modern Forge template for 1.20.1 (Java 17, Gradle 8.8, FG 6.0.29)')

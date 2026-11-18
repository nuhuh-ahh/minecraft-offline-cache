import os
import shutil

MODERN_FABRIC_VERSIONS = {
    '1.14.4': {'java': '8', 'yarn': '1.14.4+build.18', 'api': '0.28.5+1.14'},
    '1.15.2': {'java': '8', 'yarn': '1.15.2+build.17', 'api': '0.28.5+1.15'},
    '1.16.5': {'java': '8', 'yarn': '1.16.5+build.10', 'api': '0.42.0+1.16'},
    '1.17.1': {'java': '16', 'yarn': '1.17.1+build.65', 'api': '0.46.1+1.17'},
    '1.18.2': {'java': '17', 'yarn': '1.18.2+build.4', 'api': '0.77.0+1.18.2'},
    '1.19.2': {'java': '17', 'yarn': '1.19.2+build.28', 'api': '0.77.0+1.19.2'},
    '1.20.1': {'java': '17', 'yarn': '1.20.1+build.10', 'api': '0.92.12+1.20.1'},
    '1.20.4': {'java': '17', 'yarn': '1.20.4+build.3', 'api': '0.97.3+1.20.4'},
    '1.21.1': {'java': '21', 'yarn': '1.21.1+build.3', 'api': '0.116.18+1.21.1'},
}

base_builder = '../fabric-linux-builder'

for ver, info in MODERN_FABRIC_VERSIONS.items():
    target = f'templates/fabric-{ver}'
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)

    # Copy gradle wrapper & gradlew
    shutil.copytree(os.path.join(base_builder, 'gradle'), os.path.join(target, 'gradle'))
    shutil.copy(os.path.join(base_builder, 'gradlew'), os.path.join(target, 'gradlew'))
    shutil.copy(os.path.join(base_builder, 'gradlew.bat'), os.path.join(target, 'gradlew.bat'))

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
        f.write(f'''org.gradle.jvmargs=-Xmx1G
org.gradle.parallel=true

minecraft_version={ver}
yarn_mappings={info['yarn']}
loader_version=0.16.10
loom_version=1.14.10
fabric_api_version={info['api']}
target_java={info['java']}

version=1.0.0
group=com.example
archives_base_name=example-mod
''')

    # build.gradle
    with open(os.path.join(target, 'build.gradle'), 'w', encoding='utf-8') as f:
        f.write('''plugins {
	id 'net.fabricmc.fabric-loom-remap' version "${loom_version}"
	id 'maven-publish'
}

repositories {
	mavenCentral()
	maven {
		name = 'Fabric'
		url = 'https://maven.fabricmc.net/'
	}
}

dependencies {
	minecraft "com.mojang:minecraft:${project.minecraft_version}"
	mappings "net.fabricmc:yarn:${project.yarn_mappings}:v2"
	modImplementation "net.fabricmc:fabric-loader:${project.loader_version}"
	modImplementation "net.fabricmc.fabric-api:fabric-api:${project.fabric_api_version}"
}

processResources {
	def version = project.version
	inputs.property "version", version

	filesMatching("fabric.mod.json") {
		expand "version": version
	}
}

tasks.withType(JavaCompile).configureEach {
	it.options.encoding = "UTF-8"
	it.options.release = project.target_java as Integer
}

java {
	withSourcesJar()
	sourceCompatibility = JavaVersion.toVersion(project.target_java)
	targetCompatibility = JavaVersion.toVersion(project.target_java)
}

jar {
	inputs.property "archivesName", project.base.archivesName
}
''')

    # src/main/resources/fabric.mod.json
    res_dir = os.path.join(target, 'src', 'main', 'resources')
    os.makedirs(res_dir, exist_ok=True)
    with open(os.path.join(res_dir, 'fabric.mod.json'), 'w', encoding='utf-8') as f:
        f.write(f'''{{
  "schemaVersion": 1,
  "id": "examplemod",
  "version": "${{version}}",
  "name": "Example Mod",
  "description": "Pre-cached Fabric mod template for {ver}",
  "authors": ["Developer"],
  "license": "CC0-1.0",
  "environment": "*",
  "entrypoints": {{
    "main": [
      "com.example.ExampleMod"
    ]
  }},
  "depends": {{
    "fabricloader": ">=0.16.0",
    "minecraft": ">=1.14.0"
  }}
}}
''')

    # src/main/java/com/example/ExampleMod.java
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

    print(f'Configured Modern Fabric template for {ver} (Java {info["java"]})')

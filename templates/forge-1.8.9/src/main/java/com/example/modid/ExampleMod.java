package com.example.modid;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;

@Mod(modid = "examplemod", name = "Example Mod", version = "1.0.0")
public class ExampleMod {
    @Mod.EventHandler
    public void init(FMLInitializationEvent event) {
        System.out.println("Hello Forge world!");
    }
}

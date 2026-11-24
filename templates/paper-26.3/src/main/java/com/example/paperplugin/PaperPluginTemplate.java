package com.example.paperplugin;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;

public class PaperPluginTemplate extends JavaPlugin implements Listener, CommandExecutor {

    @Override
    public void onEnable() {
        saveDefaultConfig();
        getServer().getPluginManager().registerEvents(this, this);

        if (getCommand("paperhello") != null) {
            getCommand("paperhello").setExecutor(this);
        }

        getLogger().info("=================================================");
        getLogger().info(" ExamplePaperPlugin 1.21.11 Successfully Enabled!");
        getLogger().info(" Built 100% Offline for Gemini Web Containers");
        getLogger().info(" Author & Developer: AkumiYuukii");
        getLogger().info("=================================================");
    }

    @Override
    public void onDisable() {
        getLogger().info("ExamplePaperPlugin 1.21.11 Disabled.");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("paperhello")) {
            String welcomeMsg = getConfig().getString("welcome-message", "&a[Paper 1.21.11] &fHello from ExamplePaperPlugin!");
            sender.sendMessage(ChatColor.translateAlternateColorCodes('&', welcomeMsg));
            return true;
        }
        return false;
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        if (getConfig().getBoolean("enable-join-broadcast", true)) {
            Player player = event.getPlayer();
            String format = getConfig().getString("join-message-format", "&b[Server] &fWelcome &e{player} &fto our Paper 1.21.11 server!");
            String msg = format.replace("{player}", player.getName());
            player.sendMessage(ChatColor.translateAlternateColorCodes('&', msg));
        }
    }
}

package mcheli.hud;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Set;
import mcheli.MCH_InputFile;
import mcheli.MCH_Lib;
import net.minecraft.client.Minecraft;

public class MCH_HudManager {

    private static MCH_HudManager instance = new MCH_HudManager();
    private static HashMap map;

    private MCH_HudManager() {
        MCH_HudManager.map = new HashMap();
    }

    public static boolean load(String path) {
        MCH_HudItem.mc = Minecraft.getMinecraft();
        MCH_HudManager.map.clear();
        path = path.replace('\\', '/');
        File dir = new File(path);
        File[] files = dir.listFiles(new FileFilter() {
            public boolean accept(File pathname) {
                String s = pathname.getName().toLowerCase();

                return pathname.isFile() && s.length() >= 5 && s.substring(s.length() - 4).compareTo(".txt") == 0;
            }
        });

        if (files != null && files.length > 0) {
            File[] arr$ = files;
            int len$ = files.length;

            for (int i$ = 0; i$ < len$; ++i$) {
                File f = arr$[i$];
                MCH_InputFile inFile = new MCH_InputFile();
                int line = 0;

                try {
                    String e = f.getName().toLowerCase();

                    e = e.substring(0, e.length() - 4);
                    if (!MCH_HudManager.map.containsKey(e) && inFile.openUTF8(f)) {
                        MCH_Hud info = new MCH_Hud(e, f.getPath());

                        String str;

                        while ((str = inFile.br.readLine()) != null) {
                            ++line;
                            str = str.trim();
                            if (str.equalsIgnoreCase("endif")) {
                                str = "endif=0";
                            }

                            if (str.equalsIgnoreCase("exit")) {
                                str = "exit=0";
                            }

                            int eqIdx = str.indexOf(61);

                            if (eqIdx >= 0 && str.length() > eqIdx + 1) {
                                info.loadItemData(line, str.substring(0, eqIdx).trim().toLowerCase(), str.substring(eqIdx + 1).trim());
                            }
                        }

                        info.checkData();
                        MCH_HudManager.map.put(e, info);
                    }
                } catch (IOException ioexception) {
                    ioexception.printStackTrace();
                } catch (Exception exception) {
                    MCH_Lib.Log("### HUD file error! %s Line=%d", new Object[] { f.getName(), Integer.valueOf(line)});
                    exception.printStackTrace();
                    throw new RuntimeException(exception);
                } finally {
                    inFile.close();
                }
            }

            MCH_Lib.Log("Read %d HUD", new Object[] { Integer.valueOf(MCH_HudManager.map.size())});
            return MCH_HudManager.map.size() > 0;
        } else {
            return false;
        }
    }

    public static MCH_Hud get(String name) {
        return (MCH_Hud) MCH_HudManager.map.get(name.toLowerCase());
    }

    public static boolean contains(String name) {
        return MCH_HudManager.map.containsKey(name);
    }

    public static Set getKeySet() {
        return MCH_HudManager.map.keySet();
    }

    public static Collection getValues() {
        return MCH_HudManager.map.values();
    }
}

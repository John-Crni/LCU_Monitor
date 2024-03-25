package mcheli.hud;

import java.util.Date;
import mcheli.MCH_Config;
import mcheli.MCH_KeyName;
import mcheli.MCH_Lib;
import mcheli.MCH_MOD;
import net.minecraft.client.Minecraft;
import net.minecraft.util.MathHelper;

public class MCH_HudItemString extends MCH_HudItem {

    private final String posX;
    private final String posY;
    private final String format;
    private final MCH_HudItemStringArgs[] args;
    private final boolean isCenteredString;

    public MCH_HudItemString(int fileLine, String posx, String posy, String fmt, String[] arg, boolean centered) {
        super(fileLine);
        this.posX = posx.toLowerCase();
        this.posY = posy.toLowerCase();
        this.format = fmt;
        int len = arg.length < 3 ? 0 : arg.length - 3;

        this.args = new MCH_HudItemStringArgs[len];

        for (int i = 0; i < len; ++i) {
            this.args[i] = MCH_HudItemStringArgs.toArgs(arg[3 + i]);
        }

        this.isCenteredString = centered;
    }

    public void execute() {
        int x = (int) (MCH_HudItemString.centerX + calc(this.posX));
        int y = (int) (MCH_HudItemString.centerY + calc(this.posY));
        long dateCount = Minecraft.getMinecraft().thePlayer.worldObj.getTotalWorldTime();
        int worldTime = (int) ((MCH_HudItemString.ac.worldObj.getWorldTime() + 6000L) % 24000L);
        Date date = new Date();
        Object[] prm = new Object[this.args.length];
        double hp_per = MCH_HudItemString.ac.getMaxHP() > 0 ? (double) MCH_HudItemString.ac.getHP() / (double) MCH_HudItemString.ac.getMaxHP() : 0.0D;

        for (int i = 0; i < prm.length; ++i) {
            switch (this.args[i]) {
            case NAME:
                prm[i] = MCH_HudItemString.ac.getAcInfo().displayName;
                break;

            case ALTITUDE:
                prm[i] = Integer.valueOf(MCH_HudItemString.Altitude);
                break;

            case DATE:
                prm[i] = date;
                break;

            case MC_THOR:
                prm[i] = Integer.valueOf(worldTime / 1000);
                break;

            case MC_TMIN:
                prm[i] = Integer.valueOf(worldTime % 1000 * 36 / 10 / 60);
                break;

            case MC_TSEC:
                prm[i] = Integer.valueOf(worldTime % 1000 * 36 / 10 % 60);
                break;

            case MAX_HP:
                prm[i] = Integer.valueOf(MCH_HudItemString.ac.getMaxHP());
                break;

            case HP:
                prm[i] = Integer.valueOf(MCH_HudItemString.ac.getHP());
                break;

            case HP_PER:
                prm[i] = Double.valueOf(hp_per * 100.0D);
                break;

            case POS_X:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.posX);
                break;

            case POS_Y:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.posY);
                break;

            case POS_Z:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.posZ);
                break;

            case MOTION_X:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.motionX);
                break;

            case MOTION_Y:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.motionY);
                break;

            case MOTION_Z:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.motionZ);
                break;

            case INVENTORY:
                prm[i] = Integer.valueOf(MCH_HudItemString.ac.getSizeInventory());
                break;

            case WPN_NAME:
                prm[i] = MCH_HudItemString.WeaponName;
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }
                break;

            case WPN_AMMO:
                prm[i] = MCH_HudItemString.WeaponAmmo;
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }

                if (MCH_HudItemString.CurrentWeapon.getAmmoNumMax() <= 0) {
                    return;
                }
                break;

            case WPN_RM_AMMO:
                prm[i] = MCH_HudItemString.WeaponAllAmmo;
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }

                if (MCH_HudItemString.CurrentWeapon.getAmmoNumMax() <= 0) {
                    return;
                }
                break;

            case RELOAD_PER:
                prm[i] = Float.valueOf(MCH_HudItemString.ReloadPer);
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }
                break;

            case RELOAD_SEC:
                prm[i] = Float.valueOf(MCH_HudItemString.ReloadSec);
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }
                break;

            case MORTAR_DIST:
                prm[i] = Float.valueOf(MCH_HudItemString.MortarDist);
                if (MCH_HudItemString.CurrentWeapon == null) {
                    return;
                }
                break;

            case MC_VER:
                prm[i] = "1.7.10";
                break;

            case MOD_VER:
                prm[i] = MCH_MOD.VER;
                break;

            case MOD_NAME:
                prm[i] = "MC Helicopter MOD";
                break;

            case YAW:
                prm[i] = Double.valueOf(MCH_Lib.getRotate360((double) (MCH_HudItemString.ac.getRotYaw() + 180.0F)));
                break;

            case PITCH:
                prm[i] = Float.valueOf(-MCH_HudItemString.ac.getRotPitch());
                break;

            case ROLL:
                prm[i] = Float.valueOf(MathHelper.wrapAngleTo180_float(MCH_HudItemString.ac.getRotRoll()));
                break;

            case PLYR_YAW:
                prm[i] = Double.valueOf(MCH_Lib.getRotate360((double) (MCH_HudItemString.player.rotationYaw + 180.0F)));
                break;

            case PLYR_PITCH:
                prm[i] = Float.valueOf(-MCH_HudItemString.player.rotationPitch);
                break;

            case TVM_POS_X:
                prm[i] = Double.valueOf(MCH_HudItemString.TVM_PosX);
                break;

            case TVM_POS_Y:
                prm[i] = Double.valueOf(MCH_HudItemString.TVM_PosY);
                break;

            case TVM_POS_Z:
                prm[i] = Double.valueOf(MCH_HudItemString.TVM_PosZ);
                break;

            case TVM_DIFF:
                prm[i] = Double.valueOf(MCH_HudItemString.TVM_Diff);
                break;

            case CAM_ZOOM:
                prm[i] = Float.valueOf(MCH_HudItemString.ac.camera.getCameraZoom());
                break;

            case UAV_DIST:
                prm[i] = Double.valueOf(MCH_HudItemString.UAV_Dist);
                break;

            case KEY_GUI:
                MCH_Config mch_config = MCH_MOD.config;

                prm[i] = MCH_KeyName.getDescOrName(MCH_Config.KeyGUI.prmInt);
                break;

            case THROTTLE:
                prm[i] = Double.valueOf(MCH_HudItemString.ac.getCurrentThrottle() * 100.0D);

            case NONE:
            }
        }

        if (this.isCenteredString) {
            this.drawCenteredString(String.format(this.format, prm), x, y, MCH_HudItemString.colorSetting);
        } else {
            this.drawString(String.format(this.format, prm), x, y, MCH_HudItemString.colorSetting);
        }

    }

    static class SyntheticClass_1 {

    }
}

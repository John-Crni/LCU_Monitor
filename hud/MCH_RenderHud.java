package mcheli.hud;

import java.util.Iterator;

import org.lwjgl.opengl.GL11;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import mcheli.MCH_Lib;
import mcheli.MCH_ModelManager;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.aircraft.MCH_RenderAircraft;
import mcheli.vehicle.MCH_EntityVehicle;
import mcheli.vehicle.MCH_RenderVehicle;
import mcheli.vehicle.MCH_VehicleInfo;
import mcheli.weapon.MCH_WeaponSet;
import mcheli.wrapper.W_Lib;
import net.minecraft.entity.Entity;
import net.minecraft.util.ResourceLocation;

@SideOnly(Side.CLIENT)
public class MCH_RenderHud extends MCH_RenderAircraft {

    public MCH_RenderHud() {
        this.shadowSize = 2.0F;
    }

    public void bind_tex(String path, MCH_EntityAircraft ac) {
    	super.bindTexture(path, ac);
    }

    public void renderAircraft(MCH_EntityAircraft entity, double posX, double posY, double posZ, float yaw, float pitch, float roll, float tickTime) {

    }

    public void drawPart(MCH_EntityVehicle vehicle, MCH_VehicleInfo info, float yaw, float pitch, MCH_WeaponSet ws, float tickTime) {
     }

    int drawPart(MCH_VehicleInfo.VPart vp, MCH_EntityVehicle vehicle, MCH_VehicleInfo info, float yaw, float pitch, float rotBrl, float tickTime, MCH_WeaponSet ws, int index) {
        GL11.glPushMatrix();
        float recoilBuf = 0.0F;

        if (index < ws.getWeaponNum()) {
            MCH_WeaponSet.Recoil bkIndex = ws.recoilBuf[index];

            recoilBuf = bkIndex.prevRecoilBuf + (bkIndex.recoilBuf - bkIndex.prevRecoilBuf) * tickTime;
        }

        if (vp.rotPitch || vp.rotYaw || vp.type == 1) {
            GL11.glTranslated(vp.pos.xCoord, vp.pos.yCoord, vp.pos.zCoord);
            if (vp.rotYaw) {
                GL11.glRotatef(-vehicle.lastRiderYaw + yaw, 0.0F, 1.0F, 0.0F);
            }

            if (vp.rotPitch) {
                float i$ = MCH_Lib.RNG(vehicle.lastRiderPitch, info.minRotationPitch, info.maxRotationPitch);

                GL11.glRotatef(i$ - pitch, 1.0F, 0.0F, 0.0F);
            }

            if (vp.type == 1) {
                GL11.glRotatef(rotBrl, 0.0F, 0.0F, -1.0F);
            }

            GL11.glTranslated(-vp.pos.xCoord, -vp.pos.yCoord, -vp.pos.zCoord);
        }

        if (vp.type == 2) {
            GL11.glTranslated(0.0D, 0.0D, (double) (-vp.recoilBuf * recoilBuf));
        }

        if (vp.type == 2 || vp.type == 3) {
            ++index;
        }

        MCH_VehicleInfo.VPart vcp;

        if (vp.child != null) {
            for (Iterator iterator = vp.child.iterator(); iterator.hasNext(); index = this.drawPart(vcp, vehicle, info, yaw, pitch, rotBrl, recoilBuf, ws, index)) {
                vcp = (MCH_VehicleInfo.VPart) iterator.next();
            }
        }

        if ((vp.drawFP || !W_Lib.isClientPlayer(vehicle.riddenByEntity) || !W_Lib.isFirstPerson()) && (vp.type != 3 || !vehicle.isWeaponNotCooldown(ws, index))) {
            renderPart(vp.model, info.model, vp.modelName);
            MCH_ModelManager.render("vehicles", vp.modelName);
        }

        GL11.glPopMatrix();
        return index;
    }

    protected ResourceLocation getEntityTexture(Entity entity) {
        return MCH_RenderVehicle.TEX_DEFAULT;
    }

}

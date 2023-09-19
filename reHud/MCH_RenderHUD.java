package mcheli.reHud;

import org.lwjgl.opengl.GL11;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.plane.MCP_PlaneInfo;
import mcheli.plane.RealHudRenderer;
import mcheli.wrapper.W_Render;
import mcheli.wrapper.modelloader.W_ModelCustom;
import net.minecraft.entity.Entity;
import net.minecraft.util.MathHelper;
import net.minecraft.util.Vec3;
import net.minecraftforge.client.model.IModelCustom;

@SideOnly(Side.CLIENT)
public class MCH_RenderHUD extends W_Render{

	private RealHudRenderer RHR=null;

	private MCH_HUDCarsol HUd_Carsol=null;

	private Vec3 InitPos=Vec3.createVectorHelper(10, 5, 0);

	private Vec3 Size=Vec3.createVectorHelper(5, 5, 0);


	@Override
	public void doRender(Entity entity, double posX, double posY, double posZ, float par8, float tickTime) {

		this.shadowSize = 0.0F;

		MCP_PlaneInfo planeInfo = null;

    	if(this.RHR==null) {
    		this.RHR=new RealHudRenderer();
    		MCH_Lib.Log("SUCSESS2!");
    	}

        if (entity != null && entity instanceof MCH_Entity_Hud) {
        	if(((MCH_Entity_Hud)entity).planemodel!=null) {
        		MCH_EntityAircraft ac=((MCH_Entity_Hud)entity).getEntityPlane();
        		int type=((MCH_Entity_Hud)entity).pattern;
                float yaw = this.calcRot(ac.getRotYaw(), ac.prevRotationYaw, tickTime);
                float pitch = ac.calcRotPitch(tickTime);
                float roll = this.calcRot(ac.getRotRoll(), ac.prevRotationRoll, tickTime);
                this.setHudCarsol(ac);
                this.updateHudCarsol(ac);

            	GL11.glPushMatrix();
                GL11.glTranslated(posX, posY, posZ);
                GL11.glRotatef(yaw, 0.0F, -1.0F, 0.0F);
                GL11.glRotatef(pitch, 1.0F, 0.0F, 0.0F);
                GL11.glRotatef(roll, 0.0F, 0.0F, 1.0F);
                this.RHR.update2(type,HUd_Carsol.pos);
                GL11.glPopMatrix();
        	}
        }

   }

	
	
	
	private void setHudCarsol(MCH_EntityAircraft ac) {
    	if(this.HUd_Carsol==null) {
    		Vec3 right=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)0);
    		Vec3 up=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)1);
    		this.HUd_Carsol=new MCH_HUDCarsol(ac,ac.worldObj,right,up,this.InitPos,this.Size);
    	}
	}

	private void updateHudCarsol(MCH_EntityAircraft ac) {
		if(this.HUd_Carsol!=null) {
			Vec3 right=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)0);
			Vec3 up=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)1);
			Vec3 forward=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)2);
			this.HUd_Carsol.update(forward,right, up, this.InitPos,this.Size, ac.posX,ac.posY,ac.posZ);
		}
	}


    public static void renderHud(IModelCustom model) {
        if (model != null) {
            if (model instanceof W_ModelCustom) {
                if (((W_ModelCustom) model).containsPart("$hud")) {
                    model.renderPart("$hud");
                }
            }
        }
    }

    public float calcRot(float rot, float prevRot, float tickTime) {
        rot = MathHelper.wrapAngleTo180_float(rot);
        prevRot = MathHelper.wrapAngleTo180_float(prevRot);
        if (rot - prevRot < -180.0F) {
            prevRot -= 360.0F;
        } else if (prevRot - rot < -180.0F) {
            prevRot += 360.0F;
        }

        return prevRot + (rot - prevRot) * tickTime;
    }

    public static void renderBody(IModelCustom model) {
        if (model != null) {
            if (model instanceof W_ModelCustom) {
                if (((W_ModelCustom) model).containsPart("$body")) {
                    model.renderPart("$body");
                } else {
                    model.renderAll();
                }
            } else {
                model.renderAll();
            }
        }

    }

	private  double Pcos=0;

	private  double Psin=0;

	private  double Ycos=0;

	private  double Ysin=0;

	private  double Rcos=0;

	private  double Rsin=0;

	public Vec3 getRotationMat(float pitch,float yaw,float roll,byte xyz) {
		Pcos=Math.cos(Math.toRadians(pitch));
		Psin=Math.sin(Math.toRadians(pitch));

		Ycos=Math.cos(Math.toRadians(yaw));
		Ysin=Math.sin(Math.toRadians(yaw));

		Rcos=Math.cos(Math.toRadians(roll));
		Rsin=Math.sin(Math.toRadians(roll));

		Vec3 re=Vec3.createVectorHelper(0, 0, 0);

		switch(xyz) {
			case 0:re.xCoord=Rcos*Ycos-Rsin*Psin*Ysin;re.yCoord=-Pcos*Rsin;re.zCoord=Rcos*Ysin+Ycos*Rsin*Psin;break;
			case 1:re.xCoord=Ycos*Rsin+Rcos*Psin*Ysin;re.yCoord=Rcos*Pcos;re.zCoord=Rsin*Ysin-Rcos*Ycos*Psin;break;
			case 2:re.xCoord=-Pcos*Ysin;re.yCoord=Psin;re.zCoord=Pcos*Ycos;break;
		}

		return re;
	}



}

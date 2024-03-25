package mcheli.reHud;

import java.util.List;

import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.hud.MCH_HUDfixed;
import mcheli.plane.MCP_PlaneInfo;
import net.minecraft.util.MathHelper;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class MCHFixedHUD {

	private World worldObj;

	public MCH_Entity_Hud HUD_Entity=null;

	MCP_PlaneInfo planemodel;

	private double Posx=0D;

	private double Posy=0D;

	private double PosZ=0D;

	private float yaw=0;

	private float pitch=0;


	private Vec3 InitSize=Vec3.createVectorHelper(0, 0, 0);



	public MCHFixedHUD(World w,double x,double y,double z,float yaw,float pitch,Vec3 pos,List<MCH_HUDfixed> fixedlist,MCP_PlaneInfo info,MCH_EntityAircraft Plane) {
		this.worldObj=w;
		this.Posx=x;
		this.Posy=y;
		this.PosZ=z;
		Vec3 Diffx=MCH_RotateMatrix.getRotationMat((float)(pitch), -1*MathHelper.wrapAngleTo180_float(yaw), 0, (byte) 0);
		Diffx=Vec3.createVectorHelper(Diffx.xCoord, Diffx.yCoord, Diffx.zCoord);
		Vec3 Diffy=MCH_RotateMatrix.getRotationMat((float)(pitch),-1* MathHelper.wrapAngleTo180_float(yaw), 0, (byte) 1);
		Diffy=Vec3.createVectorHelper(Diffy.xCoord, Diffy.yCoord, Diffy.zCoord);

		Diffx.xCoord*=pos.xCoord;
		Diffx.yCoord*=pos.xCoord;
		Diffx.zCoord*=pos.xCoord;

		Diffy.xCoord*=pos.yCoord;
		Diffy.yCoord*=pos.yCoord;
		Diffy.zCoord*=pos.yCoord;

		this.Posx+=Diffx.xCoord;
		this.Posx+=Diffy.xCoord;

		this.Posy+=Diffx.yCoord;
		this.Posy+=Diffy.yCoord;

		this.PosZ+=Diffx.zCoord;
		this.PosZ+=Diffy.zCoord;

		this.yaw=yaw;
		this.pitch=pitch;


		this.HUD_Entity=new MCH_Entity_Hud(this.worldObj,this.Posx,this.Posy,this.PosZ,this.yaw,this.pitch,fixedlist,info,Plane);
		this.worldObj.spawnEntityInWorld(this.HUD_Entity);
		this.HUD_Entity.IsSeted=true;
	}


	public void Destroy() {
		MCH_Lib.Log("DEATH!!!");
		this.HUD_Entity.setDead();
	}

}

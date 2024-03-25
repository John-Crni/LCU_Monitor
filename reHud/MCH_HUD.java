package mcheli.reHud;

import java.util.ArrayList;
import java.util.List;

import mcheli.MCH_Lib;
import mcheli.plane.MCP_PlaneInfo;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class MCH_HUD {

	private World worldObj;

	public MCH_Entity_Hud HUD_Entity=null;

	MCP_PlaneInfo planemodel;

	private double Posx=0D;

	private double Posy=0D;

	private double PosZ=0D;

	private float yaw=0;

	private float pitch=0;

	private Vec3 InitPos=Vec3.createVectorHelper(10, 5, 0);

	public List<HudSquare> HudList;

	public MCH_HUD(World w) {
		this.worldObj=w;
		this.HudList=new ArrayList();
	}

	public void setType(int type) {
		this.HUD_Entity.pattern=type;
	}

/*
	public void setHUD_Entity(double x,double y,double z,float yaw,float pitch,MCP_PlaneInfo info,MCH_EntityAircraft Plane) {
		this.Posx=x;
		this.Posy=y;
		this.PosZ=z;
		Vec3 Diffx=MCH_RotateMatrix.getRotationMat((float)(pitch), -1*MathHelper.wrapAngleTo180_float(yaw), 0, (byte) 0);
		Diffx=Vec3.createVectorHelper(Diffx.xCoord, Diffx.yCoord, Diffx.zCoord);
		Vec3 Diffy=MCH_RotateMatrix.getRotationMat((float)(pitch),-1* MathHelper.wrapAngleTo180_float(yaw), 0, (byte) 1);
		Diffy=Vec3.createVectorHelper(Diffy.xCoord, Diffy.yCoord, Diffy.zCoord);

		Diffx.xCoord*=this.InitPos.xCoord;
		Diffx.yCoord*=this.InitPos.xCoord;
		Diffx.zCoord*=this.InitPos.xCoord;

		Diffy.xCoord*=this.InitPos.yCoord;
		Diffy.yCoord*=this.InitPos.yCoord;
		Diffy.zCoord*=this.InitPos.yCoord;

		this.Posx+=Diffx.xCoord;
		this.Posx+=Diffy.xCoord;

		this.Posy+=Diffx.yCoord;
		this.Posy+=Diffy.yCoord;

		this.PosZ+=Diffx.zCoord;
		this.PosZ+=Diffy.zCoord;

		this.yaw=yaw;
		this.pitch=pitch;
		this.HUD_Entity=new MCH_Entity_Hud(this.worldObj,this.Posx,this.Posy,this.PosZ,this.yaw,this.pitch,info,Plane);
		this.worldObj.spawnEntityInWorld(this.HUD_Entity);
		this.HUD_Entity.IsSeted=true;
	}
	*/

	public void Destroy() {
		MCH_Lib.Log("DEATH!!!");
		this.HUD_Entity.setDead();
	}

}

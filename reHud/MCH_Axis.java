package mcheli.reHud;

import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.plane.MCP_PlaneInfo;
import net.minecraft.world.World;

public class MCH_Axis {

	private World worldObj;

	public MCH_EntityAxis HUD_Entity=null;

	MCP_PlaneInfo planemodel;

	private double Posx=0D;

	private double Posy=0D;

	private double PosZ=0D;

	private float yaw=0;

	private float pitch=0;

	private boolean isEnabled=false;

	public MCH_Axis(World w) {
		this.worldObj=w;
	}

	public void setAxis_Entity(double x,double y,double z,float yaw,float pitch,MCP_PlaneInfo info,MCH_EntityAircraft Plane) {
		this.Posx=x;
		this.Posy=y;
		this.PosZ=z;
		this.yaw=yaw;
		this.pitch=pitch;
		this.HUD_Entity=new MCH_EntityAxis(this.worldObj,this.Posx,this.Posy,this.PosZ,this.yaw,this.pitch,info,Plane);
		this.planemodel=info;
		this.worldObj.spawnEntityInWorld(this.HUD_Entity);
		this.isEnabled=true;
	}

	public void update(double PosX,double PosY,double PosZ, float yaw, float pitch) {
		this.HUD_Entity.Update(PosX,PosY,PosZ,yaw,pitch);
	}

	public void Destroy() {
		MCH_Lib.Log("DEATH!!!");
		this.HUD_Entity.setDead();
	}


}

package mcheli.reHud;

import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.plane.MCP_PlaneInfo;
import mcheli.wrapper.W_Entity;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.world.World;

public class MCH_EntityAxis  extends W_Entity{

	public MCP_PlaneInfo planemodel;

	private MCH_EntityAircraft Plane=null;

	private byte count=0;

	private int PrevCount=0;

	public MCH_EntityAxis(World par1World) {
		super(par1World);
		// TODO 自動生成されたコンストラクター・スタブ
	}

    public MCH_EntityAxis(World par1World, double posX, double posY, double posZ, float yaw, float pitch,MCP_PlaneInfo info,MCH_EntityAircraft PLANE) {
        super(par1World);
        this.Plane=PLANE;
        this.ignoreFrustumCheck = true;
        this.setSize(1.0F, 1.0F);
        this.setLocationAndAngles(posX, posY, posZ, yaw, pitch);
        this.setPosition(posX, posY, posZ);
        this.planemodel=info;
    }

	@Override
	protected void readEntityFromNBT(NBTTagCompound p_70037_1_) {
		// TODO 自動生成されたメソッド・スタブ

	}

	@Override
	protected void writeEntityToNBT(NBTTagCompound p_70014_1_) {
		// TODO 自動生成されたメソッド・スタブ

	}

	public MCP_PlaneInfo getInfo() {
		return this.planemodel;
	}

	public void onUpdate() {
		this.MonitorPlane();
	}

	public void Update(double PosX,double PosY,double PosZ, float yaw, float pitch){
        this.setLocationAndAngles(posX, posY, posZ, yaw, pitch);
        this.setPosition(posX, posY, posZ);
		this.prevPosX=this.posX;
		this.prevPosY=this.posY;
		this.prevPosZ=this.posZ;
		this.posX=PosX;
		this.posY=PosY;
		this.posZ=PosZ;
	}

	private void MonitorPlane() {
		if(this.IsPlaneDead()) {
			MCH_Lib.Log("PLANE IS DEAD!!!!!! ");
			this.setDead();
		}
	}


	private boolean IsPlaneDead() {
		if(this.count%3==0) {
			this.count=0;
			this.PrevCount=this.Plane.getCountOnUpdate();
			this.count+=1;
		}else {
			if(this.PrevCount==this.Plane.getCountOnUpdate()) {
				return true;
			}
			this.count+=1;
		}
		return false;
	}

}

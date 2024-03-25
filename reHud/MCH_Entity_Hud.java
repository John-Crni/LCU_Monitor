package mcheli.reHud;

import java.util.ArrayList;
import java.util.List;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.hud.MCH_HUDfixed;
import mcheli.plane.MCP_PlaneInfo;
import mcheli.wrapper.W_Entity;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class MCH_Entity_Hud extends W_Entity{

	public final String NAME="HUDENETIYT!";

	private final int BrightPattern=15728880;

	private final int DarkPattern=15728640;

	private boolean Light_Stats=true;

	public MCP_PlaneInfo planemodel;

	private MCH_EntityAircraft Plane=null;

	public List<MCH_HUDfixed> fixedHudlist;

	private int PrevCount=0;


	private byte count=0;

	private double[][] rotate_matrix=new double[3][3];

	private Vec3 vDiff=Vec3.createVectorHelper(0, 0, 0);
	private Vec3 Diffx=Vec3.createVectorHelper(0, 0, 0);
	private Vec3 Diffy=Vec3.createVectorHelper(0, 0, 0);
	private Vec3 Diffz=Vec3.createVectorHelper(0, 0, 0);
	private Vec3 InitPos=Vec3.createVectorHelper(10, 5, 0);

	private double distance=11.18033989;

	public boolean IsSeted=false;

	public int pattern=1;



	public MCH_Entity_Hud(World par1World) {
		super(par1World);
		this.ignoreFrustumCheck = true;
	}

	public MCH_EntityAircraft getEntityPlane() {
		return this.Plane;
	}

    public MCH_Entity_Hud(World par1World, double posX, double posY, double posZ, float yaw, float pitch,List<MCH_HUDfixed> fixedlist,MCP_PlaneInfo info,MCH_EntityAircraft PLANE) {
        super(par1World);
        this.fixedHudlist=new ArrayList();
        for(int i=0;i<fixedlist.size();i++) {
        	this.fixedHudlist.add(fixedlist.get(i));
        	this.fixedHudlist.get(this.fixedHudlist.size()-1).EntityHud=this;
        }
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

	public void onUpdate() {
		this.MonitorPlane();
		if(this.Plane!=null&&this.IsSeted) {
			this.Update();
		}
	}

	public void Update(){
		this.setPosition();

	}

	public void setPosition() {
	if(this.Plane!=null) {
			this.prevPosX=this.posX;
			this.prevPosY=this.posY;
			this.prevPosZ=this.posZ;
			this.posX=this.Plane.posX;
			this.posY=this.Plane.posY;
			this.posZ=this.Plane.posZ;
	       // this.rotationYaw =  (this.Plane.getRotYaw()%360);
	      //  this.rotationPitch = this.Plane.getRotPitch();
			/**
			if(this.pattern==1) {
				this.setRotationMat((float)(-1*this.Plane.getRotPitch()),(this.Plane.getRotYaw()%360),-1*(this.Plane.getRotRoll()%360) );//-1*(this.Plane.getRotRoll()%360)

				Diffx.xCoord*=this.InitPos.xCoord;
				Diffx.yCoord*=this.InitPos.xCoord;
				Diffx.zCoord*=this.InitPos.xCoord;

				Diffy.xCoord*=this.InitPos.yCoord;
				Diffy.yCoord*=this.InitPos.yCoord;
				Diffy.zCoord*=this.InitPos.yCoord;

				this.posX+=Diffx.xCoord;
				this.posX+=Diffy.xCoord;

				this.posY+=Diffx.yCoord;
				this.posY+=Diffy.yCoord;

				this.posZ+=Diffx.zCoord;
				this.posZ+=Diffy.zCoord;
			}
			*/
		}
	}



	private void MonitorPlane() {
		if(this.IsPlaneDead()) {
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

	public void SetLight(boolean light_stats) {
		this.Light_Stats=light_stats;
	}

    protected void entityInit() {
        super.entityInit();
    }

    public void setDead() {
        super.setDead();
    }


    @SideOnly(Side.CLIENT)
    public float getShadowSize() {
        return 0.0F;
    }

    public float getBrightness(float par1) {
        return 1.0F;
    }

    @SideOnly(Side.CLIENT)//15728880
    public int getBrightnessForRender(float par1) {
    	if(this.Light_Stats) {
    		return this.BrightPattern;
    	}else {
    		return this.DarkPattern;
    	}
    }

	private  double Pcos=0;

	private  double Psin=0;

	private  double Ycos=0;

	private  double Ysin=0;

	private  double Rcos=0;

	private  double Rsin=0;

	public void setRotationMat(float pitch,float yaw,float roll) {
		Pcos=Math.cos(Math.toRadians(pitch));
		Psin=Math.sin(Math.toRadians(pitch));

		Ycos=Math.cos(Math.toRadians(yaw));
		Ysin=Math.sin(Math.toRadians(yaw));

		Rcos=Math.cos(Math.toRadians(roll));
		Rsin=Math.sin(Math.toRadians(roll));

		Diffx.xCoord=Rcos*Ycos-Rsin*Psin*Ysin;
		Diffx.yCoord=-Pcos*Rsin;
		Diffx.zCoord=Rcos*Ysin+Ycos*Rsin*Psin;

		Diffy.xCoord=Ycos*Rsin+Rcos*Psin*Ysin;
		Diffy.yCoord=Rcos*Pcos;
		Diffy.zCoord=Rsin*Ysin-Rcos*Ycos*Psin;

		Diffz.xCoord=-Pcos*Ysin;
		Diffz.yCoord=Psin;
		Diffz.zCoord=Pcos*Ycos;


	}






}

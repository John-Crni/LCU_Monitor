package mcheli.reHud;

import java.util.ArrayList;
import java.util.List;

import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_EntityAircraft;
import net.minecraft.client.Minecraft;
import net.minecraft.client.settings.GameSettings;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class MCH_HUDCarsol {

	private Vec3 RightVector=Vec3.createVectorHelper(0, 0, 0);

	private Vec3 UpVector=Vec3.createVectorHelper(0, 0, 0);

	private double posx=0;

	private double posy=0;

	private double posz=0;

	private MCH_RealRadar Radar;

	private MCH_EntityAircraft Aircraft;

	private World worldObj;

	public Vec3 U_Left=Vec3.createVectorHelper(3, 0, 0);

	public Vec3 U_Right=Vec3.createVectorHelper(3, 0, 0);

	public Vec3 MiddlePos=Vec3.createVectorHelper(3, 0, 0);

	public Vec3 D_Left=Vec3.createVectorHelper(3, 0, 0);

	public Vec3 D_Right=Vec3.createVectorHelper(3, 0, 0);

	public Vec3 eyePos=Vec3.createVectorHelper(0, 0, 0);

	public Vec3 intersectPoint=Vec3.createVectorHelper(0, 0, 0);

	//--------------------------------------------------//

	private Vec3 n=Vec3.createVectorHelper(0, 0, 0);

	private Vec3 x=Vec3.createVectorHelper(0, 0, 0);

	private Vec3 m=Vec3.createVectorHelper(0, 0, 0);

	private Vec3 x0=Vec3.createVectorHelper(0, 0, 0);

	//--------------------------------------------------//

	double posAB=0;
	double posBC=0;
	double posCD=0;
	double posDA=0;

	public vec2 pos=new vec2();




	private double h=0;

	Minecraft mc;



	public MCH_HUDCarsol(MCH_EntityAircraft air,World w,Vec3 right,Vec3 up,Vec3 rate,Vec3 size){
		this.Aircraft=air;
		this.updatePos(right, up, rate,size, air.posX, air.posY, air.posZ);
		Radar=new MCH_RealRadar(w);
		mc = Minecraft.getMinecraft();
	}

	public void updatePos(Vec3 right,Vec3 up,Vec3 rate,Vec3 size,double x,double y,double z) {
		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*rate.xCoord;
		this.RightVector.yCoord=right.yCoord*rate.xCoord;
		this.RightVector.zCoord=right.zCoord*rate.xCoord;
		this.UpVector.xCoord=up.xCoord*rate.yCoord;
		this.UpVector.yCoord=up.yCoord*rate.yCoord;
		this.UpVector.zCoord=up.zCoord*rate.yCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord);

		this.D_Right.xCoord=this.posx;
		this.D_Right.yCoord=this.posy;
		this.D_Right.zCoord=this.posz;

		this.D_Left.xCoord=this.posx+(size.xCoord*right.xCoord);
		this.D_Left.yCoord=this.posy+(size.xCoord*right.yCoord);
		this.D_Left.zCoord=this.posz+(size.xCoord*right.zCoord);

		this.U_Right.xCoord=this.posx+(size.yCoord*up.xCoord);
		this.U_Right.yCoord=this.posy+(size.yCoord*up.yCoord);
		this.U_Right.zCoord=this.posz+(size.yCoord*up.zCoord);

		this.MiddlePos.xCoord=this.posx+((size.yCoord/2)*up.xCoord);
		this.MiddlePos.yCoord=this.posy+((size.yCoord/2)*up.yCoord);
		this.MiddlePos.zCoord=this.posz+((size.yCoord/2)*up.zCoord);

		this.U_Left.xCoord=this.U_Right.xCoord+(size.yCoord*right.xCoord);
		this.U_Left.yCoord=this.U_Right.yCoord+(size.yCoord*right.yCoord);
		this.U_Left.zCoord=this.U_Right.zCoord+(size.yCoord*right.zCoord);

		this.MiddlePos.xCoord=this.MiddlePos.xCoord+(size.yCoord/2*right.xCoord);
		this.MiddlePos.yCoord=this.MiddlePos.yCoord+(size.yCoord/2*right.yCoord);
		this.MiddlePos.zCoord=this.MiddlePos.zCoord+(size.yCoord/2*right.zCoord);
		if(this.mc!=null) {
			this.eyePos.xCoord=mc.thePlayer.getPosition(1).xCoord;
			this.eyePos.yCoord=mc.thePlayer.getPosition(1).yCoord;
			this.eyePos.zCoord=mc.thePlayer.getPosition(1).zCoord;
		}
	}

	List<Vec3> Entitys = new ArrayList<Vec3>();


	public void update(Vec3 forward,Vec3 right,Vec3 up,Vec3 rate,Vec3 size,double x,double y,double z) {
		this.updatePos(right, up, rate, size, x, y, z);
		GameSettings gameSettings = this.mc.gameSettings;
		Entitys=this.Radar.updateXZ(this.Aircraft, 100,this.eyePos,this.mc.thePlayer.getLookVec(),gameSettings.fovSetting+30,this.MiddlePos,forward);
		if(Entitys!=null) {
			if(Entitys.size()>0) {
				setPointPos(MiddlePos,forward,eyePos,Entitys.get(0));
			}
		}
	}
	private void setPointPos2(Vec3 planePos,Vec3 planeForward,Vec3 startPos,Vec3 tgtPos) {
		this.setCrossPoint(planePos, planeForward, startPos, tgtPos);
		n.xCoord=this.D_Right.xCoord-this.D_Left.xCoord;
		n.yCoord=this.D_Right.yCoord-this.D_Left.yCoord;
		n.zCoord=this.D_Right.zCoord-this.D_Left.zCoord;
		double dis=Vec2Dis(n);
		//EA
		x.xCoord=intersectPoint.xCoord-this.D_Left.xCoord;
		x.yCoord=intersectPoint.yCoord-this.D_Left.yCoord;
		x.zCoord=intersectPoint.zCoord-this.D_Left.zCoord;

		posAB=(x.dotProduct(n))/(dis*dis);
		//if(posAB<0||posAB>1) return false ;

		//BC
		n.xCoord=this.U_Right.xCoord-this.D_Right.xCoord;
		n.yCoord=this.U_Right.yCoord-this.D_Right.yCoord;
		n.zCoord=this.U_Right.zCoord-this.D_Right.zCoord;
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.D_Right.xCoord;
		x.yCoord=intersectPoint.yCoord-this.D_Right.yCoord;
		x.zCoord=intersectPoint.zCoord-this.D_Right.zCoord;

		posBC=(x.dotProduct(n))/(dis*dis);
		//if(posBC<0||posBC>1) return false ;

		//CD
		n.xCoord=this.U_Left.xCoord-this.U_Right.xCoord;
		n.yCoord=this.U_Left.yCoord-this.U_Right.yCoord;
		n.zCoord=this.U_Left.zCoord-this.U_Right.zCoord;
		//BC_Length
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.U_Right.xCoord;
		x.yCoord=intersectPoint.yCoord-this.U_Right.yCoord;
		x.zCoord=intersectPoint.zCoord-this.U_Right.zCoord;

		posCD=(x.dotProduct(n))/(dis*dis);
		//if(posCD<0||posCD>1) return false ;

		//DA
		n.xCoord=this.D_Left.xCoord-this.U_Left.xCoord;
		n.yCoord=this.D_Left.yCoord-this.U_Left.yCoord;
		n.zCoord=this.D_Left.zCoord-this.U_Left.zCoord;
		//BC_Length
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.U_Left.xCoord;
		x.yCoord=intersectPoint.yCoord-this.U_Left.yCoord;
		x.zCoord=intersectPoint.zCoord-this.U_Left.zCoord;

		posDA=(x.dotProduct(n))/(dis*dis);
		//if(posDA<0||posDA>1) return false ;

		pos.x=(float)(1D-posAB);
		pos.y=(float)posBC;
	}

	private boolean setPointPos(Vec3 planePos,Vec3 planeForward,Vec3 startPos,Vec3 tgtPos) {
		this.setCrossPoint(planePos, planeForward, startPos, tgtPos);
		//AB
		n.xCoord=this.D_Right.xCoord-this.D_Left.xCoord;
		n.yCoord=this.D_Right.yCoord-this.D_Left.yCoord;
		n.zCoord=this.D_Right.zCoord-this.D_Left.zCoord;
		double dis=Vec2Dis(n);
		//EA
		x.xCoord=intersectPoint.xCoord-this.D_Left.xCoord;
		x.yCoord=intersectPoint.yCoord-this.D_Left.yCoord;
		x.zCoord=intersectPoint.zCoord-this.D_Left.zCoord;

		posAB=(x.dotProduct(n))/(dis*dis);

		if(posAB<0||posAB>1) return false ;

		//BC
		n.xCoord=this.U_Right.xCoord-this.D_Right.xCoord;
		n.yCoord=this.U_Right.yCoord-this.D_Right.yCoord;
		n.zCoord=this.U_Right.zCoord-this.D_Right.zCoord;
		//BC_Length
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.D_Right.xCoord;
		x.yCoord=intersectPoint.yCoord-this.D_Right.yCoord;
		x.zCoord=intersectPoint.zCoord-this.D_Right.zCoord;

		posBC=(x.dotProduct(n))/(dis*dis);

		if(posBC<0||posBC>1) return false ;

		//CD
		n.xCoord=this.U_Left.xCoord-this.U_Right.xCoord;
		n.yCoord=this.U_Left.yCoord-this.U_Right.yCoord;
		n.zCoord=this.U_Left.zCoord-this.U_Right.zCoord;
		//BC_Length
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.U_Right.xCoord;
		x.yCoord=intersectPoint.yCoord-this.U_Right.yCoord;
		x.zCoord=intersectPoint.zCoord-this.U_Right.zCoord;

		posCD=(x.dotProduct(n))/(dis*dis);

		if(posCD<0||posCD>1) return false ;

		//DA
		n.xCoord=this.D_Left.xCoord-this.U_Left.xCoord;
		n.yCoord=this.D_Left.yCoord-this.U_Left.yCoord;
		n.zCoord=this.D_Left.zCoord-this.U_Left.zCoord;
		//BC_Length
		dis=Vec2Dis(n);
		//EB
		x.xCoord=intersectPoint.xCoord-this.U_Left.xCoord;
		x.yCoord=intersectPoint.yCoord-this.U_Left.yCoord;
		x.zCoord=intersectPoint.zCoord-this.U_Left.zCoord;

		posDA=(x.dotProduct(n))/(dis*dis);

		if(posDA<0||posDA>1) return false ;

		pos.x=(float)(1D-posAB);
		pos.y=(float)posBC;

		return true;
	}

	private void setCrossPoint(Vec3 planePos,Vec3 planeForward,Vec3 startPos,Vec3 tgtPos){
		n.xCoord=-1*planeForward.xCoord;
		n.yCoord=-1*planeForward.yCoord;
		n.zCoord=-1*planeForward.zCoord;
		x.xCoord=planePos.xCoord;
		x.yCoord=planePos.yCoord;
		x.zCoord=planePos.zCoord;
		intersectPoint.xCoord=startPos.xCoord;
		intersectPoint.yCoord=startPos.yCoord;
		intersectPoint.zCoord=startPos.zCoord;
		m.xCoord=tgtPos.xCoord-startPos.xCoord;
		m.yCoord=tgtPos.yCoord-startPos.yCoord;
		m.zCoord=tgtPos.zCoord-startPos.zCoord;
		h=n.dotProduct(x);
		double h_m=(h-n.dotProduct(intersectPoint))/(n.dotProduct(m));
		m.xCoord*=h_m;
		m.yCoord*=h_m;
		m.zCoord*=h_m;
		intersectPoint.xCoord+=m.xCoord;
		intersectPoint.yCoord+=m.yCoord;
		intersectPoint.zCoord+=m.zCoord;
	}

	private double Vec2Dis(Vec3 vec) {
		return Math.sqrt((vec.xCoord*vec.xCoord)+(vec.yCoord*vec.yCoord)+(vec.zCoord*vec.zCoord));
	}


	private void print(String format) {
		MCH_Lib.Log(format);
	}








}

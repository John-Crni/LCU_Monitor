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

	private Vec3 FwdVector=Vec3.createVectorHelper(0, 0, 0);

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

	Vec3 DLrate=Vec3.createVectorHelper(0, 0, 0);
	Vec3 DRrate=Vec3.createVectorHelper(0, 0, 0);
	Vec3 Middlerate=Vec3.createVectorHelper(0, 0, 0);
	Vec3 ULrate=Vec3.createVectorHelper(0, 0, 0);
	Vec3 URrate=Vec3.createVectorHelper(0, 0, 0);

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

	public MCH_HUDCarsol(MCH_EntityAircraft air,World w,Vec3 right,Vec3 up,Vec3 forward,Vec3 DRrate,Vec3 DLrate,Vec3 Middlerate,Vec3 URrate,Vec3 ULrate){
		this.Aircraft=air;
		this.DRrate.xCoord=DRrate.xCoord;
		this.DRrate.yCoord=DRrate.yCoord;
		this.DRrate.zCoord=DRrate.zCoord;
		this.DLrate.xCoord=DLrate.xCoord;
		this.DLrate.yCoord=DLrate.yCoord;
		this.DLrate.zCoord=DLrate.zCoord;
		this.Middlerate.xCoord=Middlerate.xCoord;
		this.Middlerate.yCoord=Middlerate.yCoord;
		this.Middlerate.zCoord=Middlerate.zCoord;
		this.URrate.xCoord=URrate.xCoord;
		this.URrate.yCoord=URrate.yCoord;
		this.URrate.zCoord=URrate.zCoord;
		this.ULrate.xCoord=ULrate.xCoord;
		this.ULrate.yCoord=ULrate.yCoord;
		this.ULrate.zCoord=ULrate.zCoord;
		this.updatePos2(right, up, forward,DRrate,DLrate,Middlerate,URrate,ULrate, air.posX, air.posY, air.posZ);
		mc = Minecraft.getMinecraft();
	}

	public void updatePos2(Vec3 right,Vec3 up,Vec3 forward,Vec3 DRrate,Vec3 DLrate,Vec3 Middlerate,Vec3 URrate,Vec3 ULrate,double x,double y,double z) {
		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*DRrate.xCoord;
		this.RightVector.yCoord=right.yCoord*DRrate.xCoord;
		this.RightVector.zCoord=right.zCoord*DRrate.xCoord;
		this.UpVector.xCoord=up.xCoord*DRrate.yCoord;
		this.UpVector.yCoord=up.yCoord*DRrate.yCoord;
		this.UpVector.zCoord=up.zCoord*DRrate.yCoord;
		this.FwdVector.xCoord=forward.xCoord*DRrate.zCoord;
		this.FwdVector.yCoord=forward.yCoord*DRrate.zCoord;
		this.FwdVector.zCoord=forward.zCoord*DRrate.zCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord+this.FwdVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord+this.FwdVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord+this.FwdVector.zCoord);

		this.D_Right.xCoord=this.posx;
		this.D_Right.yCoord=this.posy;
		this.D_Right.zCoord=this.posz;

		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*DLrate.xCoord;
		this.RightVector.yCoord=right.yCoord*DLrate.xCoord;
		this.RightVector.zCoord=right.zCoord*DLrate.xCoord;
		this.UpVector.xCoord=up.xCoord*DLrate.yCoord;
		this.UpVector.yCoord=up.yCoord*DLrate.yCoord;
		this.UpVector.zCoord=up.zCoord*DLrate.yCoord;
		this.FwdVector.xCoord=forward.xCoord*DLrate.zCoord;
		this.FwdVector.yCoord=forward.yCoord*DLrate.zCoord;
		this.FwdVector.zCoord=forward.zCoord*DLrate.zCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord+this.FwdVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord+this.FwdVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord+this.FwdVector.zCoord);

		this.D_Left.xCoord=this.posx;
		this.D_Left.yCoord=this.posy;
		this.D_Left.zCoord=this.posz;

		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*URrate.xCoord;
		this.RightVector.yCoord=right.yCoord*URrate.xCoord;
		this.RightVector.zCoord=right.zCoord*URrate.xCoord;
		this.UpVector.xCoord=up.xCoord*URrate.yCoord;
		this.UpVector.yCoord=up.yCoord*URrate.yCoord;
		this.UpVector.zCoord=up.zCoord*URrate.yCoord;
		this.FwdVector.xCoord=forward.xCoord*URrate.zCoord;
		this.FwdVector.yCoord=forward.yCoord*URrate.zCoord;
		this.FwdVector.zCoord=forward.zCoord*URrate.zCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord+this.FwdVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord+this.FwdVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord+this.FwdVector.zCoord);

		this.U_Right.xCoord=this.posx;
		this.U_Right.yCoord=this.posy;
		this.U_Right.zCoord=this.posz;

		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*ULrate.xCoord;
		this.RightVector.yCoord=right.yCoord*ULrate.xCoord;
		this.RightVector.zCoord=right.zCoord*ULrate.xCoord;
		this.UpVector.xCoord=up.xCoord*ULrate.yCoord;
		this.UpVector.yCoord=up.yCoord*ULrate.yCoord;
		this.UpVector.zCoord=up.zCoord*ULrate.yCoord;
		this.FwdVector.xCoord=forward.xCoord*ULrate.zCoord;
		this.FwdVector.yCoord=forward.yCoord*ULrate.zCoord;
		this.FwdVector.zCoord=forward.zCoord*ULrate.zCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord+this.FwdVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord+this.FwdVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord+this.FwdVector.zCoord);

		this.U_Left.xCoord=this.posx;
		this.U_Left.yCoord=this.posy;
		this.U_Left.zCoord=this.posz;

		this.posx=x;
		this.posy=y;
		this.posz=z;
		this.RightVector.xCoord=right.xCoord*Middlerate.xCoord;
		this.RightVector.yCoord=right.yCoord*Middlerate.xCoord;
		this.RightVector.zCoord=right.zCoord*Middlerate.xCoord;
		this.UpVector.xCoord=up.xCoord*Middlerate.yCoord;
		this.UpVector.yCoord=up.yCoord*Middlerate.yCoord;
		this.UpVector.zCoord=up.zCoord*Middlerate.yCoord;
		this.FwdVector.xCoord=forward.xCoord*Middlerate.zCoord;
		this.FwdVector.yCoord=forward.yCoord*Middlerate.zCoord;
		this.FwdVector.zCoord=forward.zCoord*Middlerate.zCoord;
		this.posx+=(this.RightVector.xCoord+this.UpVector.xCoord+this.FwdVector.xCoord);
		this.posy+=(this.RightVector.yCoord+this.UpVector.yCoord+this.FwdVector.yCoord);
		this.posz+=(this.RightVector.zCoord+this.UpVector.zCoord+this.FwdVector.zCoord);

		this.MiddlePos.xCoord=this.posx;
		this.MiddlePos.yCoord=this.posy;
		this.MiddlePos.zCoord=this.posz;

		if(this.mc!=null) {
			this.eyePos.xCoord=mc.thePlayer.getPosition(1).xCoord;
			this.eyePos.yCoord=mc.thePlayer.getPosition(1).yCoord;
			this.eyePos.zCoord=mc.thePlayer.getPosition(1).zCoord;
		}
	}

    public Vec3 calculateCentroid(Vec3 p1,Vec3 p2,Vec3 p3,Vec3 p4) {
    	Vec3 centroid = Vec3.createVectorHelper(0, 0, 0);

    	centroid.xCoord= (p1.xCoord + p2.xCoord + p3.xCoord + p4.xCoord) / 4;
    	centroid.yCoord = (p1.yCoord + p2.yCoord + p3.yCoord + p4.yCoord) / 4;
        centroid.zCoord = (p1.zCoord + p2.zCoord + p3.zCoord + p4.zCoord) / 4;

        return centroid;
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


	public boolean update(Vec3 forward,Vec3 right,Vec3 up,Vec3 rate,Vec3 size,Vec3 tgtPos,double x,double y,double z) {
		this.updatePos(right, up, rate, size, x, y, z);
		GameSettings gameSettings = this.mc.gameSettings;
		boolean re=setPointPos(MiddlePos,forward,eyePos,tgtPos);
		return re;
	}

	public boolean update2(Vec3 right,Vec3 up,Vec3 forward,Vec3 tgtPos,double x,double y,double z) {
		this.updatePos2(right, up, forward,this.DRrate,this.DLrate,this.Middlerate,this.URrate,this.ULrate, x, y, z);
		GameSettings gameSettings = this.mc.gameSettings;
		boolean re=setPointPos(MiddlePos,forward,eyePos,tgtPos);
		return re;
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

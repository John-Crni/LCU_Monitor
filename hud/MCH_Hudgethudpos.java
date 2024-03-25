package mcheli.hud;

import mcheli.reHud.MCH_HUDCarsol;
import mcheli.reHud.vec2;
import net.minecraft.util.Vec3;

public class MCH_Hudgethudpos extends MCH_HudFunction{

	String TposX="0";
	String TposY="0";
	String TposZ="0";

	vec2 Vec=new vec2();

	private MCH_HUDCarsol HUd_Carsol=null;

    public MCH_Hudgethudpos(int fileLine,String data,MCH_Hudgethudpos HudClass,String tposx,String tposy,String tposz) {
        super(fileLine,data);
        this.TposX=tposx;
        this.TposY=tposy;
        this.TposZ=tposz;
		Vec3 right=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)0);
		Vec3 up=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)1);
		Vec3 forward=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)2);
		if(HudClass instanceof DefineFixedhudRoot) {
			((DefineFixedhudRoot)HudClass)
		}
		this.HUd_Carsol=new MCH_HUDCarsol(ac,ac.worldObj,right,up,forward,DRrate,DLrate,Middlerate,URrate,ULrate);
    }

	@Override
	public void execute() {
		//this.Vec=this.peac.getLandInDistance(player,this.Altitude+250,ac);
		Vec3 right=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)0);
		Vec3 up=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)1);
		Vec3 forward=this.getRotationMat((float)(-1*ac.getRotPitch()), (ac.getRotYaw()%360), -1*(ac.getRotRoll()%360),(byte)2);
		double x=calc(this.TposX);
		double y=calc(this.TposY);
		double z=calc(this.TposZ);
		Vec3 tgtpos=Vec3.createVectorHelper(x, y, z);
		if(this.HUd_Carsol.update2(right, up, forward,tgtpos, ac.posX,ac.posY,ac.posZ)) {
			this.Vec=this.HUd_Carsol.pos;
			for (int i=0;i<this.Argument.size();i++) {
	    		if(this.Argument.get(i) instanceof String) {
	    			switch(i) {
	    				case 1:updateVarMapItem(this.Argument.get(i), this.Vec.x);break;
	    				case 2:updateVarMapItem(this.Argument.get(i), this.Vec.y);break;
	    			}
	    		}
	    	}
		}

	}

    public Vec3 calculateCentroid(Vec3 p1,Vec3 p2,Vec3 p3,Vec3 p4) {
    	Vec3 centroid = Vec3.createVectorHelper(0, 0, 0);

    	centroid.xCoord= (p1.xCoord + p2.xCoord + p3.xCoord + p4.xCoord) / 4;
    	centroid.yCoord = (p1.yCoord + p2.yCoord + p3.yCoord + p4.yCoord) / 4;
        centroid.zCoord = (p1.zCoord + p2.zCoord + p3.zCoord + p4.zCoord) / 4;

        return centroid;
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

package mcheli.hud;

import java.util.ArrayList;
import java.util.List;

import mcheli.reHud.vec2;
import net.minecraft.util.Vec3;

public class DefineFixedhudRoot extends DefineHudEntitiy{

	public Vec3 pos=Vec3.createVectorHelper(1, 0, 0);

	public vec2 size=new vec2();

	public List<MCH_HUDfixed> fixedHudlist;

	public double[][] hudCornerPos={{0,0,0},{0,0,0},{0,0,0},{0,0,0}};

	public boolean CornerMode=false;


	public DefineFixedhudRoot(String name,String x,String y,String z,String sizex,String sizey) {
		super(name);
		this.pos.xCoord=this.tofloat(x);
		this.pos.yCoord=this.tofloat(y);
		this.pos.zCoord=this.tofloat(z);
		this.size.x=this.tofloat(sizex);
		this.size.y=this.tofloat(sizey);
		this.fixedHudlist=new ArrayList();
	}

	public DefineFixedhudRoot(String name,double[][] hCp) {
		super(name);
		this.CornerMode=true;
		this.hudCornerPos[0][0]=-1*hCp[0][0];
		this.hudCornerPos[0][1]=hCp[0][1];
		this.hudCornerPos[0][2]=hCp[0][2];

		this.hudCornerPos[1][0]=-1*hCp[1][0];
		this.hudCornerPos[1][1]=hCp[1][1];
		this.hudCornerPos[1][2]=hCp[1][2];

		this.hudCornerPos[2][0]=-1*hCp[2][0];
		this.hudCornerPos[2][1]=hCp[2][1];
		this.hudCornerPos[2][2]=hCp[2][2];

		this.hudCornerPos[3][0]=-1*hCp[3][0];
		this.hudCornerPos[3][1]=hCp[3][1];
		this.hudCornerPos[3][2]=hCp[3][2];

		this.fixedHudlist=new ArrayList();
	}

}

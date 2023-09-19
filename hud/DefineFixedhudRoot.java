package mcheli.hud;

import mcheli.reHud.vec2;
import net.minecraft.util.Vec3;

public class DefineFixedhudRoot extends DefineHudEntitiy{

	public Vec3 pos=Vec3.createVectorHelper(1, 0, 0);

	public vec2 size=new vec2();

	public DefineFixedhudRoot(String name,float x,float y,float z,float sizex,float sizey) {
		super(name);
		this.pos.xCoord=x;
		this.pos.yCoord=y;
		this.pos.zCoord=z;
		this.size.x=sizex;
		this.size.y=sizey;
	}

}

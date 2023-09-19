package mcheli.hud;

import mcheli.reHud.vec2;

public class DefineFixedhuds extends DefineHudEntitiy{

	public DefineFixedhudRoot parent=null;

	public vec2 pos=new vec2();

	public vec2 size=new vec2();

	public float rotation=0;

	public DefineFixedhuds(String n,DefineFixedhudRoot dfr) {
		super(n);
		this.parent=dfr;
	}

}

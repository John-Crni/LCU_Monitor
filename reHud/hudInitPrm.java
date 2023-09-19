package mcheli.reHud;

public class hudInitPrm {

	public vec2 Scale=new vec2(1,1);

	public vec2 Rotate=new vec2();

	public vec2 Transform=new vec2();

	public vec2 centerPos=new vec2();

	public boolean isCenter=false;

	public float rot=0;

	private int textureWidth=0;

	private int textureHeight=0;

	public hudInitPrm(vec2...center) {
		if(center.length>0) {
			this.isCenter=true;
			this.centerPos=center[0];
		}
	}


}

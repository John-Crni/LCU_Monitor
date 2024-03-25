package mcheli.reHud;

public class HudTexCoord {

	private vec2 Pos;

	private vec2 TexCoord;

	public vec2 WorldPos;


	public HudTexCoord[] getArray(int num) {
		HudTexCoord[] re=new HudTexCoord[num];
		for(int i=0;i<num;i++) {
			re[i]=new HudTexCoord();
		}
		return re;
	}

	public vec2 getPos() {
		return this.Pos;
	}

	public vec2 getWPos() {
		return this.WorldPos;
	}

	public vec2 getTexPos() {
		return this.TexCoord;
	}


	public vec2 getTexCoord() {
		return this.TexCoord;
	}

	public HudTexCoord() {
		this.Pos=new vec2();
		this.TexCoord=new vec2();
		this.WorldPos=new vec2();
	}

	public HudTexCoord(vec2 center,vec2 pos) {
		this.Pos=new vec2();
		this.TexCoord=new vec2();
		this.Pos.setClone(pos);
		this.TexCoord.setClone(center);
	}


	public HudTexCoord(HudTexCoord  clone) {
		this.Pos.setClone(clone.Pos);
		this.TexCoord.setClone(clone.TexCoord);
	}

	public void setClone(HudTexCoord  clone) {
		this.Pos.setClone(clone.Pos);
		this.TexCoord.setClone(clone.TexCoord);
	}

	public void setPos(vec2 c) {
		this.Pos.setClone(c);
	}

	public void setWorld(vec2 c) {
		this.WorldPos.setClone(c);

	}

	public void setTexCoord(vec2 c) {
		this.TexCoord.setClone(c);
	}

}

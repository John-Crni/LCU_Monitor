package mcheli.reHud;

public class HudTexPoint {

	public vec2 Pos;


	public HudTexPoint() {
		this.Pos=new vec2();
	}

	public HudTexPoint(vec2 pos) {
		this.Pos=pos;
	}

	public void setPos(vec2 p) {
		this.Pos=p;
	}


}

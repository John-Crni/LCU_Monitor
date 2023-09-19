package mcheli.reHud;

public class Square {

	 public HudTexCoord P1;

	 public HudTexCoord P2;

	 public HudTexCoord P3;

	 public HudTexCoord P4;

	 public Square() {
		 this.init();
	 }

	 private void init() {
		 this.P1=new HudTexCoord();
		 this.P2=new HudTexCoord();
		 this.P3=new HudTexCoord();
		 this.P4=new HudTexCoord();
	 }

	 public void setSquareAuto() {
		 this.P1.setPos(new vec2(this.P4.getPos().x,this.P2.getPos().y));
		 this.P3.setPos(new vec2(this.P2.getPos().x,this.P4.getPos().y));
	 }




}

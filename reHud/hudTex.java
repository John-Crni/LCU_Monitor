package mcheli.reHud;

/**
 *
 * @author yasio
 * 正四角形しか受け付けない
 *
 */
public class hudTex {

	private HudTexPoint P1=new HudTexPoint();//左上

	private HudTexPoint P2=new HudTexPoint();//右上

	private HudTexPoint P3=new HudTexPoint();//右下

	private HudTexPoint P4=new HudTexPoint();//左下


	private vec2 TexCord1=new vec2();

	private vec2 TexCord2=new vec2();

	private vec2 TexCord3=new vec2();

	private vec2 TexCord4=new vec2();


	public  vec2 centerPos=new vec2();

	public vec2[] CalcPoint;

	public CalcCirclePoint Calc;

	public hudTex() {
		this.Calc=new CalcCirclePoint();
	}

	public hudTex(HudTexPoint p1,HudTexPoint p2,HudTexPoint p3,HudTexPoint p4) {
		this.CalcPoint= new vec2[4];
		this.setPoint2Square(p1, p2, p3, p4);
		//this.setCenterPos();
		//this.centerPos=new vec2(0.585f,0.585f);
		this.Calc=new CalcCirclePoint();
		this.CalcPoint[0]=this.P1.Pos;
		this.CalcPoint[1]=this.P2.Pos;
		this.CalcPoint[2]=this.P3.Pos;
		this.CalcPoint[3]=this.P4.Pos;
	}

	public void setTexPos(vec2 p1,vec2 p2,vec2 p3,vec2 p4) {
		this.setPoint2Square2(p1, p2, p3, p4);
		this.setCenterPos();
	}

	private void setPoint2Square2(vec2 p1,vec2 p2,vec2 p3,vec2 p4) {

		//float minX=p1.Pos.RvCompareXmin(p2.Pos.RvCompareXmin(p3.Pos.RvCompareXmin(p4.Pos.x)));
		float minX=p3.RvCompareXmin(p4.x);
		minX=p2.RvCompareXmin(minX);
		minX=p1.RvCompareXmin(minX);


		//float  minY=p1.Pos.RvCompareYmin(p2.Pos.RvCompareYmin(p3.Pos.RvCompareYmin(p4.Pos.y)));

		float minY=p3.RvCompareYmin(p4.y);
		minY=p2.RvCompareYmin(minY);
		minY=p1.RvCompareYmin(minY);


		vec2 minVec=new vec2(minX,minY);

		this.TexCord4=minVec;

		if(minVec.x==p1.x&&minVec.y<p1.y) {
			this.TexCord1=p1;
		}
		if(minVec.x==p2.x&&minVec.y<p2.y) {
			this.TexCord1=p2;
		}
		if(minVec.x==p3.x&&minVec.y<p3.y) {
			this.TexCord1=p3;
		}
		if(minVec.x==p4.x&&minVec.y<p4.y) {
			this.TexCord1=p4;
		}

		if(this.TexCord1.y==p1.y&&this.TexCord1.x<p1.x) {
			this.TexCord2=p1;
		}
		if(this.TexCord1.y==p2.y&&this.TexCord1.x<p2.x) {
			this.TexCord2=p2;
		}
		if(this.TexCord1.y==p3.y&&this.TexCord1.x<p3.x) {
			this.TexCord2=p3;
		}
		if(this.TexCord1.y==p4.y&&this.TexCord1.x<p4.x) {
			this.TexCord2=p4;
		}

		if(this.TexCord2.y>p1.y&&this.TexCord2.x==p1.x) {
			this.TexCord3=p1;
		}
		if(this.TexCord2.y>p2.y&&this.TexCord2.x==p2.x) {
			this.TexCord3=p2;
		}
		if(this.TexCord2.y>p3.y&&this.TexCord2.x==p3.x) {
			this.TexCord3=p3;
		}
		if(this.TexCord2.y>p4.y&&this.TexCord2.x==p4.x) {
			this.TexCord3=p4;
		}

	}


	private void setPoint2Square(HudTexPoint p1,HudTexPoint p2,HudTexPoint p3,HudTexPoint p4) {

		//float minX=p1.Pos.RvCompareXmin(p2.Pos.RvCompareXmin(p3.Pos.RvCompareXmin(p4.Pos.x)));
		float minX=p3.Pos.RvCompareXmin(p4.Pos.x);
		minX=p2.Pos.RvCompareXmin(minX);
		minX=p1.Pos.RvCompareXmin(minX);


		//float  minY=p1.Pos.RvCompareYmin(p2.Pos.RvCompareYmin(p3.Pos.RvCompareYmin(p4.Pos.y)));

		float minY=p3.Pos.RvCompareYmin(p4.Pos.y);
		minY=p2.Pos.RvCompareYmin(minY);
		minY=p1.Pos.RvCompareYmin(minY);


		vec2 minVec=new vec2(minX,minY);

		this.P4.Pos=minVec;

		if(minVec.x==p1.Pos.x&&minVec.y<p1.Pos.y) {
			P1=p1;
		}
		if(minVec.x==p2.Pos.x&&minVec.y<p2.Pos.y) {
			P1=p2;
		}
		if(minVec.x==p3.Pos.x&&minVec.y<p3.Pos.y) {
			P1=p3;
		}
		if(minVec.x==p4.Pos.x&&minVec.y<p4.Pos.y) {
			P1=p4;
		}

		if(P1.Pos.y==p1.Pos.y&&P1.Pos.x<p1.Pos.x) {
			P2=p1;
		}
		if(P1.Pos.y==p2.Pos.y&&P1.Pos.x<p2.Pos.x) {
			P2=p2;
		}
		if(P1.Pos.y==p3.Pos.y&&P1.Pos.x<p3.Pos.x) {
			P2=p3;
		}
		if(P1.Pos.y==p4.Pos.y&&P1.Pos.x<p4.Pos.x) {
			P2=p4;
		}

		if(P2.Pos.y>p1.Pos.y&&P2.Pos.x==p1.Pos.x) {
			P3=p1;
		}
		if(P2.Pos.y>p2.Pos.y&&P2.Pos.x==p2.Pos.x) {
			P3=p2;
		}
		if(P2.Pos.y>p3.Pos.y&&P2.Pos.x==p3.Pos.x) {
			P3=p3;
		}
		if(P2.Pos.y>p4.Pos.y&&P2.Pos.x==p4.Pos.x) {
			P3=p4;
		}

	}

	private void setCenterPos() {
		this.centerPos.x=(this.TexCord1.x+this.TexCord2.x)/2;
		this.centerPos.y=(this.TexCord1.y+this.TexCord4.y)/2;
	}

	/**
	 * テクスチャの原点を中心にして回す
	 */
	public vec2[] rotateHud(float rot) {
		this.CalcPoint[0]=this.Calc.Calc_cPoint(this.centerPos,this.P1.Pos,rot);
		this.CalcPoint[1]=this.Calc.Calc_cPoint(this.centerPos,this.P2.Pos,rot);
		this.CalcPoint[2]=this.Calc.Calc_cPoint(this.centerPos,this.P3.Pos,rot);
		this.CalcPoint[3]=this.Calc.Calc_cPoint(this.centerPos,this.P4.Pos,rot);

		this.P1.Pos=this.CalcPoint[0];
		this.P2.Pos=this.CalcPoint[1];
		this.P3.Pos=this.CalcPoint[2];
		this.P4.Pos=this.CalcPoint[3];

		return this.CalcPoint;
	}

	public vec2[] rvVec2Aray() {
		return this.CalcPoint;
	}

}

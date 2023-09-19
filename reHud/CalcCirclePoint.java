package mcheli.reHud;

public class CalcCirclePoint {

	public vec2 Calc_cPoint(vec2 centerPos,vec2 tgtPos,float Rot) {
		float NormX=tgtPos.x-centerPos.x;
		float NormY=tgtPos.y-centerPos.y;
		double Cos=Math.cos(Rot);
		double Sin=Math.sin(Rot);

		double CalcX= ((NormX*Cos)-(NormY*Sin))+centerPos.x;
		double CalcY= ((NormX*Sin)+(NormY*Cos))+centerPos.y;


		return new vec2((float)CalcX,(float) CalcY);
	}

}

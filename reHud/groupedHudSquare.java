package mcheli.reHud;

import java.util.List;

public class groupedHudSquare extends HudSquare{

	vec2 trashVec1=new vec2();

	vec2 trashVec2=new vec2();


	public groupedHudSquare(List<HudSquare> hud_compornents) {
		this.hudGrouped(hud_compornents, hud_compornents.get(0), (byte)0);

		this.update_GroupLeaderCornerPos(true);

		this.setSquares();
		this.setSize();
		this.setCenterPos();

		this.Points2output[0].setClone(this.P1.getPos());
		this.Points2output[1].setClone(this.P2.getPos());
		this.Points2output[2].setClone(this.P3.getPos());
		this.Points2output[3].setClone(this.P4.getPos());

		this.Stats.Position=new vec2(0.5f,0.5f);
		this.WorldCenter=this.getCenterPos();
	}

	/**
	 * グループ用HUDのリーダーの各変を更新する関数　多分結構重要
	 * @param isinit グループ用HUDのリーダーを初期化するための引数
	 */
	private void update_GroupLeaderCornerPos(boolean isinit) {
		float[] poss=this.getGrupedAroundpos();

		this.P1.getPos().x=poss[0];
		this.P1.getPos().y=poss[3];

		this.P2.getPos().x=poss[2];
		this.P2.getPos().y=poss[3];

		this.P3.getPos().x=poss[2];
		this.P3.getPos().y=poss[1];

		this.P4.getPos().x=poss[0];
		this.P4.getPos().y=poss[1];
		if(isinit) {
			this.P1.getTexCoord().x=poss[0];
			this.P1.getTexCoord().y=poss[3];
			this.P2.getTexCoord().x=poss[2];
			this.P2.getTexCoord().y=poss[3];
			this.P3.getTexCoord().x=poss[2];
			this.P3.getTexCoord().y=poss[1];
			this.P4.getTexCoord().x=poss[0];
			this.P4.getTexCoord().y=poss[1];
		}else {
			this.setSize();
			this.setCenterPos();
			this.Stats.Position=this.getCenterPos();
			this.WorldCenter=this.getCenterPos();
			this.P1.getTexCoord().x=poss[0];
			this.P1.getTexCoord().y=poss[3];
			this.P2.getTexCoord().x=poss[2];
			this.P2.getTexCoord().y=poss[3];
			this.P3.getTexCoord().x=poss[2];
			this.P3.getTexCoord().y=poss[1];
			this.P4.getTexCoord().x=poss[0];
			this.P4.getTexCoord().y=poss[1];

			this.P1.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P1.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P2.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P2.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P4.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P4.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P3.getTexCoord().x=0;
			this.P3.getTexCoord().y=0;
		}
	}


	/**
	 * テクスチャの原点を中心にして回す
	 */
	@Override
	public void rotateHud(float rot,vec2... centerpos) {
		this.update_GroupLeaderCornerPos(false);

		vec2 center=new vec2();
		center.setClone(this.centerPos);
		boolean roop=true;

		this.Points2output[0]=this.Calc.Calc_cPoint(center,this.P1.getPos(),rot);
		this.Points2output[1]=this.Calc.Calc_cPoint(center,this.P2.getPos(),rot);
		this.Points2output[2]=this.Calc.Calc_cPoint(center,this.P3.getPos(),rot);
		this.Points2output[3]=this.Calc.Calc_cPoint(center,this.P4.getPos(),rot);
		HudSquare nexthud=this.pairHudSquare;
		while(roop) {
			if(this.GroupedID==nexthud.GroupedID)break;
			nexthud.rotateHud(rot, center);
			nexthud=nexthud.pairHudSquare;
		}

		this.Stats.Rotate=rot;

		this.set2Point();
	}

	/**
	 *　HUDの指定した座標(X軸に対しての割合,Y軸に対しての割合)にテクスチャを置く
	 * めちゃくちゃ重要
	 * @param tgtPoint ※WorldPos
	 */
	@Override
	public void Transform2Point(vec2 tgtPoint) {
		this.update_GroupLeaderCornerPos(false);
		this.scaleHud(this.Stats.Scale.x, this.Stats.Scale.y);

		vec2 StatsPosDiff=new vec2(tgtPoint.x-this.Stats.Position.x,tgtPoint.y-this.Stats.Position.y);


		vec2 WorldedP2=this.getWorldPos(this.P2.getPos());


		///**
		float X=((tgtPoint.x-WorldedP2.x)/this.Stats.Scale.x);
		float Y=((tgtPoint.y-WorldedP2.y)/this.Stats.Scale.y);

		X*=-1;
		Y*=-1;

		vec2 truePos=new vec2(this.P2.getPos().x+(X*this.P2.getTexCoord().x),this.P2.getPos().y+(Y*this.P2.getTexCoord().y));
		vec2 diff=this.P2.getPos().getdiff2vec(truePos);


	//	MCH_Lib.Log("\nWorldedP2="+X);

		this.P2.getPos().setClone(truePos);
		this.P1.getPos().setSumVec(diff);
		this.P3.getPos().setSumVec(diff);
		this.P4.getPos().setSumVec(diff);
		///**



		vec2 diff2center=new vec2(-1*this.P2.getTexCoord().x/2,-1*this.P2.getTexCoord().y/2);

		this.P1.getPos().setSumVec(diff2center);
		this.P2.getPos().setSumVec(diff2center);
		this.P3.getPos().setSumVec(diff2center);
		this.P4.getPos().setSumVec(diff2center);

		this.Stats.Position.x=tgtPoint.x;
		this.Stats.Position.y=tgtPoint.y;

		this.WorldCenter.x=tgtPoint.x;
		this.WorldCenter.y=tgtPoint.y;
		boolean roop=true;
		HudSquare nexthud=this.pairHudSquare;
		while(roop) {
			if(this.GroupedID==nexthud.GroupedID)break;
			nexthud.Transform2Point4Group(diff, diff2center, StatsPosDiff);
			nexthud=nexthud.pairHudSquare;
		}

		//**/

		//MCH_Lib.Log("\nthis.Stats.Position="+this.Stats.Position.RvText());


		this.set2Array();
	}









}

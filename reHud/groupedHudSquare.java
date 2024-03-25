package mcheli.reHud;

import java.util.ArrayList;
import java.util.List;

import mcheli.MCH_Lib;
import net.minecraft.client.Minecraft;

public class groupedHudSquare extends HudSquare{

	vec2 trashVec1=new vec2();

	vec2 trashVec2=new vec2();

	List<HudSquare> hud_compornent;


	public groupedHudSquare(List<HudSquare> hud_compornents) {
		this.hud_compornent=new ArrayList();
		for(int i=0;i<hud_compornents.size();i++) {
			this.hud_compornent.add(hud_compornents.get(i));
		}

		MCH_Lib.Log("[HudSquare nexthud]NOW_POS1="+this.hud_compornent.get(0).getPointCoords());
		this.hudGrouped(this.hud_compornent, this.hud_compornent.get(0), (byte)0);
		MCH_Lib.Log("[HudSquare nexthud]NOW_POS2="+this.hud_compornent.get(0).getPointCoords());

		this.update_GroupLeaderCornerPos();

		//this.setSquares();

		//this.setSize();

		//this.setCenterPos();

		//this.Points2output[0].setClone(this.P1.getWPos());
		//this.Points2output[1].setClone(this.P2.getWPos());
		//this.Points2output[2].setClone(this.P3.getWPos());
		//this.Points2output[3].setClone(this.P4.getWPos());

		//this.Stats.Position=this.getCenterPos();

		this.WorldCenter.setClone(this.Stats.Position);
	}

	@Override
	 public void Update(vec2 size,vec2 pos,float rot, boolean isrotpos,vec2 rotpos,Minecraft mc) {
		this.mc=mc;
		this.Stats.Rotate=0;
		this.update_GroupLeaderCornerPos();
		this.TransformHud(pos,rot,isrotpos,rotpos);
	 }

	@Override
	 public void drawHud() {
		this.isGrouped=false;


	 		if(this.isExecuteok()) {
	 			//MCH_Lib.Log("drawHud!!!!!!!!!!!");
	 			boolean roop=true;
	 			HudSquare nexthud=this.pairHudSquare;
	 			while(roop) {
	 				nexthud.isExecute=true;
	 				nexthud.isGrouped=false;
	 				nexthud.drawHud();
	 				nexthud.isGrouped=true;
	 				nexthud=nexthud.pairHudSquare;
	 				if(this.GroupedID==nexthud.GroupedID) {
	 					roop=false;
	 					break;
	 				}
	 			}

	 			this.setExecuteEnd();

	 		}

	}


	/**
	 * グループ用HUDのリーダーの各変を更新する関数　多分結構重要
	 * @param isinit グループ用HUDのリーダーを初期化するための引数
	 *
	  * re[0]=minx
	  * re[1]=miny
	  * re[2]=maxx
	  * re[3]=maxy
	  * @return
	 */
	private void update_GroupLeaderCornerPos() {
		float[] poss=this.updateGroupedPos();

		this.P1.getWPos().x=poss[0];
		this.P1.getWPos().y=poss[3];

		this.P2.getWPos().x=poss[2];
		this.P2.getWPos().y=poss[3];

		this.P3.getWPos().x=poss[2];
		this.P3.getWPos().y=poss[1];

		this.P4.getWPos().x=poss[0];
		this.P4.getWPos().y=poss[1];

		this.Stats.Scale.x=this.P2.getWPos().x-this.P1.getWPos().x;
		this.Stats.Scale.y=this.P2.getWPos().y-this.P3.getWPos().y;
		this.Stats.Position.x=(this.P2.getWPos().x+this.P1.getWPos().x)/2;
		this.Stats.Position.y=(this.P2.getWPos().y+this.P4.getWPos().y)/2;
		this.WorldCenter.setClone(this.Stats.Position);

		/*

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

			/**
			this.P1.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P1.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P2.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P2.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P4.getTexCoord().x-=this.P3.getTexCoord().x;
			this.P4.getTexCoord().y-=this.P3.getTexCoord().y;
			this.P3.getTexCoord().x=0;
			this.P3.getTexCoord().y=0;
			*/
		//}

	}


	/**
	 * テクスチャの原点を中心にして回す
	 */
	@Override
	public void rotateHud(float rot,boolean... rotateByGroup) {
		//this.update_GroupLeaderCornerPos(false,false);

		boolean roop=true;

		HudSquare nexthud=this.pairHudSquare;

		while(roop) {
			nexthud.RotateByPosition(this.WorldCenter,rot);
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}
		}

		if (rotateByGroup.length==0) {
			this.Stats.Rotate=rot;
		}

		//this.set2Point();
	}

	/**
	 *　HUDの指定した座標(X軸に対しての割合,Y軸に対しての割合)にテクスチャを置く
	 * めちゃくちゃ重要
	 * @param tgtPoint
	 */
	@Override
	public void Transform2PointNew() {
		MCH_Lib.Log("Transform2PointNew="+this.WorldCenter.RvText());
		vec2[] childDiffs=new vec2[this.hud_compornent.size()];

		for(int i=0;i<this.hud_compornent.size();i++) {
			childDiffs[i]=this.getCenter().getdiff2vec(this.hud_compornent.get(i).getCenter());
			vec2 diff=childDiffs[i];
			childDiffs[i].setClone(this.Stats.Position.getSumvec(diff));
		}

		boolean roop=true;
		HudSquare nexthud=this.pairHudSquare;

		int i=0;

		while(roop) {
			nexthud.Transform2Point(childDiffs[i]);
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}else {
				i+=1;
			}

		}
		this.WorldCenter.setClone(this.Stats.Position);
		this.rotateHud(test);
		this.set2Array();
	}

	/**
	 *　HUDの指定した座標(X軸に対しての割合,Y軸に対しての割合)にテクスチャを置く
	 * めちゃくちゃ重要
	 * @param tgtPoint ※WorldPos
	 */
	@Override
	public void Transform2Point(vec2 tgtPoint){
		this.update_GroupLeaderCornerPos();

		//this.scaleHud(this.Stats.Scale.x, this.Stats.Scale.y);

		//MCH_Lib.Log("GROUP_CENTER="+this.WorldCenter.RvText());
		//MCH_Lib.Log("TGT_POS="+tgtPoint.RvText());
		//MCH_Lib.Log("GROUP_SCALE="+this.Stats.Scale.RvText());

		//vec2 StatsPosDiff=new vec2(tgtPoint.x-this.Stats.Position.x,tgtPoint.y-this.Stats.Position.y);

		vec2[] childDiffs=new vec2[this.hud_compornent.size()];

		for(int i=0;i<this.hud_compornent.size();i++) {
			childDiffs[i]=this.getCenter().getdiff2vec(this.hud_compornent.get(i).getCenter());
			vec2 diff=childDiffs[i];
			childDiffs[i].setClone(tgtPoint.getSumvec(diff));
		}

		//MCH_Lib.Log("DIFF="+StatsPosDiff.RvText());

		/*
		vec2 WorldedP2=this.P2.getPos();
		///**
		float X=((tgtPoint.x-WorldedP2.x)/this.Stats.Scale.x);
		float Y=((tgtPoint.y-WorldedP2.y)/this.Stats.Scale.y);

		X*=-1;
		Y*=-1;

		vec2 truePos=new vec2(this.P2.getPos().x+(X*this.P2.getTexCoord().x),this.P2.getPos().y+(Y*this.P2.getTexCoord().y));
		vec2 diff=this.P2.getPos().getdiff2vec(truePos);


		//MCH_Lib.Log("\nWorldedP2="+X);
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
		*/

		boolean roop=true;
		HudSquare nexthud=this.pairHudSquare;

		//MCH_Lib.Log("---------------------------------GROUPLEADER---------------------------------");

		int i=0;

		while(roop) {
			nexthud.Transform2Point(childDiffs[i]);
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}else {
				i+=1;
			}

		}

		//MCH_Lib.Log("P1:WPOS="+this.P1.getPos().RvText());
		//MCH_Lib.Log("P2:WPOS="+this.P2.getPos().RvText());
		//MCH_Lib.Log("P3:WPOS="+this.P3.getPos().RvText());
		//MCH_Lib.Log("P4:WPOS="+this.P4.getPos().RvText());


		//MCH_Lib.Log("------------------------------GROUPLEADER-----END-----------------------------");
		this.WorldCenter.setClone(tgtPoint);
		this.rotateHud(test);
		MCH_Lib.Log("[TEST_ROT]:"+test);

		test+=0.1;
		if(test>=5) {
			test=0;
		}
		this.set2Array();
	}

	float test=0;









}

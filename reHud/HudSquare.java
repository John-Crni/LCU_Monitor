package mcheli.reHud;

import java.util.List;

import org.lwjgl.opengl.GL11;
import org.lwjgl.opengl.GL13;

import mcheli.MCH_Lib;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.util.ResourceLocation;

public class HudSquare {

	 protected String Texname="b";

	 protected double left;

	 protected double width;

	 protected double top;

	 protected double height;

	 protected HudTexCoord P1;

	 protected HudTexCoord P2;

	 protected HudTexCoord P3;

	 protected HudTexCoord P4;


	 protected vec2 centerPos;

	 protected vec2 texSize;


	 protected String texName;

	 protected vec2[] Points2output;

	 protected CalcCirclePoint Calc;

	 protected HudStats Stats;

	 protected vec2 LocalCenter;

	 protected vec2 WorldCenter;

	 /**
	  * グループ化関係
	  */

	 public HudSquare pairHudSquare=null;

	 public byte GroupedID=-1;

	 public boolean isGrouped=false;

	 /**
	  * グループ化した時の中心座標(ワールド座標系)
	  */
	 protected vec2 GrupedCenterPos=new vec2();

	 public boolean groupedhudcommander=false;

	 public boolean isExecute=false;

	 public boolean isExecute_end=false;

	 private boolean useCornerPos=false;

	 private double[][] cornerpos={{0,0,0},{0,0,0},{0,0,0},{0,0,0}};


	 public Minecraft mc;



	 public vec2 getCenter() {
		 return this.Stats.Position;
	 }

	 public void Update(vec2 size,vec2 pos,float rot, boolean isrotpos,vec2 rotpos,Minecraft mc) {
		 this.mc=mc;
		 this.Stats.Rotate=0;
		 this.Stats.Scale.setClone(size);
		 this.Stats.Position.setClone(pos);
		 this.TransformHud(pos,rot,isrotpos,rotpos);
	 }


	 public void drawHud() {

		 		//MCH_Lib.Log("isExecuteok="+this.isExecuteok());

		 		if(this.isExecuteok()) {
		 			this.Transform2PointNew();
		 			GL11.glEnable(GL11.GL_LIGHTING);
		 			GL11.glEnable(GL11.GL_LIGHT0);
		 			GL11.glShadeModel(GL11.GL_SMOOTH);
		 			GL11.glPushMatrix();


	        		this.mc.renderEngine.bindTexture(new ResourceLocation("mcheli",  "textures/gui/"+this.texName+".png"));
	        		//MCH_Lib.Log("P4="+this.getP4().RvText());


	        		//GL11.glBindTexture(GL11.GL_TEXTURE_2D, fb.pixelBuffer);


	        		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_S, GL13.GL_CLAMP_TO_BORDER);
	        		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_T, GL13.GL_CLAMP_TO_BORDER);

	        		// テクスチャの拡大時にピクセルを線形補間するように設定する
	        		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_LINEAR);

	        		// テクスチャの縮小時にピクセルを線形補間するように設定する
	        		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_LINEAR);

	        		if(this.useCornerPos) {
	        			GL11.glTranslated(0,0,0);
	        		}else {
	        			GL11.glTranslated(this.getLeft() + this.getWidth() / 2.0D, this.getTop() + this.getHeight() / 2.0D, 0.0D);
	        		}
	        		GL11.glRotatef(0, 0.0F, 0.0F, 1.0F);


	        		Tessellator tessellator = Tessellator.instance;// (double) this.zLevel

	        		tessellator.startDrawingQuads();

	        		/**
	        		 * 中心からの相対距離で図形を生成している
	        		 * なお、1は恐らくマイクラ内での1m
	        		 *         		MCH_Lib.Log("P1="+this.getP1().RvText());

	        		MCH_Lib.Log("P2="+this.getP2().RvText());
	        		MCH_Lib.Log("P3="+this.getP3().RvText());
	        		MCH_Lib.Log("P4="+this.getP4().RvText());
	        		 */
	        		if(this.useCornerPos) {

		        		tessellator.addVertexWithUV(this.cornerpos[0][0], this.cornerpos[0][1],this.cornerpos[0][2], (double)this.getP1().x ,(double)this.getP1().y);//UpLeft

		        		tessellator.addVertexWithUV(this.cornerpos[1][0], this.cornerpos[1][1],this.cornerpos[1][2],  (double)this.getP2().x ,(double)this.getP2().y);//UR

		        		tessellator.addVertexWithUV(this.cornerpos[2][0], this.cornerpos[2][1],this.cornerpos[2][2],  (double)this.getP3().x ,(double)this.getP3().y);//DowmLeft

		        		tessellator.addVertexWithUV(this.cornerpos[3][0], this.cornerpos[3][1],this.cornerpos[3][2],(double)this.getP4().x ,(double)this.getP4().y);//DR
	    	        }else {
		        		tessellator.addVertexWithUV(-this.getWidth() / 2.0D, this.getHeight() / 2.0D, 2, (double)this.getP1().x ,(double)this.getP1().y);//UpLeft

		        		tessellator.addVertexWithUV(this.getWidth() / 2.0D, this.getHeight() / 2.0D, 2,  (double)this.getP2().x ,(double)this.getP2().y);//UR

		        		tessellator.addVertexWithUV(this.getWidth() / 2.0D, -this.getHeight() / 2.0D,2,  (double)this.getP3().x ,(double)this.getP3().y);//DowmLeft

		        		tessellator.addVertexWithUV(-this.getWidth() / 2.0D, -this.getHeight() / 2.0D,2,(double)this.getP4().x ,(double)this.getP4().y);//DR
	        		}


	        		//MCH_Lib.Log("P1="+this.getP1().RvText()+"P2="+this.getP2().RvText()+"P3="+this.getP3().RvText()+"P4="+this.getP4().RvText());

	        		tessellator.draw();

	        		GL11.glPopMatrix();

	        		this.setExecuteEnd();
	        		this.P1.setWorld(new vec2());
	        		this.P2.setWorld(new vec2());
	        		this.P3.setWorld(new vec2());
	        		this.P4.setWorld(new vec2());

		 		}


	    }

	 protected boolean isExecuteok() {
		 boolean re=false;
		 if(this.isExecute&&!this.isGrouped) {
			 re=true;
			 this.isExecute_end=false;
		 }
		 if(!this.isExecute&&!this.isExecute_end) {
			 this.isExecute_end=true;
		 }
		 return re;
	 }

	 protected void setExecuteEnd() {
		 this.isExecute_end=true;
	 }

	 public String getPointCoords() {
		 return "P1="+this.P1.getPos().RvText()+"\n P2="+this.P2.getPos().RvText()+"\n P3="+this.P3.getPos().RvText()+"\n P4="+this.P4.getPos().RvText();
	 }

	 public void SetClone(HudSquare clone) {
		 this.left=clone.left;
		 this.width=clone.width;
		 this.top=clone.top;
		 this.height=clone.height;
		 this.P1.setClone(clone.P1);
		 this.P2.setClone(clone.P2);
		 this.P3.setClone(clone.P3);
		 this.P4.setClone(clone.P4);
		 this.setSize();
		 this.centerPos.setClone(clone.centerPos);
		 int len=clone.Points2output.length;
		 this.Points2output=new vec2().getArray(len);
		 for(int i=0;i<len;i++) {
			 this.Points2output[i].setClone(clone.Points2output[i]);
		 }
		 this.Calc=clone.Calc;
	 }

	 public HudSquare() {
		 this.init();
	 }

	 public HudSquare(HudTexCoord p1,HudTexCoord p2,HudTexCoord p3,HudTexCoord p4) {
		 this.init();
		 this.P1.setClone(p1);
		 this.P2.setClone(p2);
		 this.P3.setClone(p3);
		 this.P4.setClone(p4);
		 this.setSquares();
		 this.setSize();
		 this.setCenterPos();
		 this.Points2output[0].setClone(this.P1.getPos());
		 this.Points2output[1].setClone(this.P2.getPos());
		 this.Points2output[2].setClone(this.P3.getPos());
		 this.Points2output[3].setClone(this.P4.getPos());
	 }

	 /**
	  * グループHUDを生成する関数
	  * @param hud_compornents
	  * @param nextComponent
	  * @param id
	  */
	 protected void hudGrouped(List<HudSquare> hud_compornents,HudSquare nextComponent,byte id) {
		 this.GroupedID=id;
		 if(hud_compornents!=null) {//BIG_BOSS
			this.init();
			this.groupedhudcommander=true;
		 	int size=hud_compornents.size();
		 	this.pairHudSquare=hud_compornents.get(0);
		 	MCH_Lib.Log("[pairHudSquare]NOW_POS="+this.pairHudSquare.getPointCoords());
		 	for(int i=0;i<size-1;i++) {
		 		hud_compornents.get(i).hudGrouped(null,hud_compornents.get((i+1)%size),(byte)(i+1));
		 		MCH_Lib.Log("[hud_compornents]NOW_POS="+this.pairHudSquare.pairHudSquare.getPointCoords());
		 	}
		 	hud_compornents.get(size-1).hudGrouped(null,this,(byte)size);
		 	MCH_Lib.Log("[hud_compornents]NOW_POS2="+this.pairHudSquare.pairHudSquare.pairHudSquare.getPointCoords());

		 	this.setGrupedCenter();
		 }else {//child
			 this.pairHudSquare=nextComponent;
			 this.isGrouped=true;
		 }

	}

	 /**
	  * グループHUD用の関数で グループ用HUDを生成するときに使用する
	  * re[0]=minx
	  * re[1]=miny
	  * re[2]=maxx
	  * re[3]=maxy
	  */
	 protected float[] updateGroupedPos() {
		if(!this.groupedhudcommander) return null;
		boolean roop=true;

		//boolean roop=true;
		HudSquare nexthud=this.pairHudSquare;

		float[] now_m4xy=nexthud.getm4xy();
		float[] m4xy= {0,0,0,0};
		while(roop) {
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}
			m4xy=nexthud.getm4xy();
			//MCH_Lib.Log("X="+now_m4xy[0]);
			//MCH_Lib.Log("now_m4xy="+"MINX:"+now_m4xy[0]+"MINY="+now_m4xy[1]+"MAXX="+now_m4xy[2]+"MAXY="+now_m4xy[3]);
						//MCH_Lib.Log("NOW_POS="+nexthud.getPointCoords());
			now_m4xy[0]=now_m4xy[0]<=m4xy[0]?now_m4xy[0]:m4xy[0];
			now_m4xy[1]=now_m4xy[1]<=m4xy[1]?now_m4xy[1]:m4xy[1];
			now_m4xy[2]=now_m4xy[2]>=m4xy[2]?now_m4xy[2]:m4xy[2];
			now_m4xy[3]=now_m4xy[3]>=m4xy[3]?now_m4xy[3]:m4xy[3];
			//MCH_Lib.Log("m4xy="+"MINX:"+now_m4xy[0]+"MINY="+now_m4xy[1]+"MAXX="+now_m4xy[2]+"MAXY="+now_m4xy[3]);
		}
		//MCH_Lib.Log("now_m4xy="+"MINX:"+now_m4xy[0]+"MINY="+now_m4xy[1]+"MAXX="+now_m4xy[2]+"MAXY="+now_m4xy[3]);
		return now_m4xy;
	 }

	 /**
	  * グループHUD用の関数で グループ用HUDを生成するときに使用する
	  * re[0]=minx
	  * re[1]=miny
	  * re[2]=maxx
	  * re[3]=maxy
	  */
	 protected float[] getGrupedAroundpos() {
		if(!this.groupedhudcommander) return null;


		boolean roop=true;
		float[] now_m4xy=this.getm4xy();
		float[] m4xy= {0,0,0,0};
		HudSquare nexthud=this.pairHudSquare;
		while(roop) {
			m4xy=nexthud.getm4xy();
			//MCH_Lib.Log("NOW_POS="+nexthud.getPointCoords());
			now_m4xy[0]=now_m4xy[0]<=m4xy[0]?now_m4xy[0]:m4xy[0];
			now_m4xy[1]=now_m4xy[1]<=m4xy[1]?now_m4xy[1]:m4xy[1];
			now_m4xy[2]=now_m4xy[2]>=m4xy[2]?now_m4xy[2]:m4xy[2];
			now_m4xy[3]=now_m4xy[3]>=m4xy[3]?now_m4xy[3]:m4xy[3];
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}
		}

		return now_m4xy;
	 }

	 /**
	  * グループHUD用の関数で、Update毎にグループHUDの中心を計算する
	  * この様にすることで、回転させるときに容易に位置を計算できるようになる
	  */
	 protected void setGrupedCenter() {
		if(!this.groupedhudcommander) return;

		boolean roop=true;
		HudSquare nexthud=this.pairHudSquare;
		MCH_Lib.Log("[setGrupedCenter]NOW_POS="+nexthud.getPointCoords());
		float[] now_m4xy=nexthud.getm4xy();
		float[] m4xy= {0,0,0,0};
		while(roop) {
			nexthud=nexthud.pairHudSquare;
			if(this.GroupedID==nexthud.GroupedID) {
				roop=false;
				break;
			}
			m4xy=nexthud.getm4xy();
			now_m4xy[0]=now_m4xy[0]<=m4xy[0]?now_m4xy[0]:m4xy[0];
			now_m4xy[1]=now_m4xy[1]<=m4xy[1]?now_m4xy[1]:m4xy[1];
			now_m4xy[2]=now_m4xy[2]>=m4xy[2]?now_m4xy[2]:m4xy[2];
			now_m4xy[3]=now_m4xy[3]>=m4xy[3]?now_m4xy[3]:m4xy[3];
		}

		this.GrupedCenterPos.x=(now_m4xy[0]+now_m4xy[2])/2;
		this.GrupedCenterPos.y=(now_m4xy[1]+now_m4xy[3])/2;

	 }

	 /**
	  * グループHUD用に使う関数
	  * re[0]=minx
	  * re[1]=miny
	  * re[2]=maxx
	  * re[3]=maxy
	  * @return
	  * float型の配列
	  */
	 public float[] getm4xy() {
		float[] re= {0f,0f,0f,0f};
		//MCH_Lib.Log("[getm4xy]P1"+this.P1.getPos().RvText());
		//MCH_Lib.Log("[getm4xy]P2"+this.P2.getPos().RvText());
		//MCH_Lib.Log("[getm4xy]P3"+this.P3.getPos().RvText());
		//MCH_Lib.Log("[getm4xy]P4"+this.P4.getPos().RvText());
		//re[0]=this.P1.getPos().RvCompareXmin(this.P2.getPos().RvCompareXmin(this.P3.getPos().RvCompareXmin(this.P4.getPos().x)));
		//re[1]=this.P1.getPos().RvCompareYmin(this.P2.getPos().RvCompareYmin(this.P3.getPos().RvCompareYmin(this.P4.getPos().y)));
		//re[2]=this.P1.getPos().RvCompareXmax(this.P2.getPos().RvCompareXmax(this.P3.getPos().RvCompareXmax(this.P4.getPos().x)));
		//re[3]=this.P1.getPos().RvCompareYmax(this.P2.getPos().RvCompareYmax(this.P3.getPos().RvCompareYmax(this.P4.getPos().y)));


		vec2 worldedP4=this.P4.getWPos();
		vec2 worldedP2=this.P2.getWPos();


		re[0]=worldedP4.x;
		re[1]=worldedP4.y;
		re[2]=worldedP2.x;
		re[3]=worldedP2.y;

		//MCH_Lib.Log("re[0]:"+re[0]+" re[1]:"+re[1]+" re[2]:"+re[2]+" re[3]:"+re[3]);

		 return re;
	 }

	 public HudSquare(HudTexCoord p1,HudTexCoord p2,HudTexCoord p3,HudTexCoord p4,String name,double[][] cornerpos) {
		this.useCornerPos=true;
		this.cornerpos[0][0]=cornerpos[0][0];
		this.cornerpos[0][1]=cornerpos[0][1];
		this.cornerpos[0][2]=cornerpos[0][2];

		this.cornerpos[1][0]=cornerpos[1][0];
		this.cornerpos[1][1]=cornerpos[1][1];
		this.cornerpos[1][2]=cornerpos[1][2];

		this.cornerpos[2][0]=cornerpos[2][0];
		this.cornerpos[2][1]=cornerpos[2][1];
		this.cornerpos[2][2]=cornerpos[2][2];

		this.cornerpos[3][0]=cornerpos[3][0];
		this.cornerpos[3][1]=cornerpos[3][1];
		this.cornerpos[3][2]=cornerpos[3][2];

		 this.init();
		 //MCH_Lib.Log("intit ok!");
		 this.texName=Texname;


		 this.P1.setClone(p1);
		 this.P2.setClone(p2);
		 this.P3.setClone(p3);
		 this.P4.setClone(p4);

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

	 public HudSquare(HudTexCoord p1,HudTexCoord p2,HudTexCoord p3,HudTexCoord p4,float rot,vec2 center,double L,double W,double T,double H,String name) {
		 MCH_Lib.Log("ROT="+rot);

		 float Rot=(float) Math.toRadians(rot);
		 MCH_Lib.Log("rot ok!");
		 this.init();
		 MCH_Lib.Log("intit ok!");
		 this.left=L;
		 this.width=W;
		 this.top=T;
		 this.height=H;
		 MCH_Lib.Log("LWTH ok!");

		 this.P1.setClone(p1);
		 this.P2.setClone(p2);
		 this.P3.setClone(p3);
		 this.P4.setClone(p4);
		 MCH_Lib.Log("P1~4 ok!");


		 this.setSquares();
		 this.setSize();
		 this.setCenterPos();
		 MCH_Lib.Log("setSquares ok!");

		 this.Points2output[0].setClone(this.P1.getPos());
		 this.Points2output[1].setClone(this.P2.getPos());
		 this.Points2output[2].setClone(this.P3.getPos());
		 this.Points2output[3].setClone(this.P4.getPos());

		 MCH_Lib.Log("Points2output ok!");

		 this.rotateHud(Rot,false);
	 }

	 public void HudSquare4GrupedLeader(HudTexCoord p1,HudTexCoord p2,HudTexCoord p3,HudTexCoord p4,double L,double W,double T,double H) {
		 //MCH_Lib.Log("intit ok!");
		 this.left=L;
		 this.width=W;
		 this.top=T;
		 this.height=H;
		 //MCH_Lib.Log("LWTH ok!");

		 this.P1.setClone(p1);
		 this.P2.setClone(p2);
		 this.P3.setClone(p3);
		 this.P4.setClone(p4);
		 //MCH_Lib.Log("P1~4 ok!");


		 this.setSquares();
		 this.setSize();
		 this.setCenterPos();



		 //MCH_Lib.Log("setSquares ok!");

		 this.Points2output[0].setClone(this.P1.getPos());
		 this.Points2output[1].setClone(this.P2.getPos());
		 this.Points2output[2].setClone(this.P3.getPos());
		 this.Points2output[3].setClone(this.P4.getPos());

		 this.Stats.Position=new vec2(0.5f,0.5f);
		 this.WorldCenter=this.getCenterPos();
	 }

	 public HudSquare(HudTexCoord p1,HudTexCoord p2,HudTexCoord p3,HudTexCoord p4,double L,double W,double T,double H,String Texname,hudInitPrm... InitP) {
		 //MCH_Lib.Log("rot ok!");
		 this.init();
		 //MCH_Lib.Log("intit ok!");
		 this.texName=Texname;
		 this.left=L;
		 this.width=W;//POSX
		 this.top=T;
		 this.height=H;//POSY
		 //MCH_Lib.Log("LWTH ok!");

		 this.P1.setClone(p1);
		 this.P2.setClone(p2);
		 this.P3.setClone(p3);
		 this.P4.setClone(p4);
		 //MCH_Lib.Log("P1~4 ok!");


		 this.setSquares();
		 this.setSize();
		 this.setCenterPos();



		 //MCH_Lib.Log("setSquares ok!");

		 this.Points2output[0].setClone(this.P1.getPos());
		 this.Points2output[1].setClone(this.P2.getPos());
		 this.Points2output[2].setClone(this.P3.getPos());
		 this.Points2output[3].setClone(this.P4.getPos());

		 this.Stats.Position=new vec2(0.5f,0.5f);
		 this.WorldCenter=this.getCenterPos();

		 //MCH_Lib.Log("Points2output ok!");

		 if(InitP.length>0) {
			 float Rot=(float) Math.toRadians(InitP[0].rot);
			 //this.rotateHud(Rot,InitP[0].isCenter?InitP[0].centerPos:this.centerPos);
			 this.scaleHud(InitP[0].Scale.x, InitP[0].Scale.x);
			 this.transformHud(InitP[0].Transform.x, InitP[0].Transform.x);
		 }
	 }

	 protected void init() {
		 this.left=0;
		 this.width=0;
		 this.top=0;
		 this.height=0;
		 this.Points2output=new vec2().getArray(4);
		 this.P1=new HudTexCoord();
		 this.P2=new HudTexCoord();
		 this.P3=new HudTexCoord();
		 this.P4=new HudTexCoord();
		 this.centerPos=new vec2();
		 this.texSize=new vec2();
		 this.Calc=new CalcCirclePoint();
		 this.Stats=new HudStats();
		 this.WorldCenter=new vec2();
	 }

	 protected void setSize() {
		 this.texSize.x=this.P2.getTexCoord().x;
		 this.texSize.y=this.P2.getTexCoord().y;
	 }

	 protected void setSquares() {
		 vec2[] t1;
		// MCH_Lib.Log("vec2 ok!");

		 t1=this.setPoint2Square(P1.getPos(), P2.getPos(), P3.getPos(), P4.getPos());
		 //MCH_Lib.Log("setPoint2Square ok!");

		 this.P1.getPos().setClone(t1[0]);
		 this.P2.getPos().setClone(t1[1]);
		 this.P3.getPos().setClone(t1[2]);
		 this.P4.getPos().setClone(t1[3]);
		 vec2[] t2;

		 t2=this.setPoint2Square(P1.getTexCoord(), P2.getTexCoord(), P3.getTexCoord(), P4.getTexCoord());
		 this.P1.getTexCoord().setClone(t2[0]);
		 this.P2.getTexCoord().setClone(t2[1]);
		 this.P3.getTexCoord().setClone(t2[2]);
		 this.P4.getTexCoord().setClone(t2[3]);
	 }

	 protected vec2[] setPoint2Square(vec2 p1,vec2 p2,vec2 p3,vec2 p4) {

			float minX=p1.RvCompareXmin(p2.RvCompareXmin(p3.RvCompareXmin(p4.x)));
			//MCH_Lib.Log("MINX ok!");


			float  minY=p1.RvCompareYmin(p2.RvCompareYmin(p3.RvCompareYmin(p4.y)));
			//MCH_Lib.Log("MINY ok!");

			vec2 minVec=new vec2(minX,minY);

			vec2 re[]=new vec2().getArray(4);

			//MCH_Lib.Log("re ok!");

			re[3].setClone(minVec);

			//MCH_Lib.Log("setClone ok!");

			if(minVec.x==p1.x&&minVec.y<p1.y) {
				re[0].setClone(p1);
			}
			if(minVec.x==p2.x&&minVec.y<p2.y) {
				re[0].setClone(p2);
			}
			if(minVec.x==p3.x&&minVec.y<p3.y) {
				re[0].setClone(p3);
			}
			if(minVec.x==p4.x&&minVec.y<p4.y) {
				re[0].setClone(p4);
			}

			if(re[0].y==p1.y&&re[0].x<p1.x) {
				re[1].setClone(p1);
			}
			if(re[0].y==p2.y&&re[0].x<p2.x) {
				re[1].setClone(p2);
			}
			if(re[0].y==p3.y&&re[0].x<p3.x) {
				re[1].setClone(p3);
			}
			if(re[0].y==p4.y&&re[0].x<p4.x) {
				re[1].setClone(p4);
			}

			if(re[1].y>p1.y&&re[1].x==p1.x) {
				re[2].setClone(p1);
			}
			if(re[1].y>p2.y&&re[1].x==p2.x) {
				re[2].setClone(p2);
			}
			if(re[1].y>p3.y&&re[1].x==p3.x) {
				re[2].setClone(p3);
			}
			if(re[1].y>p4.y&&re[1].x==p4.x) {
				re[2].setClone(p4);
			}

			return re;
	}

	 protected void setCenterPos() {
		this.centerPos.x=(this.P1.getTexCoord().x+this.P2.getTexCoord().x)/2;
		this.centerPos.y=(this.P1.getTexCoord().y+this.P4.getTexCoord().y)/2;
	}

	protected vec2 getCenterPos() {
		return new vec2((this.P1.getPos().x+this.P2.getPos().x)/2,(this.P1.getPos().y+this.P4.getPos().y)/2);
	}

	protected vec2 getCenterWPos() {
		return new vec2((this.P1.getWPos().x+this.P2.getWPos().x)/2,(this.P1.getWPos().y+this.P4.getWPos().y)/2);
	}

	/**
	 * テクスチャの原点を中心にして回す
	 */
	public void rotateHudbyGroup(float rot,vec2... centerpos) {
		if(centerpos.length>0) {
			vec2 rcenter=this.Calc.Calc_cPoint(centerpos[0],this.WorldCenter,rot);
			this.Transform2Point(rcenter);
			this.rotateHud(rot,false);
		}
	}

	/**
	 * テクスチャの原点を中心にして回す
	 */
	public void rotateHud(float rot,boolean... rotateByGroup) {
		vec2 center=new vec2();
		center.setClone(this.centerPos);

		this.Points2output[0]=this.Calc.Calc_cPoint(center,this.P1.getPos(),rot);
		this.Points2output[1]=this.Calc.Calc_cPoint(center,this.P2.getPos(),rot);
		this.Points2output[2]=this.Calc.Calc_cPoint(center,this.P3.getPos(),rot);
		this.Points2output[3]=this.Calc.Calc_cPoint(center,this.P4.getPos(),rot);

		this.set2Point();
		if (rotateByGroup.length==0) {
			this.Stats.Rotate=rot;
		}
	}


	public void RotateByPosition(vec2 pos,float rot) {
		vec2 worldpos=this.Calc.Calc_cPoint2((pos),(this.Stats.Position),rot);
		this.Stats.Position.setClone(worldpos);
	}
	/**
	 * テクスチャを拡大する関数(ワールド)
	 * @param X_Scale
	 * @param Y_Scale
	 */
	public void scaleWorldHud(float X_Scale,float Y_Scale) {
		this.Stats.Scale.x=X_Scale;
		this.Stats.Scale.y=Y_Scale;
	}

	/**
	 * テクスチャを移動する関数(ワールド)
	 * @param X_Scale
	 * @param Y_Scale
	 */
	public void TransformHud(vec2 tgtPoint,float rotation,boolean rotpos,vec2 pos) {
		this.Stats.Position.x=tgtPoint.x;
		this.Stats.Position.y=tgtPoint.y;

		this.P2.setWorld(new vec2((this.Stats.Position.x+this.Stats.Scale.x/2),(this.Stats.Position.y+this.Stats.Scale.y/2)));
		this.P1.setWorld(new vec2((this.Stats.Position.x-this.Stats.Scale.x/2),(this.Stats.Position.y+this.Stats.Scale.y/2)));
		this.P3.setWorld(new vec2((this.Stats.Position.x+this.Stats.Scale.x/2),(this.Stats.Position.y-this.Stats.Scale.y/2)));
		this.P4.setWorld(new vec2((this.Stats.Position.x-this.Stats.Scale.x/2),(this.Stats.Position.y-this.Stats.Scale.y/2)));
		if(rotpos) {
			this.RotateByPosition(pos, rotation);
		}

		if(this.groupedhudcommander) {
			boolean roop=true;
			HudSquare nexthud=this.pairHudSquare;
			while(roop) {
				nexthud.TransformHud(nexthud.getCenter().getSumvec(this.WorldCenter.getdiff2vec(this.Stats.Position)),0,false,null);
				nexthud=nexthud.pairHudSquare;
				if(this.GroupedID==nexthud.GroupedID) {
					roop=false;
					break;
				}
			}
		}

		this.RotateHud(rotation);
		this.WorldCenter.x=this.Stats.Position.x;
		this.WorldCenter.y=this.Stats.Position.y;
	}


	public void Rotate(float rotation,boolean rotpos,vec2 pos) {
		if(rotpos) {
			this.RotateByPosition(pos, rotation);
		}
		this.RotateHud(rotation);
	}

	/**
	 * テクスチャを回転させる関数(ワールド)
	 * @param X_Scale
	 * @param Y_Scale
	 */
	public void RotateHud(float rotation) {
		this.Stats.Rotate+=rotation;
		this.Stats.Rotate%=360;
		if(this.groupedhudcommander) {
			boolean roop=true;
			HudSquare nexthud=this.pairHudSquare;
			while(roop) {
				nexthud.TransformHud(nexthud.getCenter(), rotation, true, this.getCenter());
				nexthud=nexthud.pairHudSquare;
				if(this.GroupedID==nexthud.GroupedID) {
					roop=false;
					break;
				}
			}
		}
	}


	/**
	 * テクスチャを拡大する関数
	 * @param X_Scale
	 * @param Y_Scale
	 */
	public void scaleHud(float X_Scale,float Y_Scale) {
		this.P1.getPos().setClone(this.P1.getTexCoord().getMulVec(new vec2(1/X_Scale,1/Y_Scale)));
		this.P2.getPos().setClone(this.P2.getTexCoord().getMulVec(new vec2(1/X_Scale,1/Y_Scale)));
		this.P3.getPos().setClone(this.P3.getTexCoord().getMulVec(new vec2(1/X_Scale,1/Y_Scale)));
		this.P4.getPos().setClone(this.P4.getTexCoord().getMulVec(new vec2(1/X_Scale,1/Y_Scale)));

		this.texSize.setClone(this.P2.getTexCoord().getMulVec(new vec2(1/X_Scale,1/Y_Scale)));

		this.Stats.Scale.x=X_Scale;
		this.Stats.Scale.y=Y_Scale;

		this.Stats.Position.x=X_Scale-(X_Scale/2);
		this.Stats.Position.y=Y_Scale-(Y_Scale/2);

		//MCH_Lib.Log("this.Stats.Position="+this.Stats.Position.RvText());

		this.set2Array();
	}

	/**
	 * -∞～∞ 正直使わないゴミ関数
	 * @param X
	 * @param Y
	 */
	public void transformHud(float X,float Y) {
		vec2 mul=new vec2(X,Y);
		MCH_Lib.Log("MUL="+this.texSize.getMulVec(mul).RvText());

		this.P1.getPos().setSumVec(this.texSize.getMulVec(mul));
		this.P2.getPos().setSumVec(this.texSize.getMulVec(mul));
		this.P3.getPos().setSumVec(this.texSize.getMulVec(mul));
		this.P4.getPos().setSumVec(this.texSize.getMulVec(mul));

		MCH_Lib.Log("P2="+this.P2.getPos().RvText());

		this.set2Array();
	}

	/**
	 *　HUDの指定した座標(X軸に対しての割合,Y軸に対しての割合)にテクスチャを置く
	 * めちゃくちゃ重要
	 * @param tgtPoint
	 */
	public void Transform2PointNew() {
		this.scaleHud(this.Stats.Scale.x, this.Stats.Scale.y);
		vec2 WorldedP2=this.getWorldPos(this.P2.getPos());

		float X=((this.WorldCenter.x-WorldedP2.x)/this.Stats.Scale.x);
		float Y=((this.WorldCenter.y-WorldedP2.y)/this.Stats.Scale.y);

		X*=-1;
		Y*=-1;

		vec2 truePos=new vec2(this.P2.getPos().x+(X*this.P2.getTexCoord().x),this.P2.getPos().y+(Y*this.P2.getTexCoord().y));
		vec2 diff=this.P2.getPos().getdiff2vec(truePos);

		this.P2.getPos().setClone(truePos);
		this.P1.getPos().setSumVec(diff);
		this.P3.getPos().setSumVec(diff);
		this.P4.getPos().setSumVec(diff);

		vec2 diff2center=new vec2(-1*this.P2.getTexCoord().x/2,-1*this.P2.getTexCoord().y/2);

		this.P1.getPos().setSumVec(diff2center);
		this.P2.getPos().setSumVec(diff2center);
		this.P3.getPos().setSumVec(diff2center);
		this.P4.getPos().setSumVec(diff2center);

		this.rotateHud(this.Stats.Rotate);
		this.setWorldPos();
		this.set2Array();
	}

	/**
	 *　HUDの指定した座標(X軸に対しての割合,Y軸に対しての割合)にテクスチャを置く
	 * めちゃくちゃ重要
	 * @param tgtPoint
	 */
	public void Transform2Point(vec2 tgtPoint) {
		this.scaleHud(this.Stats.Scale.x, this.Stats.Scale.y);
		vec2 WorldedP2=this.getWorldPos(this.P2.getPos());

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

		vec2 diff2center=new vec2(-1*this.P2.getTexCoord().x/2,-1*this.P2.getTexCoord().y/2);

		this.P1.getPos().setSumVec(diff2center);
		this.P2.getPos().setSumVec(diff2center);
		this.P3.getPos().setSumVec(diff2center);
		this.P4.getPos().setSumVec(diff2center);

		this.Stats.Position.x=tgtPoint.x;
		this.Stats.Position.y=tgtPoint.y;

		this.WorldCenter.x=tgtPoint.x;
		this.WorldCenter.y=tgtPoint.y;

		this.rotateHud(this.Stats.Rotate);
		this.setWorldPos();

		//**/

		//MCH_Lib.Log("\nthis.Stats.Position="+this.Stats.Position.RvText());

		//MCH_Lib.Log("[HUDTRANSFORM]"+this.getPointCoords()+"[TGT]"+tgtPoint.RvText());

		this.set2Array();
	}

	private void setWorldPos() {
		this.P2.setWorld(this.getWorldPos(this.P2.getPos()));
		this.P1.setWorld(this.getWorldPos(this.P1.getPos()));
		this.P3.setWorld(this.getWorldPos(this.P3.getPos()));
		this.P4.setWorld(this.getWorldPos(this.P4.getPos()));
	}

	public void PrintStats() {
		/*
		MCH_Lib.Log("P1:TEX="+this.P1.getTexCoord().RvText());
		MCH_Lib.Log("P1:POS="+this.P1.getPos().RvText());
		MCH_Lib.Log("P2:TEX="+this.P2.getTexCoord().RvText());
		MCH_Lib.Log("P2:POS="+this.P2.getPos().RvText());
		MCH_Lib.Log("P3:TEX="+this.P3.getTexCoord().RvText());
		MCH_Lib.Log("P3:POS="+this.P3.getPos().RvText());
		MCH_Lib.Log("P4:TEX="+this.P4.getTexCoord().RvText());
		MCH_Lib.Log("P4:POS="+this.P4.getPos().RvText());
		*/
		MCH_Lib.Log("P1:TEX="+this.P1.getTexCoord().RvText());
		MCH_Lib.Log("P1:POS="+this.P1.getPos().RvText());
		MCH_Lib.Log("P2:TEX="+this.P2.getTexCoord().RvText());
		MCH_Lib.Log("P2:POS="+this.P2.getPos().RvText());
		MCH_Lib.Log("P3:TEX="+this.P3.getTexCoord().RvText());
		MCH_Lib.Log("P3:POS="+this.P3.getPos().RvText());
		MCH_Lib.Log("P4:TEX="+this.P4.getTexCoord().RvText());
		MCH_Lib.Log("P4:POS="+this.P4.getPos().RvText());
	}

	public void Transform2Point4Group(vec2 localdiff1,vec2 localdiff2,vec2 worlddiff) {
		this.P1.getPos().setSumVec(localdiff1);
		this.P2.getPos().setSumVec(localdiff1);
		this.P3.getPos().setSumVec(localdiff1);
		this.P4.getPos().setSumVec(localdiff1);
		this.P1.getPos().setSumVec(localdiff2);
		this.P2.getPos().setSumVec(localdiff2);
		this.P3.getPos().setSumVec(localdiff2);
		this.P4.getPos().setSumVec(localdiff2);
		this.Stats.Position.setSumVec(worlddiff);
		this.WorldCenter.setSumVec(worlddiff);
		MCH_Lib.Log("---------------------------Transform2Point4Group-------------------------");
		MCH_Lib.Log("WorldPOS="+worlddiff.RvText());
		this.PrintStats();
		MCH_Lib.Log("-------------------------------------END---------------------------------");
	}

	/**
	 * ワールド座標をローカル座標に変換する関数
	 * @param tgtPoint #ワールド座標
	 * @return ローカル座標
	 */
	public vec2 getLocalPos(vec2 tgtPoint) {
		vec2 diff=new vec2();
		diff.setClone(this.Stats.Position.getdiff2vec(tgtPoint));
		diff.setDivvec(this.Stats.Scale);
		diff.setMulvec(this.texSize);
		diff.setClone(this.getCenterPos().getSumvec(diff.getMulVec(null,1)));
		return diff;
	}

	public vec2 getLocalPos2(vec2 tgtPoint) {
		vec2 diff=new vec2();
		MCH_Lib.Log("🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶🎶");
		MCH_Lib.Log("[MY_POS]"+this.Stats.Position.RvText());
		MCH_Lib.Log("[TGT_POS]"+tgtPoint.RvText());
		diff.setClone(this.Stats.Position.getdiff2vec(tgtPoint));
		MCH_Lib.Log("[DIFF]"+diff.RvText());
		diff.setDivvec(this.Stats.Scale);
		MCH_Lib.Log("[Scale]"+this.Stats.Scale.RvText());
		MCH_Lib.Log("[DIFF]"+diff.RvText());
		diff.setMulvec(this.texSize);
		MCH_Lib.Log("[texSize]"+this.texSize.RvText());
		MCH_Lib.Log("[DIFF]"+diff.RvText());
		MCH_Lib.Log("[getCenterPos]"+this.getCenterPos().RvText());
		diff.setClone(this.getCenterPos().getSumvec(diff.getMulVec(null,1)));
		MCH_Lib.Log("[DIFF]"+diff.RvText());
		MCH_Lib.Log("[WORLD]"+this.getWorldPos(diff).RvText());
		MCH_Lib.Log("🎶🎶🎶🎶🎶🎶🎶🎶getLocalPos2END🎶🎶🎶🎶🎶🎶🎶");

		return diff;
	}

	/**
	 * ローカル座標をワールド座標に変換する関数
	 * @param tgtPoint #ローカル座標
	 * @return ワールド座標
	 */
	public vec2 getWorldPos(vec2 tgtPoint) {
		vec2 diff=new vec2();
		diff.setClone(this.getCenterPos().getdiff2vec(tgtPoint));
		diff.setDivvec(this.texSize);
		diff.setMulvec(this.Stats.Scale);
		diff.setClone(this.Stats.Position.getSumvec(diff.getMulVec(null,1)));
		return diff;
	}


	protected void set2Array() {
		this.Points2output[0].setClone(this.P1.getPos());
		this.Points2output[1].setClone(this.P2.getPos());
		this.Points2output[2].setClone(this.P3.getPos());
		this.Points2output[3].setClone(this.P4.getPos());
	}

	protected void set2Point() {
		this.P1.getPos().setClone(this.Points2output[0]);
		this.P2.getPos().setClone(this.Points2output[1]);
		this.P3.getPos().setClone(this.Points2output[2]);
		this.P4.getPos().setClone(this.Points2output[3]);
	}


	public vec2 getP1() {
		return this.P1.getPos();
	}

	public vec2 getP2() {
		return this.P2.getPos();
	}

	public vec2 getP3() {
		return this.P3.getPos();
	}

	public vec2 getP4() {
		return this.P4.getPos();
	}

	public vec2 getP1Tex() {
		return this.P1.getTexPos();
	}

	public vec2 getP2Tex() {
		return this.P2.getTexPos();
	}

	public vec2 getP3Tex() {
		return this.P3.getTexPos();
	}

	public vec2 getP4Tex() {
		return this.P4.getTexPos();
	}


	public vec2[] rvVec2Aray() {
		return this.Points2output;
	}

	 public void setLeft(double LEFT) {
		 this.left=LEFT;
	 }

	 public void setWidth(double WIDTH) {
		 this.width=WIDTH;
	 }

	 public void setTop(double TOP) {
		 this.left=TOP;
	 }

	 public void setHeight(double HEIGHT) {
		 this.left=HEIGHT;
	 }

	 public double getLeft() {
		 return this.left;
	 }

	 public double getWidth() {
		 return this.width;
	 }

	 public double getTop() {
		 return this.top;
	 }

	 public double getHeight() {
		 return this.height;
	 }


	 public HudSquare[] getArray(int num) {
		 HudSquare[] re=new HudSquare[num];
		 for(int i=0;i<num;i++) {
			 re[i]=new HudSquare();
		 }
		 return re;
	 }


}
package mcheli.hud;

import mcheli.MCH_Lib;
import mcheli.reHud.HudSquare;
import mcheli.reHud.HudTexCoord;
import mcheli.reHud.hudInitPrm;
import mcheli.reHud.vec2;
import mcheli.wrapper.W_TextureUtil;
import net.minecraft.client.Minecraft;

public class DefineFixedhuds extends DefineHudEntitiy{

	public DefineFixedhudRoot parent=null;

	public vec2 pos=new vec2(0.5f,0.5f);// Image

	public vec2 texSize=new vec2(1,1);//Image

	public float rotation=0;//Image

	public String texname;


	boolean InitComp=false;

	public DefineFixedhuds(String n,DefineFixedhudRoot dfr,String x,String y,String sizex,String sizey,String TexName,String rot) {
		super(n);
		this.parent=dfr;
		this.pos.x=this.tofloat(x);
		this.pos.y=this.tofloat(y);
		this.texSize.x=this.tofloat(sizex);
		this.texSize.y=this.tofloat(sizey);
		this.rotation=this.tofloat(rot);
		this.texname=TexName;
	}

	public DefineFixedhuds(DefineFixedhuds clone) {
		super(clone.name);
		this.parent=clone.parent;
		this.pos.setClone(clone.pos);
		this.texSize.setClone(clone.texSize);
		this.rotation=clone.rotation;
		this.texname=clone.texname;
	}

	@Override
	public void final_init(Minecraft mc) {

		int[] texSize=this.texinit(mc);
		vec2[] initpos=this.initTexCoord(texSize);
		hudInitPrm parametor=new hudInitPrm();
		parametor.rot=this.rotation;
		parametor.Scale.setClone(this.texSize);
		parametor.Transform.setClone(pos);
		//MCH_Lib.Log("POSX="+parent.pos.xCoord+"SizeX="+parent.size.x+"PosY="+parent.pos.yCoord+"SizeY="+parent.size.y);
		//parent.pos.xCoord,parent.size.x,parent.pos.yCoord,parent.size.y
		if(this.parent.CornerMode) {
			this.ExecuteFunc=new HudSquare(new HudTexCoord(initpos[0],initpos[0]),new HudTexCoord(initpos[1],initpos[1]),new HudTexCoord(initpos[2],initpos[2]),new HudTexCoord(initpos[3],initpos[3]),this.texname,parent.hudCornerPos);
		}else {
			this.ExecuteFunc=new HudSquare(new HudTexCoord(initpos[0],initpos[0]),new HudTexCoord(initpos[1],initpos[1]),new HudTexCoord(initpos[2],initpos[2]),new HudTexCoord(initpos[3],initpos[3]),parent.pos.xCoord,parent.size.x,parent.pos.yCoord,parent.size.y,this.texname);
		}
		float [] test=this.ExecuteFunc.getm4xy();

		this.IsCompletalyInitedok=true;
	}

    private int[] texinit(Minecraft mc) {
    	int[] re=new int[2];
    	re[0] = 0;
    	re[1] = 0;
        W_TextureUtil.TextureParam prm = W_TextureUtil.getTextureInfo("mcheli",  "textures/gui/"+this.texname+".png");//textures/planes/zodiac.png

        if (prm != null) {
        	re[0] = prm.width;
        	re[1] = prm.height;
        }

        re[0] = re[0] > 0 ? re[0] : 256;
        re[1] = re[1] > 0 ? re[1] : 256;

        return re;
    }

    private vec2[] initTexCoord(int[] texSize) {
    	vec2[] re=(new vec2()).getArray(4);

		float fx = (float) (1.0D / (double) texSize[0]);
        float fy = (float) (1.0D / (double) texSize[1]);

        re[0].setClone(new vec2(0,(float)(this.texSize.y) * fy));
        MCH_Lib.Log("[initTexCoord]TEXSIZE="+this.texSize.RvText());
        re[1].setClone(new vec2((float)(this.texSize.x) * fx,(float)(this.texSize.y) * fy));
        re[2].setClone(new vec2((float)(this.texSize.x) * fx,0));
        re[3].setClone(new vec2(0,0));

		return re;
    }


	@Override
	public void execute(vec2 size,vec2 pos,float rot, boolean isrotvec,vec2 rotvec1,Minecraft mc) {//ItemHUDからの呼び出し
		this.ExecuteFunc.isExecute=false;

		this.ExecuteFunc.Update(size, pos, rot, isrotvec, rotvec1,mc);

		this.ExecuteFunc.isExecute=true;
	}

}

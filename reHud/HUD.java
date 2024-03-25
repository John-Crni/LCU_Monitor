package mcheli.reHud;

import org.lwjgl.opengl.GL11;
import org.lwjgl.opengl.GL13;

import mcheli.wrapper.W_TextureUtil;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.util.ResourceLocation;

public class HUD {

	private HudSquare HUD;

	public String texUrl;

	private vec2 hudPos;//realWorld

	private vec2 hudSize;//realWorld

	private vec2 texSize;//

	private boolean IsGrouped=false;

	private vec2 GroupedCenterPos;

	public int HudID=-1;


	public HUD(Minecraft mc,float World_X,float World_Y,float sizeX,float sizeY,float Px,float Py,String texurl,hudInitPrm... initprm) {
		this.init();
		this.texUrl=texurl;
		this.hudPos.x=World_X;
		this.hudPos.y=World_Y;
		this.hudSize.x=sizeX;
		this.hudSize.y=sizeY;
		this.texSize.x=Px;
		this.texSize.y=Py;
		int[] texSize=this.texinit(mc);
		vec2[] initpos=this.initTexCoord(texSize);
		if(initprm.length>0) {
		//	this.HUD=new HudSquare(new HudTexCoord(initpos[0],initpos[0]),new HudTexCoord(initpos[1],initpos[1]),new HudTexCoord(initpos[2],initpos[2]),new HudTexCoord(initpos[3],initpos[3]),World_X,sizeX,World_Y,sizeY,initprm[0]);
		}else {
		//	this.HUD=new HudSquare(new HudTexCoord(initpos[0],initpos[0]),new HudTexCoord(initpos[1],initpos[1]),new HudTexCoord(initpos[2],initpos[2]),new HudTexCoord(initpos[3],initpos[3]),World_X,sizeX,World_Y,sizeY);
		}
	}

	private void init() {
		this.texUrl="textures/gui/bou1.png";
		this.hudPos=new vec2();
		this.hudSize=new vec2();
		this.texSize=new vec2();
	}

    private int[] texinit(Minecraft mc) {
    	int[] re=new int[2];
    	re[0] = 0;
    	re[1] = 0;
        W_TextureUtil.TextureParam prm = W_TextureUtil.getTextureInfo("mcheli",  "textures/gui/bou1.png");//textures/planes/zodiac.png

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
        re[1].setClone(new vec2((float)(this.texSize.x) * fx,(float)(this.texSize.y) * fy));
        re[2].setClone(new vec2((float)(this.texSize.x) * fx,0));
        re[3].setClone(new vec2(0,0));

		return re;

    }

    public void AppTex(Minecraft mc) {
    	GL11.glPushMatrix();

    	mc.renderEngine.bindTexture(new ResourceLocation("mcheli",  this.texUrl));

    	GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_S, GL13.GL_CLAMP_TO_BORDER);
    	GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_T, GL13.GL_CLAMP_TO_BORDER);

    	// テクスチャの拡大時にピクセルを線形補間するように設定する
    	GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_LINEAR);

    	// テクスチャの縮小時にピクセルを線形補間するように設定する
    	GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_LINEAR);


    	GL11.glTranslated(this.HUD.getLeft() + this.HUD.getWidth() / 2.0D, this.HUD.getTop() + this.HUD.getHeight() / 2.0D, 0.0D);
    	GL11.glRotatef(0, 0.0F, 0.0F, 1.0F);
    	GL11.glEnable(GL11.GL_LIGHTING);
    	GL11.glEnable(GL11.GL_LIGHT0);

    	Tessellator tessellator = Tessellator.instance;// (double) this.zLevel

    	tessellator.startDrawingQuads();

    	tessellator.addVertexWithUV(-this.HUD.getWidth() / 2.0D, this.HUD.getHeight() / 2.0D, 0, (double)this.HUD.getP1().x ,(double)this.HUD.getP1().y);

    	tessellator.addVertexWithUV(this.HUD.getWidth() / 2.0D, this.HUD.getHeight() / 2.0D, 0,  (double)this.HUD.getP2().x ,(double)this.HUD.getP2().y);

    	tessellator.addVertexWithUV(this.HUD.getWidth() / 2.0D, -this.HUD.getHeight() / 2.0D,0,  (double)this.HUD.getP3().x ,(double)this.HUD.getP3().y);

    	tessellator.addVertexWithUV(-this.HUD.getWidth() / 2.0D, -this.HUD.getHeight() / 2.0D, 0,(double)this.HUD.getP4().x ,(double)this.HUD.getP4().y);

    	tessellator.draw();


    	GL11.glPopMatrix();
    }


}

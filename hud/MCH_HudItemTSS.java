package mcheli.hud;

import org.lwjgl.opengl.GL11;

import mcheli.wrapper.W_TextureUtil;

public class MCH_HudItemTSS extends MCH_HudItem{

    private final String name;
    private final String left;
    private final String top;
    private final String width;
    private final String height;
    private final String uLeft;
    private final String vTop;
    private final String uWidth;
    private final String vHeight;
    private final String rot;
    private final W_TextureUtil.TextureParam prm;
    private int textureWidth;
    private int textureHeight;

    public MCH_HudItemTSS(int fileLine, String name, String Xpos, String YPos, String Size,String width, String height, String uLeft, String vTop, String uWidth, String vHeight, String rot)
    {
        super(fileLine);
        this.name = name;
        double NormXpos=Math.abs(calc(Xpos));
        double NormYpos=Math.abs(calc(YPos));

        this.left = toFormula(String.valueOf((NormXpos*this.mc.displayHeight)));
        this.top = toFormula(name);
        this.width = toFormula(width);
        this.height = toFormula(height);
        this.uLeft = toFormula(uLeft);
        this.vTop = toFormula(vTop);
        this.uWidth = toFormula(uWidth);
        this.vHeight = toFormula(vHeight);
        this.rot = toFormula(rot);
        this.prm=null;
        this.textureWidth = this.textureHeight = 0;
    }

    private double RvNormXpos(double Xps) {
    	int ex=1;
    	double re=0;
    	if(Xps>1) {
    		return -1;
    	}
    	if(Xps<=0.5D) {
    		ex=-1;
    		re=ex*Xps;
    	}else {
    		re=Xps-0.5D*ex;
    	}
    	return re;
    }

    private double RvNormYpos(double Xps) {
    	int ex=1;
    	double re=0;
    	if(Xps>1) {
    		return -1;
    	}
    	if(Xps<=0.5D) {
    		ex=-1;
    		re=ex*Xps;
    	}else {
    		re=Xps-0.5D*ex;
    	}
    	return re;
    }

    public void execute()
    {
        GL11.glEnable(GL11.GL_BLEND);
        GL11.glColor4f(1.0F, 1.0F, 1.0F, 1.0F);

        if (this.textureWidth == 0 || this.textureHeight == 0)
        {
            int w = 0;
            int h = 0;
           // W_TextureUtil.TextureParam prm = W_TextureUtil.getTextureInfo("mcheli", "textures/gui/" + this.name + ".png");

            if (prm != null)
            {
                w = prm.width;
                h = prm.height;
            }

            this.textureWidth = w > 0 ? w : 256;
            this.textureHeight = h > 0 ? h : 256;
        }

        this.drawdrawTextureTss(this.name, centerX + calc(this.left), centerY + calc(this.top), calc(this.width), calc(this.height), calc(this.uLeft), calc(this.vTop), calc(this.uWidth), calc(this.vHeight), (float)calc(this.rot), this.textureWidth, this.textureHeight);
    }

}

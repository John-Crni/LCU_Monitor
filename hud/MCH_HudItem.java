package mcheli.hud;

import java.nio.FloatBuffer;
import java.nio.IntBuffer;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Random;

import org.lwjgl.BufferUtils;
import org.lwjgl.opengl.GL11;
import org.lwjgl.util.glu.GLU;

import mcheli.MCH_ClientCommonTickHandler;
import mcheli.MCH_Config;
import mcheli.MCH_Lib;
import mcheli.MCH_LowPassFilterFloat;
import mcheli.MCH_MOD;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.eval.eval.ExpRuleFactory;
import mcheli.eval.eval.Expression;
import mcheli.eval.eval.var.MapVariable;
import mcheli.gui.MCH_Gui;
import mcheli.helicopter.MCH_EntityHeli;
import mcheli.particles.MCH_HUDFIX;
import mcheli.plane.MCP_EntityPlane;
import mcheli.weapon.MCH_EntityTvMissile;
import mcheli.weapon.MCH_SightType;
import mcheli.weapon.MCH_WeaponBase;
import mcheli.weapon.MCH_WeaponInfo;
import mcheli.weapon.MCH_WeaponSet;
import mcheli.wrapper.W_McClient;
import mcheli.wrapper.W_OpenGlHelper;
import mcheli.wrapper.W_WorldFunc;
import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.renderer.ActiveRenderInfo;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.MathHelper;

public abstract class MCH_HudItem extends Gui {

    public final int fileLine;
    public static Vector3 VecZero=Vector3.zero;
    public static Minecraft mc;
    public static EntityPlayer player;
    public static MCH_EntityAircraft ac;
    protected static double centerX = 0.0D;
    protected static double centerY = 0.0D;
    public static double width;
    public static double height;
    protected static Random rand = new Random();
    public static int scaleFactor;
    public static int colorSetting = -16777216;
    protected static int altitudeUpdateCount = 0;
    protected static int Altitude = 0;
    protected static float prevRadarRot;
    protected static String WeaponName = "";
    protected static String WeaponAmmo = "";
    protected static String WeaponAllAmmo = "";
    protected static MCH_WeaponSet CurrentWeapon = null;
    protected static float ReloadPer = 0.0F;
    protected static float ReloadSec = 0.0F;
    protected static float MortarDist = 0.0F;
    protected static MCH_LowPassFilterFloat StickX_LPF = new MCH_LowPassFilterFloat(4);
    protected static MCH_LowPassFilterFloat StickY_LPF = new MCH_LowPassFilterFloat(4);
    protected static double StickX;
    protected static double StickY;
    protected static double TVM_PosX;
    protected static double TVM_PosY;
    protected static double TVM_PosZ;
    protected static double TVM_Diff;
    protected static double UAV_Dist;
    protected static int countFuelWarn;
    protected static ArrayList EntityList;
    protected static ArrayList EnemyList;
    protected static Map varMap = null;
    protected MCH_Hud parent;
    protected static float partialTicks;
    private static MCH_HudItemExit dummy = new MCH_HudItemExit(0);
    private static MCH_RenderHud TEST_RH=new MCH_RenderHud();

    private static MCH_HUDFIX Fixed_Hud=new MCH_HUDFIX();

    public MCH_HudItem(int fileLine) {
        this.fileLine = fileLine;
        this.zLevel = -110.0F;
    }

    public abstract void execute();

    public boolean canExecute() {
        return !this.parent.isIfFalse;
    }

    public static void update() {
        MCH_WeaponSet ws = MCH_HudItem.ac.getCurrentWeapon(MCH_HudItem.player);

        updateRadar(MCH_HudItem.ac);
        updateStick();
        updateAltitude(MCH_HudItem.ac);
        updateTvMissile(MCH_HudItem.ac);
        updateUAV(MCH_HudItem.ac);
        updateWeapon(MCH_HudItem.ac, ws);
        updateVarMap(MCH_HudItem.ac, ws);
    }

    public static String toFormula(String s) {
        return s.toLowerCase().replaceAll("#", "0x").replace("\t", " ").replace(" ", "");
    }

    public static double calc(String s) {
        Expression exp = ExpRuleFactory.getDefaultRule().parse(s);

        exp.setVariable(new MapVariable(MCH_HudItem.varMap));
        return exp.evalDouble();
    }

    public static long calcLong(String s) {
        Expression exp = ExpRuleFactory.getDefaultRule().parse(s);

        exp.setVariable(new MapVariable(MCH_HudItem.varMap));
        return exp.evalLong();
    }

    public void drawdrawTextureTss(String name, double left, double top, double width, double height, double uLeft, double vTop, double uWidth, double vHeight, float rot, int textureWidth, int textureHeight) {

    }

    public void drawCenteredString(String s, int x, int y, int color) {
        this.drawCenteredString(MCH_HudItem.mc.fontRenderer, s, x, y, color);
    }

    public void drawString(String s, int x, int y, int color) {
        this.drawString(MCH_HudItem.mc.fontRenderer, s, x, y, color);
    }

    public void drawTexture(String name, double left, double top, double width, double height, double uLeft, double vTop, double uWidth, double vHeight, float rot, int textureWidth, int textureHeight) {
        W_McClient.MOD_bindTexture("textures/gui/" + name + ".png");
        GL11.glPushMatrix();
        GL11.glTranslated(left + width / 2.0D, top + height / 2.0D, 0.0D);
        GL11.glRotatef(rot, 0.0F, 0.0F, 1.0F);
        float fx = (float) (1.0D / (double) textureWidth);
        float fy = (float) (1.0D / (double) textureHeight);
        Tessellator tessellator = Tessellator.instance;

        tessellator.startDrawingQuads();
        tessellator.addVertexWithUV(-width / 2.0D, height / 2.0D, (double) this.zLevel, uLeft * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, -height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, vTop * (double) fy);
        tessellator.addVertexWithUV(-width / 2.0D, -height / 2.0D, (double) this.zLevel, uLeft * (double) fx, vTop * (double) fy);
        tessellator.draw();
        GL11.glPopMatrix();
    }

    public double BomgSight_XCoord=0d;
    public double BomgSight_YCoord=0d;
    public double BombSight=0d;

    public void  drawbombsight(PreEAClass PreGLID,String name, double left, double top, double width, double height, double uLeft, double vTop, double uWidth, double vHeight, float rot, int textureWidth, int textureHeight)
    {
            BombSight = (float)PreGLID.getLandInDistance1(player,this.Altitude+250,ac,0);
            W_McClient.MOD_bindTexture("textures/gui/" + name + ".png");
            GL11.glPushMatrix();
            GL11.glTranslated(PreGLID.GetDispPos().x+width / 2.0D, PreGLID.GetDispPos().y + height / 2.0D, 0.0);
            GL11.glRotatef(0, 0, 0, 1.0F);
            float fx = (float) (1.0D / (double) textureWidth);
            float fy = (float) (1.0D / (double) textureHeight);
            Tessellator tessellator = Tessellator.instance;
            tessellator.startDrawingQuads();
            tessellator.addVertexWithUV(-width / 2.0D, height / 2.0D, (double) this.zLevel, uLeft * (double) fx, (vTop + vHeight) * (double) fy);
            tessellator.addVertexWithUV(width / 2.0D, height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, (vTop + vHeight) * (double) fy);
            tessellator.addVertexWithUV(width / 2.0D, -height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, vTop * (double) fy);
            tessellator.addVertexWithUV(-width / 2.0D, -height / 2.0D, (double) this.zLevel, uLeft * (double) fx, vTop * (double) fy);
            tessellator.draw();
            GL11.glPopMatrix();
    }

    public void drawBulletPoint(PreEAClass PreGLID,String name, double left, double top, double width, double height, double uLeft, double vTop, double uWidth, double vHeight, float rot, int textureWidth, int textureHeight) {
        BombSight = (float)PreGLID.getLandInDistance2(player,this.Altitude+250,ac);
        W_McClient.MOD_bindTexture("textures/gui/" + name + ".png");
        GL11.glPushMatrix();
        GL11.glTranslated(PreGLID.GetDispPos().x, PreGLID.GetDispPos().y , 0.0);//-width / 4.0D -height / 4.0D
        GL11.glRotatef(0, 0, 0, 1.0F);
        float fx = (float) (1.0D / (double) textureWidth);
        float fy = (float) (1.0D / (double) textureHeight);
        Tessellator tessellator = Tessellator.instance;
        tessellator.startDrawingQuads();
        tessellator.addVertexWithUV(-width / 2.0D, height / 2.0D, (double) this.zLevel, uLeft * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, -height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, vTop * (double) fy);
        tessellator.addVertexWithUV(-width / 2.0D, -height / 2.0D, (double) this.zLevel, uLeft * (double) fx, vTop * (double) fy);
        tessellator.draw();
        GL11.glPopMatrix();
    }

    public void PlaySound(String SE_Name) {
    	W_McClient.MOD_playSoundFX(SE_Name, 1.0F, 1.0F);
    }

    Vector3 test=Vector3.zero;
    Vector3 diff=Vector3.zero;
    float x_diff=0;
    float y_diff=0;
    boolean s=false;
    int cnt=0;
//throws NoSuchFieldException, SecurityException, IllegalArgumentException, IllegalAccessException
    public void drawFixedTexture(String name, double left, double top, double width, double height, double uLeft, double vTop, double uWidth, double vHeight, float rot, int textureWidth, int textureHeight) throws IllegalArgumentException, IllegalAccessException, NoSuchFieldException, SecurityException  {

    	test=(getFreeLook(ac, MCH_HudItem.player)==1)?(Rv_HudPos(this.ac)):new Vector3((float)left,(float)top,0);

    	if(getFreeLook(ac, MCH_HudItem.player)==1) {
    		if(!s) {
    			cnt+=1;
    			x_diff=10000;
    			y_diff=10000;
    			if(cnt>=5) {
    				cnt=0;
        			s=true;
            		x_diff=(float)left-test.x;
            		y_diff=(float)top-test.y;
    			}
    		}
    	}else {
    		cnt=0;
    		x_diff=0;
    		y_diff=0;
    		s=false;
    	}
    	GL11.glMatrixMode(GL11.GL_MODELVIEW);

    	GL11.glPushMatrix();
    	W_McClient.MOD_bindTexture("textures/gui/" + name + ".png");

        GL11.glTranslated(x_diff+test.x + (width / 2.0D),y_diff+test.y + (height / 2.0D), 0.0D);

        GL11.glRotatef(rot, 0.0F, 0.0F, 1.0F);
        GL11.glRotatef(0, 0, 0, 1.0F);

        float fx = (float) (1.0D / (double) textureWidth);
        float fy = (float) (1.0D / (double) textureHeight);
        Tessellator tessellator = Tessellator.instance;


        tessellator.startDrawingQuads();

		tessellator.addVertexWithUV(-width / 2.0D, height / 2.0D, (double) this.zLevel, uLeft * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, (vTop + vHeight) * (double) fy);
        tessellator.addVertexWithUV(width / 2.0D, -height / 2.0D, (double) this.zLevel, (uLeft + uWidth) * (double) fx, vTop * (double) fy);
        tessellator.addVertexWithUV(-width / 2.0D, -height / 2.0D, (double) this.zLevel, uLeft * (double) fx, vTop * (double) fy);
        tessellator.draw();


        GL11.glPopMatrix();


    }

    static int count=0;

    public Vector3 Rv_HudPos(MCH_EntityAircraft air) {
    	Vector3 re=Vector3.zero;
    	if(air!=null&&this.player!=null) {
    		///*
            double X,Y,Z,AC_Yaw,AC_Pitch,AB_Yaw,x,z,Dis=1000;
            int F=0;
            AB_Yaw=0;
            AC_Yaw= MathHelper.wrapAngleTo180_float(air.getRotYaw());
            AC_Pitch=MathHelper.wrapAngleTo180_float(air.getRotPitch());

            if(AC_Yaw<=0&&AC_Yaw>=-90){
                F=1;
            }
            if(AC_Yaw>0&&AC_Yaw<=90){
                F=2;
            }
            if(AC_Yaw>90&&AC_Yaw<=180){
                F=3;
            }
            if(AC_Yaw<-90&&AC_Yaw>=-180){
                F=4;
            }

            switch (F){
            	case 1:AB_Yaw=90+AC_Yaw;break;
            	case 2:AB_Yaw=90-AC_Yaw;break;
            	case 3:AB_Yaw=AC_Yaw-90;break;
            	case 4:AB_Yaw=-AC_Yaw-90;break;
            }

            z = (Dis * Math.sin(Math.toRadians(AB_Yaw)));
            x = (Dis * Math.cos(Math.toRadians(AB_Yaw)));
            Y= player.posY+(Dis * (Math.tan(Math.toRadians(-AC_Pitch))));
            //Y= player.posY;

            switch (F){
                case 2:x=-x;break;
                case 3:x=-x;z=-z;break;
                case 4:z=-z;break;
            }


            X=(float)(player.posX+x);
            Z=(float)(player.posZ+z);

            //*/
    		//this.count=0;
    		re=this.Fixed_Hud.spawnHud(this.player,X,Y,Z);
    	}
    	//this.count+=1;
    	return re;
    }

    private Vector3 Rv_Test(Vector3 vec) {
    	Vector3 re=Vector3.zero;
    	double px1=0,py=0,pz1=0,scale1=0;
    	FloatBuffer pos=BufferUtils.createFloatBuffer(3);
        if (this.player!=null)
        {
            px1 = (double)(vec.x);
            py = (double)(vec.y);
            pz1 = (double)(vec.z);
            scale1 = Math.sqrt(px1 * px1 + py * py + pz1 * pz1) / 10.0D;

            if (scale1 < 1.0D)
            {
                scale1 = 1.0D;
            }


            FloatBuffer matModel1 = BufferUtils.createFloatBuffer(16);
            FloatBuffer matProjection1 = BufferUtils.createFloatBuffer(16);
            IntBuffer matViewport1 = BufferUtils.createIntBuffer(16);

            GL11.glGetFloat(GL11.GL_MODELVIEW_MATRIX, matModel1);
            GL11.glGetFloat(GL11.GL_PROJECTION_MATRIX, matProjection1);
            GL11.glGetInteger(GL11.GL_VIEWPORT, matViewport1);
            GLU.gluProject((float)(px1/ scale1), (float)(py / scale1), (float)(pz1 / scale1), matModel1, matProjection1, matViewport1, pos);

            int scale = MCH_Gui.scaleFactor > 0 ?  MCH_Gui.scaleFactor : 2;


            //mc=Minecraft.getMinecraft();
            double DW = this.mc.displayWidth;
            double DH = this.mc.displayHeight;
            double DSW = this.mc.displayWidth / scale;
            double DSH = this.mc.displayHeight / scale;

            re.x=(pos.get(0) / (float)scale);
            re.y= pos.get(2);
            re.z= (pos.get(1) / (float)scale);

            ///*
            if (re.z < 1.0D)
            {
            	re.y = (float)(DSH - (double)re.y);
            }
            else if (re.x < (double)(DW / 2))
            {
            	re.x = 10000.0f;
            }
            else if (re.x >= (double)(DW / 2))
            {
            	re.x = -10000.0f;
            }
            //*/

        }


        return re;

    }


    public void Bind_Tex(String n,MCH_EntityAircraft a) {
    	if(a!=null) {
    		this.TEST_RH.bind_tex(n, a);
    	}
    }


    private float getFOVModifier(float partialTicks)
    {
    	EntityLivingBase entity = this.player;
        float f1 = 70.0F;

        if (entity instanceof EntityLivingBase && ((EntityLivingBase)entity).getHealth() <= 0.0F)
        {
            float f2 = (float)((EntityLivingBase)entity).deathTime + partialTicks;
            f1 /= (1.0F - 500.0F / (f2 + 500.0F)) * 2.0F + 1.0F;
        }

        Block block = ActiveRenderInfo.getBlockAtEntityViewpoint(this.mc.theWorld,entity,partialTicks);

        if (block.getMaterial() == Material.water)
            f1 = f1 * 60.0F / 70.0F;

        return f1;
    }


    public static void drawRect(double par0, double par1, double par2, double par3, int par4) {
        double j1;

        if (par0 < par2) {
            j1 = par0;
            par0 = par2;
            par2 = j1;
        }

        if (par1 < par3) {
            j1 = par1;
            par1 = par3;
            par3 = j1;
        }

        float f3 = (float) (par4 >> 24 & 255) / 255.0F;
        float f = (float) (par4 >> 16 & 255) / 255.0F;
        float f1 = (float) (par4 >> 8 & 255) / 255.0F;
        float f2 = (float) (par4 & 255) / 255.0F;
        Tessellator tessellator = Tessellator.instance;

        GL11.glEnable(3042);
        GL11.glDisable(3553);
        W_OpenGlHelper.glBlendFunc(770, 771, 1, 0);
        GL11.glColor4f(f, f1, f2, f3);
        tessellator.startDrawingQuads();
        tessellator.addVertex(par0, par3, 0.0D);
        tessellator.addVertex(par2, par3, 0.0D);
        tessellator.addVertex(par2, par1, 0.0D);
        tessellator.addVertex(par0, par1, 0.0D);
        tessellator.draw();
        GL11.glEnable(3553);
        GL11.glDisable(3042);
    }

    public void drawLine(double[] line, int color) {
        this.drawLine(line, color, 1);
    }

    public void drawLine(double[] line, int color, int mode) {
        GL11.glPushMatrix();
        GL11.glEnable(3042);
        GL11.glDisable(3553);
        GL11.glBlendFunc(770, 771);
        GL11.glColor4ub((byte) (color >> 16 & 255), (byte) (color >> 8 & 255), (byte) (color >> 0 & 255), (byte) (color >> 24 & 255));
        Tessellator tessellator = Tessellator.instance;

        tessellator.startDrawing(mode);

        for (int i = 0; i < line.length; i += 2) {
            tessellator.addVertex(line[i + 0], line[i + 1], (double) this.zLevel);
        }

        tessellator.draw();
        GL11.glEnable(3553);
        GL11.glDisable(3042);
        GL11.glColor4b((byte) -1, (byte) -1, (byte) -1, (byte) -1);
        GL11.glPopMatrix();
    }

    public void drawLineStipple(double[] line, int color, int factor, int pattern) {
        GL11.glEnable(2852);
        GL11.glLineStipple(factor * MCH_HudItem.scaleFactor, (short) pattern);
        this.drawLine(line, color);
        GL11.glDisable(2852);
    }

    public void drawPoints(ArrayList points, int color, int pointWidth) {
        int prevWidth = GL11.glGetInteger(2833);

        GL11.glPushMatrix();
        GL11.glEnable(3042);
        GL11.glDisable(3553);
        GL11.glBlendFunc(770, 771);
        GL11.glColor4ub((byte) (color >> 16 & 255), (byte) (color >> 8 & 255), (byte) (color >> 0 & 255), (byte) (color >> 24 & 255));
        GL11.glPointSize((float) pointWidth);
        Tessellator tessellator = Tessellator.instance;

        tessellator.startDrawing(0);

        for (int i = 0; i < points.size(); i += 2) {
            tessellator.addVertex(((Double) points.get(i)).doubleValue(), ((Double) points.get(i + 1)).doubleValue(), 0.0D);
        }

        tessellator.draw();
        GL11.glEnable(3553);
        GL11.glDisable(3042);
        GL11.glPopMatrix();
        GL11.glColor4b((byte) -1, (byte) -1, (byte) -1, (byte) -1);
        GL11.glPointSize((float) prevWidth);
    }

    public static void updateVarMap(MCH_EntityAircraft ac, MCH_WeaponSet ws) {
        if (MCH_HudItem.varMap == null) {
            MCH_HudItem.varMap = new LinkedHashMap();
        }

        updateVarMapItem("color", getColor());
        updateVarMapItem("center_x", MCH_HudItem.centerX);
        updateVarMapItem("center_y", MCH_HudItem.centerY);
        updateVarMapItem("width", MCH_HudItem.width);
        updateVarMapItem("height", MCH_HudItem.height);
        updateVarMapItem("time", (double) (MCH_HudItem.player.worldObj.getWorldTime() % 24000L));
        MCH_Config mch_config = MCH_MOD.config;

        updateVarMapItem("test_mode", MCH_Config.TestMode.prmBool ? 1.0D : 0.0D);
        updateVarMapItem("plyr_yaw", (double) MathHelper.wrapAngleTo180_float(MCH_HudItem.player.rotationYaw));
        updateVarMapItem("plyr_pitch", (double) MCH_HudItem.player.rotationPitch);
        updateVarMapItem("yaw", (double) MathHelper.wrapAngleTo180_float(ac.getRotYaw()));
        updateVarMapItem("pitch", (double) ac.getRotPitch());
        updateVarMapItem("roll", (double) MathHelper.wrapAngleTo180_float(ac.getRotRoll()));
        updateVarMapItem("altitude", (double) MCH_HudItem.Altitude);
        updateVarMapItem("sea_alt", getSeaAltitude(ac));
        updateVarMapItem("have_radar", ac.isEntityRadarMounted() ? 1.0D : 0.0D);
        updateVarMapItem("radar_rot", (double) getRadarRot(ac));
        updateVarMapItem("hp", (double) ac.getHP());
        updateVarMapItem("max_hp", (double) ac.getMaxHP());
        updateVarMapItem("hp_rto", ac.getMaxHP() > 0 ? (double) ac.getHP() / (double) ac.getMaxHP() : 0.0D);
        updateVarMapItem("throttle", ac.getCurrentThrottle());
        updateVarMapItem("pos_x", ac.posX);
        updateVarMapItem("pos_y", ac.posY);
        updateVarMapItem("pos_z", ac.posZ);
        updateVarMapItem("motion_x", ac.motionX);
        updateVarMapItem("motion_y", ac.motionY);
        updateVarMapItem("motion_z", ac.motionZ);
        updateVarMapItem("speed", Math.sqrt(ac.motionX * ac.motionX + ac.motionY * ac.motionY + ac.motionZ * ac.motionZ));
        updateVarMapItem("fuel", (double) ac.getFuelP());
        updateVarMapItem("low_fuel", (double) isLowFuel(ac));
        updateVarMapItem("stick_x", MCH_HudItem.StickX);
        updateVarMapItem("stick_y", MCH_HudItem.StickY);
        updateVarMap_Weapon(ws);
        updateVarMapItem("vtol_stat", (double) getVtolStat(ac));
        updateVarMapItem("free_look", (double) getFreeLook(ac, MCH_HudItem.player));
        updateVarMapItem("gunner_mode", ac.getIsGunnerMode(MCH_HudItem.player) ? 1.0D : 0.0D);
        updateVarMapItem("cam_mode", (double) ac.getCameraMode(MCH_HudItem.player));
        updateVarMapItem("cam_zoom", (double) ac.camera.getCameraZoom());
        updateVarMapItem("auto_pilot", (double) getAutoPilot(ac, MCH_HudItem.player));
        updateVarMapItem("have_flare", ac.haveFlare() ? 1.0D : 0.0D);
        updateVarMapItem("can_flare", ac.canUseFlare() ? 1.0D : 0.0D);
        updateVarMapItem("inventory", (double) ac.getSizeInventory());
        updateVarMapItem("hovering", ac instanceof MCH_EntityHeli && ac.isHoveringMode() ? 1.0D : 0.0D);
        updateVarMapItem("is_uav", ac.isUAV() ? 1.0D : 0.0D);
        updateVarMapItem("uav_fs", getUAV_Fs(ac));
    }

    public static void updateVarMapItem(String key, double value) {
        MCH_HudItem.varMap.put(key, Double.valueOf(value));
    }

    public static void drawVarMap() {
        MCH_Config mch_config = MCH_MOD.config;

        if (MCH_Config.TestMode.prmBool) {
            int i = 0;
            int x = (int) (-300.0D + MCH_HudItem.centerX);
            int y = (int) (-100.0D + MCH_HudItem.centerY);
            Iterator i$ = MCH_HudItem.varMap.keySet().iterator();

            while (i$.hasNext()) {
                String key = (String) i$.next();

                MCH_HudItem.dummy.drawString(key, x, y, -12544);
                Double d = (Double) MCH_HudItem.varMap.get(key);
                String fmt = key.equalsIgnoreCase("color") ? String.format(": 0x%08X", new Object[] { Integer.valueOf(d.intValue())}) : String.format(": %.2f", new Object[] { d});

                MCH_HudItem.dummy.drawString(fmt, x + 50, y, -12544);
                ++i;
                y += 8;
                if (i == MCH_HudItem.varMap.size() / 2) {
                    x = (int) (200.0D + MCH_HudItem.centerX);
                    y = (int) (-100.0D + MCH_HudItem.centerY);
                }
            }
        }

    }

    private static double getUAV_Fs(MCH_EntityAircraft ac) {
        double uav_fs = 0.0D;

        if (ac.isUAV() && ac.getUavStation() != null) {
            double dx = ac.posX - ac.getUavStation().posX;
            double dz = ac.posZ - ac.getUavStation().posZ;
            float dist = (float) Math.sqrt(dx * dx + dz * dz);
            float distMax = 120.0F;

            if (dist > 120.0F) {
                dist = 120.0F;
            }

            uav_fs = (double) (1.0F - dist / 120.0F);
        }

        return uav_fs;
    }

    private static void updateVarMap_Weapon(MCH_WeaponSet ws) {
        int reloading = 0;
        double wpn_heat = 0.0D;
        int is_heat_wpn = 0;
        byte sight_type = 0;
        double lock = 0.0D;
        float rel_time = 0.0F;
        int display_mortar_dist = 0;

        if (ws != null) {
            MCH_WeaponBase wb = ws.getCurrentWeapon();
            MCH_WeaponInfo wi = wb.getInfo();

            if (wi == null) {
                return;
            }

            is_heat_wpn = wi.maxHeatCount > 0 ? 1 : 0;
            reloading = ws.isInPreparation() ? 1 : 0;
            display_mortar_dist = wi.displayMortarDistance ? 1 : 0;
            if (wi.delay > wi.reloadTime) {
                rel_time = (float) ws.countWait / (float) (wi.delay > 0 ? wi.delay : 1);
                if (rel_time < 0.0F) {
                    rel_time = -rel_time;
                }

                if (rel_time > 1.0F) {
                    rel_time = 1.0F;
                }
            } else {
                rel_time = (float) ws.countReloadWait / (float) (wi.reloadTime > 0 ? wi.reloadTime : 1);
            }

            if (wi.maxHeatCount > 0) {
                double cntLockMax = (double) ws.currentHeat / (double) wi.maxHeatCount;

                wpn_heat = cntLockMax > 1.0D ? 1.0D : cntLockMax;
            }

            int cntLockMax1 = wb.getLockCountMax();
            MCH_SightType sight = wb.getSightType();

            if (sight == MCH_SightType.LOCK && cntLockMax1 > 0) {
                lock = (double) wb.getLockCount() / (double) cntLockMax1;
                sight_type = 2;
            }

            if (sight == MCH_SightType.ROCKET) {
                sight_type = 1;
            }
        }

        updateVarMapItem("reloading", (double) reloading);
        updateVarMapItem("reload_time", (double) rel_time);
        updateVarMapItem("wpn_heat", wpn_heat);
        updateVarMapItem("is_heat_wpn", (double) is_heat_wpn);
        updateVarMapItem("sight_type", (double) sight_type);
        updateVarMapItem("lock", lock);
        updateVarMapItem("dsp_mt_dist", (double) display_mortar_dist);
        updateVarMapItem("mt_dist", (double) MCH_HudItem.MortarDist);
    }

    public static int isLowFuel(MCH_EntityAircraft ac) {
        byte is_low_fuel = 0;

        if (MCH_HudItem.countFuelWarn <= 0) {
            MCH_HudItem.countFuelWarn = 280;
        }

        --MCH_HudItem.countFuelWarn;
        if (MCH_HudItem.countFuelWarn < 160 && ac.getMaxFuel() > 0 && ac.getFuelP() < 0.1F && !ac.isInfinityFuel(MCH_HudItem.player, false)) {
            is_low_fuel = 1;
        }

        return is_low_fuel;
    }

    public static double getSeaAltitude(MCH_EntityAircraft ac) {
        double a = ac.posY - ac.worldObj.getHorizon();

        return a >= 0.0D ? a : 0.0D;
    }

    public static float getRadarRot(MCH_EntityAircraft ac) {
        float rot = (float) ac.getRadarRotate();
        float prevRot = MCH_HudItem.prevRadarRot;

        if (rot < prevRot) {
            rot += 360.0F;
        }

        MCH_HudItem.prevRadarRot = (float) ac.getRadarRotate();
        return MCH_Lib.smooth(rot, prevRot, MCH_HudItem.partialTicks);
    }

    public static int getVtolStat(MCH_EntityAircraft ac) {
        return ac instanceof MCP_EntityPlane ? ((MCP_EntityPlane) ac).getVtolMode() : 0;
    }

    public static int getFreeLook(MCH_EntityAircraft ac, EntityPlayer player) {
        return ac.isPilot(player) && ac.canSwitchFreeLook() && ac.isFreeLookMode() ? 1 : 0;
    }

    public static int getAutoPilot(MCH_EntityAircraft ac, EntityPlayer player) {
        return ac instanceof MCP_EntityPlane && ac.isPilot(player) && ac.getIsGunnerMode(player) ? 1 : 0;
    }

    public static double getColor() {
        long l = (long) MCH_HudItem.colorSetting;

        l &= 4294967295L;
        return (double) l;
    }

    private static void updateStick() {
        MCH_HudItem.StickX_LPF.put((float) (MCH_ClientCommonTickHandler.getCurrentStickX() / MCH_ClientCommonTickHandler.getMaxStickLength()));
        MCH_HudItem.StickY_LPF.put((float) (-MCH_ClientCommonTickHandler.getCurrentStickY() / MCH_ClientCommonTickHandler.getMaxStickLength()));
        MCH_HudItem.StickX = (double) MCH_HudItem.StickX_LPF.getAvg();
        MCH_HudItem.StickY = (double) MCH_HudItem.StickY_LPF.getAvg();
    }

    private static void updateRadar(MCH_EntityAircraft ac) {
        MCH_HudItem.EntityList = ac.getRadarEntityList();
        MCH_HudItem.EnemyList = ac.getRadarEnemyList();
    }

    private static void updateAltitude(MCH_EntityAircraft ac) {
        if (MCH_HudItem.altitudeUpdateCount <= 0) {
            int heliY = (int) ac.posY;

            if (heliY > 256) {
                heliY = 256;
            }

            for (int i = 0; i < 256 && heliY - i > 0; ++i) {
                int id = W_WorldFunc.getBlockId(ac.worldObj, (int) ac.posX, heliY - i, (int) ac.posZ);

                if (id != 0) {
                    MCH_HudItem.Altitude = i;
                    if (ac.posY > 256.0D) {
                        MCH_HudItem.Altitude = (int) ((double) MCH_HudItem.Altitude + (ac.posY - 256.0D));
                    }
                    break;
                }
            }

            MCH_HudItem.altitudeUpdateCount = 30;
        } else {
            --MCH_HudItem.altitudeUpdateCount;
        }

    }

    public static void updateWeapon(MCH_EntityAircraft ac, MCH_WeaponSet ws) {
        if (ac.getWeaponNum() > 0) {
            if (ws != null) {
                MCH_HudItem.CurrentWeapon = ws;
                MCH_HudItem.WeaponName = ac.isPilotReloading() ? "-- Reloading --" : ws.getName();
                if (ws.getAmmoNumMax() > 0) {
                    MCH_HudItem.WeaponAmmo = ac.isPilotReloading() ? "----" : String.format("%4d", new Object[] { Integer.valueOf(ws.getAmmoNum())});
                    MCH_HudItem.WeaponAllAmmo = ac.isPilotReloading() ? "----" : String.format("%4d", new Object[] { Integer.valueOf(ws.getRestAllAmmoNum())});
                } else {
                    MCH_HudItem.WeaponAmmo = "";
                    MCH_HudItem.WeaponAllAmmo = "";
                }

                MCH_WeaponInfo wi = ws.getInfo();

                if (wi.displayMortarDistance) {
                    MCH_HudItem.MortarDist = (float) ac.getLandInDistance(MCH_HudItem.player);
                } else {
                    MCH_HudItem.MortarDist = -1.0F;
                }

                if (wi.delay > wi.reloadTime) {
                    MCH_HudItem.ReloadSec = ws.countWait >= 0 ? (float) ws.countWait : (float) (-ws.countWait);
                    MCH_HudItem.ReloadPer = (float) ws.countWait / (float) (wi.delay > 0 ? wi.delay : 1);
                    if (MCH_HudItem.ReloadPer < 0.0F) {
                        MCH_HudItem.ReloadPer = -MCH_HudItem.ReloadPer;
                    }

                    if (MCH_HudItem.ReloadPer > 1.0F) {
                        MCH_HudItem.ReloadPer = 1.0F;
                    }
                } else {
                    MCH_HudItem.ReloadSec = (float) ws.countReloadWait;
                    MCH_HudItem.ReloadPer = (float) ws.countReloadWait / (float) (wi.reloadTime > 0 ? wi.reloadTime : 1);
                }

                MCH_HudItem.ReloadSec /= 20.0F;
                MCH_HudItem.ReloadPer = (1.0F - MCH_HudItem.ReloadPer) * 100.0F;
            }
        }
    }

    public static void updateUAV(MCH_EntityAircraft ac) {
        if (ac.isUAV() && ac.getUavStation() != null) {
            double dx = ac.posX - ac.getUavStation().posX;
            double dz = ac.posZ - ac.getUavStation().posZ;

            MCH_HudItem.UAV_Dist = (double) ((float) Math.sqrt(dx * dx + dz * dz));
        } else {
            MCH_HudItem.UAV_Dist = 0.0D;
        }

    }

    private static void updateTvMissile(MCH_EntityAircraft ac) {
        MCH_EntityTvMissile tvmissile = ac.getTVMissile();

        if (tvmissile != null) {
            MCH_HudItem.TVM_PosX = tvmissile.posX;
            MCH_HudItem.TVM_PosY = tvmissile.posY;
            MCH_HudItem.TVM_PosZ = tvmissile.posZ;
            double dx = tvmissile.posX - ac.posX;
            double dy = tvmissile.posY - ac.posY;
            double dz = tvmissile.posZ - ac.posZ;

            MCH_HudItem.TVM_Diff = Math.sqrt(dx * dx + dy * dy + dz * dz);
        } else {
            MCH_HudItem.TVM_PosX = 0.0D;
            MCH_HudItem.TVM_PosY = 0.0D;
            MCH_HudItem.TVM_PosZ = 0.0D;
            MCH_HudItem.TVM_Diff = 0.0D;
        }

    }
}

package mcheli.reHud;

import java.nio.FloatBuffer;
import java.util.Random;

import javax.vecmath.Vector3f;

import org.lwjgl.opengl.GL11;
import org.lwjgl.opengl.GLContext;

import mcheli.MCH_Lib;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.WorldClient;
import net.minecraft.client.particle.EffectRenderer;
import net.minecraft.client.renderer.GLAllocation;
import net.minecraft.client.renderer.OpenGlHelper;
import net.minecraft.client.renderer.RenderGlobal;
import net.minecraft.client.renderer.RenderHelper;
import net.minecraft.client.renderer.WorldRenderer;
import net.minecraft.client.renderer.culling.ClippingHelperImpl;
import net.minecraft.client.renderer.culling.Frustrum;
import net.minecraft.client.renderer.culling.ICamera;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.client.renderer.texture.TextureMap;
import net.minecraft.client.shader.Framebuffer;
import net.minecraft.client.shader.ShaderGroup;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.util.MathHelper;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.Timer;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;
import net.minecraftforge.client.ForgeHooksClient;

public class MFD {

	private Timer TIMER;

	private Framebuffer buffer;

	private Framebuffer buffer2;


	public EnumFace face;

	private DummyViewer dummyViewer;

	public float top;
	public float bottom;
	public float left;
	public float right;

	public boolean SETAUP_ALL_OK=false;

	Minecraft mc;
    private float farPlaneDistance;
    private int rendererUpdateCount;
    private  DynamicTexture lightmapTexture;
    private  int[] lightmapColors;
    private  ResourceLocation locationLightMap;
    private float bossColorModifier;
    private float bossColorModifierPrev;
    private boolean cloudFog;
    public ShaderGroup theShaderGroup;
    private static  ResourceLocation[] shaderResourceLocations = new ResourceLocation[] {new ResourceLocation("shaders/post/notch.json"), new ResourceLocation("shaders/post/fxaa.json"), new ResourceLocation("shaders/post/art.json"), new ResourceLocation("shaders/post/bumpy.json"), new ResourceLocation("shaders/post/blobs2.json"), new ResourceLocation("shaders/post/pencil.json"), new ResourceLocation("shaders/post/color_convolve.json"), new ResourceLocation("shaders/post/deconverge.json"), new ResourceLocation("shaders/post/flip.json"), new ResourceLocation("shaders/post/invert.json"), new ResourceLocation("shaders/post/ntsc.json"), new ResourceLocation("shaders/post/outline.json"), new ResourceLocation("shaders/post/phosphor.json"), new ResourceLocation("shaders/post/scan_pincushion.json"), new ResourceLocation("shaders/post/sobel.json"), new ResourceLocation("shaders/post/bits.json"), new ResourceLocation("shaders/post/desaturate.json"), new ResourceLocation("shaders/post/green.json"), new ResourceLocation("shaders/post/blur.json"), new ResourceLocation("shaders/post/wobble.json"), new ResourceLocation("shaders/post/blobs.json"), new ResourceLocation("shaders/post/antialias.json")};
    public static  int shaderCount = shaderResourceLocations.length;
    private int shaderIndex;
    /** Previous frame time in milliseconds */
    private long prevFrameTime;
    /** End time of last render (ns) */
    private long renderEndNanoTime;
    /** Is set, updateCameraAndRender() calls updateLightmap(); set by updateTorchFlicker() */
    private boolean lightmapUpdateNeeded;
    private float torchFlickerX;
    private float torchFlickerDX;
    private float torchFlickerY;
    private float torchFlickerDY;
    private Random random;
    private int rainSoundCounter;
    private float[] rainXCoords;
    private float[] rainYCoords;
    private FloatBuffer fogColorBuffer;
    private float fogColorRed;
    private float fogColorGreen;
    private float fogColorBlue;
    private float fogColor2;
    private float fogColor1;
    public Vec3 facePos;

    private boolean skipRender;

    private boolean skipRender2 = false;

    private Vector3f lookVec = new Vector3f();
    public boolean calledFromRenderer;



	private double depth;

	private SubRenderGlobal renderGlobal;

	public static int anaglyphField;

	public  int blockX;
	public  int blockY;
	public  int blockZ;

	public MFD() {
		this.buffer2 = new Framebuffer(1024, 1024, false);
	}


	public MFD(Minecraft mc,World world,int x, int y, int z) {

		this.blockX=x;
		this.blockY=y;
		this.blockZ=z;
		//float f0 = type == MirrorType.Mono_Panel ? -0.4375F : 0.5F;
		MCH_Lib.Log("\n 1!");
		float f0 = -0.4375F;
		//this.face = par1;
		//this.facePos = par2;
    	this.mc = mc;
    	MCH_Lib.Log("\n 2!");
    	//this.buffer2 = new Framebuffer(1024, 1024, false);
    	this.dummyViewer = new DummyViewer(world, 0.0D, 0.0D, 0.0D, 90.0F, 0.0F);
    	MCH_Lib.Log("\n 3!");


		MCH_Lib.Log("\n 3!");

		//this.buffer.setFramebufferColor(0.0F, 0.0F, 0.0F, 0.0F);
		MCH_Lib.Log("\n 3!");
				MCH_Lib.Log("\n 3!");

       // this.shaderIndex = shaderCount;
        MCH_Lib.Log("\n 4!");
        this.prevFrameTime = Minecraft.getSystemTime();
        MCH_Lib.Log("\n 5!");
        this.random = new Random();
        MCH_Lib.Log("\n 5!");
        MCH_Lib.Log("\n 5!");
        MCH_Lib.Log("\n MFD SETTING COMPLEATE!");


	}

	public void SetupBuffers() {
		this.buffer = new Framebuffer(1024, 1024, true);
		this.buffer.setFramebufferColor(0.0F, 0.0F, 0.0F, 0.0F);
		this.renderGlobal = new SubRenderGlobal();
        this.fogColorBuffer = GLAllocation.createDirectFloatBuffer(16);
        this.lightmapTexture = new DynamicTexture(16, 16);
		this.shaderIndex = shaderCount;
		this.locationLightMap = mc.getTextureManager().getDynamicTextureLocation("lightMap", this.lightmapTexture);
        this.lightmapColors = this.lightmapTexture.getTextureData();
        this.theShaderGroup = null;
		this.SETAUP_ALL_OK=true;
	}

	public void onTick()//RenderMirror.update()
	{
		if(TIMER == null)
		{
			TIMER = (Timer)Rend.getField(Minecraft.class, Rend.getMinecraft(), "timer", "field_71428_T");
		}

			float f0 = TIMER.renderPartialTicks;

			this.update(f0);

			//MirrorObject obj = MIRROR_OBJECTS.get(i);
			//obj.update(renderer, f0);

	}

	private void update(float partialTicks)//MC.runGameLoop()
	{

		//Minecraft mc = Rend.getMinecraft();
		EntityLivingBase prevViewer = mc.renderViewEntity;

		//this.clear();
		//this.updateMirrorComponents(prevViewer);
		//this.updateViewFrustrum();

		//if(this.skipRender)
		//{
		//	this.clear();
		//	return;
	//	}

		mc.renderViewEntity = this.dummyViewer;

		//NGTUtilClient.checkGLError("Pre_Mirror");



		GL11.glPushMatrix();
        //GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);//バッファクリア
        this.buffer.bindFramebuffer(true);
       // GL11.glEnable(GL11.GL_TEXTURE_2D);

       // this.updateCameraAndRender(this.buffer, partialTicks);
        //renderer.RapTex(10, -50,  500,500,  0,0,300,300);
       // GL11.glFlush();//直ちに実行
        this.buffer.unbindFramebuffer();
        GL11.glPopMatrix();


        //NGTUtilClient.checkGLError("Post_Mirror");

        //GL11.glViewport(0, 0, mc.displayWidth, mc.displayHeight);

        mc.renderViewEntity = prevViewer;

	}

    public void updateCameraAndRender(Framebuffer buffer, float par2)
    {
         this.renderWorld(par2, 0L);
    }

    public void renderWorld(float par1, long par2)
    {

    	if(this.mc==null){
    		this.mc=Rend.getMinecraft();
    	}


        GL11.glEnable(GL11.GL_CULL_FACE);
        GL11.glEnable(GL11.GL_DEPTH_TEST);
        GL11.glEnable(GL11.GL_ALPHA_TEST);
        GL11.glAlphaFunc(GL11.GL_GREATER, 0.5F);



        EntityLivingBase viewer = this.dummyViewer;
        double d0 = viewer.lastTickPosX;
        double d1 = viewer.lastTickPosY;
        double d2 = viewer.lastTickPosZ;

        RenderGlobal renderglobal = this.mc.renderGlobal;

        int pass = this.mc.gameSettings.anaglyph ? 2 : 1;
        for(int j = 0; j < pass; ++j)//アナグリフのパス
        {
            if(this.mc.gameSettings.anaglyph)
            {
                anaglyphField = j;
                if(anaglyphField == 0)
                {
                    GL11.glColorMask(false, true, true, false);
                }
                else
                {
                    GL11.glColorMask(true, false, false, false);
                }
            }

            int size = 1024;
            GL11.glViewport(0, 0, size, size);
           // this.updateFogColor(mirror, par1);
            GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);

            //テスト
            //this.SquareFill2D(10,100,500,0);


            GL11.glEnable(GL11.GL_CULL_FACE);



            //this.RapTex(10, -50,  500,500,  0,0,300,300);


            this.setupCameraTransform(par1, j);


            //ActiveRenderInfo.updateRenderInfo(this.mc.thePlayer, this.mc.gameSettings.thirdPersonView == 2);

            ClippingHelperImpl.getInstance();//init

            if(this.mc.gameSettings.renderDistanceChunks >= 4)
            {
                //this.setupFog(mirror, -1, par1);
                renderglobal.renderSky(par1);
            }

            GL11.glEnable(GL11.GL_FOG);
            //this.setupFog(mirror, 1, par1);

            if(this.mc.gameSettings.ambientOcclusion != 0)
            {
                GL11.glShadeModel(GL11.GL_SMOOTH);
            }

            WorldRenderer[] array = SubRenderGlobal.getRenderers(renderglobal);
            if(array.length == 0)
            {
            	renderglobal.loadRenderers();
            }

            //視錐台カリング
            Frustrum frustrum = new Frustrum();
            frustrum.setPosition(d0, d1, d2);
            renderglobal.clipRenderersByFrustum(frustrum, par1);



            if(j == 0)
            {
            	//ブロックのGLリスト作成
                while(!renderglobal.updateRenderers(viewer, false))// && par2 != 0L)
                {
                    long k = par2 - System.nanoTime();
                    if(k < 0L || k > 1000000000L){break;}
                }
            }

            if(viewer.posY < 128.0D)
            {
                this.renderCloudsCheck(renderglobal, par1);
            }




            this.setupFog(0, par1);
            GL11.glEnable(GL11.GL_FOG);
            this.mc.getTextureManager().bindTexture(TextureMap.locationBlocksTexture);
            RenderHelper.disableStandardItemLighting();
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPushMatrix();


            //ブロック描画(pass:1)
            //renderglobal.sortAndRender(this.mc.thePlayer, 0, (double)par1);
            this.renderBlocks(frustrum, 0,this.dummyViewer);
            GL11.glShadeModel(GL11.GL_FLAT);
            GL11.glAlphaFunc(GL11.GL_GREATER, 0.1F);


            //Entity&TileEntity描画(pass:2)
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPopMatrix();
            GL11.glPushMatrix();
            RenderHelper.enableStandardItemLighting();
            ForgeHooksClient.setRenderPass(0);
            renderglobal.renderEntities(viewer, frustrum, par1);




            ForgeHooksClient.setRenderPass(0);
            //ToDo: Try and figure out how to make particles render sorted correctly.. {They render behind water}
            RenderHelper.disableStandardItemLighting();
            this.disableLightmap((double)par1);
            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPopMatrix();
            GL11.glPushMatrix();

            GL11.glMatrixMode(GL11.GL_MODELVIEW);
            GL11.glPopMatrix();

            /*GL11.glEnable(GL11.GL_BLEND);
            OpenGlHelper.glBlendFunc(770, 1, 1, 0);
            renderglobal.drawBlockDamageTexture(Tessellator.instance, viewer, par1);
            GL11.glDisable(GL11.GL_BLEND);*/

            EffectRenderer effectrenderer = this.mc.effectRenderer;
            this.enableLightmap((double)par1);
            effectrenderer.renderLitParticles(viewer, par1);
            RenderHelper.disableStandardItemLighting();
            //this.setupFog(mirror, 0, par1);
            effectrenderer.renderParticles(viewer, par1);
            this.disableLightmap((double)par1);

            GL11.glDepthMask(false);
            GL11.glEnable(GL11.GL_CULL_FACE);

           // this.renderRainSnow(mirror, par1);
            GL11.glDepthMask(true);
            GL11.glDisable(GL11.GL_BLEND);
            GL11.glEnable(GL11.GL_CULL_FACE);
            OpenGlHelper.glBlendFunc(770, 771, 1, 0);
            GL11.glAlphaFunc(GL11.GL_GREATER, 0.1F);
            //this.setupFog(mirror, 0, par1);
            GL11.glEnable(GL11.GL_BLEND);
            GL11.glDepthMask(false);
            this.mc.getTextureManager().bindTexture(TextureMap.locationBlocksTexture);

            //ブロック描画(pass:2)
            if(this.mc.gameSettings.fancyGraphics)
            {
                if(this.mc.gameSettings.ambientOcclusion != 0)
                {
                    GL11.glShadeModel(GL11.GL_SMOOTH);
                }

                GL11.glEnable(GL11.GL_BLEND);
                OpenGlHelper.glBlendFunc(770, 771, 1, 0);

                if(this.mc.gameSettings.anaglyph)
                {
                	switch(anaglyphField)
                	{
                	case 0: GL11.glColorMask(false, true, true, true);break;
                	case 1: GL11.glColorMask(true, false, false, true);break;
                	}
                }
            }

            this.renderBlocks(frustrum, 1,this.dummyViewer);
            //renderglobal.sortAndRender(this.mc.thePlayer, 1, (double)par1);

            if(this.mc.gameSettings.fancyGraphics)
            {
            	GL11.glDisable(GL11.GL_BLEND);
                GL11.glShadeModel(GL11.GL_FLAT);
            }

            //Entity&TileEntity描画(pass:2)
            RenderHelper.enableStandardItemLighting();
            ForgeHooksClient.setRenderPass(1);
            renderglobal.renderEntities(viewer, frustrum, par1);
            ForgeHooksClient.setRenderPass(-1);
            RenderHelper.disableStandardItemLighting();

            GL11.glDepthMask(true);
            GL11.glEnable(GL11.GL_CULL_FACE);
            GL11.glDisable(GL11.GL_BLEND);
            GL11.glDisable(GL11.GL_FOG);

            if(!this.mc.gameSettings.anaglyph){return;}
        }

        GL11.glColorMask(true, true, true, false);
    }



    public void enableLightmap(double p_78463_1_)
    {
        OpenGlHelper.setActiveTexture(OpenGlHelper.lightmapTexUnit);
        GL11.glMatrixMode(GL11.GL_TEXTURE);
        GL11.glLoadIdentity();
        float f = 0.00390625F;
        GL11.glScalef(f, f, f);
        GL11.glTranslatef(8.0F, 8.0F, 8.0F);
        GL11.glMatrixMode(GL11.GL_MODELVIEW);
        this.mc.getTextureManager().bindTexture(this.locationLightMap);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_LINEAR);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_LINEAR);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_LINEAR);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_LINEAR);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_S, GL11.GL_CLAMP);
        GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_T, GL11.GL_CLAMP);
        GL11.glColor4f(1.0F, 1.0F, 1.0F, 1.0F);
        GL11.glEnable(GL11.GL_TEXTURE_2D);
        OpenGlHelper.setActiveTexture(OpenGlHelper.defaultTexUnit);
    }


    /**Disable secondary texture unit used by lightmap*/
    public void disableLightmap(double p_78483_1_)
    {
        OpenGlHelper.setActiveTexture(OpenGlHelper.lightmapTexUnit);
        GL11.glDisable(GL11.GL_TEXTURE_2D);
        OpenGlHelper.setActiveTexture(OpenGlHelper.defaultTexUnit);
    }

	public void renderBlocks(ICamera cam, int par1,DummyViewer viewer1)
	{
		this.renderGlobal.renderBlocks(cam, par1,viewer1);
	}

    /**
     * Render clouds if enabled
     */
    private void renderCloudsCheck(RenderGlobal par1, float par2)
    {
        if(this.mc.gameSettings.shouldRenderClouds())
        {
            GL11.glPushMatrix();
            this.setupFog(0, par2);
            GL11.glEnable(GL11.GL_FOG);
            par1.renderClouds(par2);
            GL11.glDisable(GL11.GL_FOG);
            this.setupFog(1, par2);
            GL11.glPopMatrix();
        }
    }

    /**Update and return fogColorBuffer with the RGBA values passed as arguments*/
    private FloatBuffer setFogColorBuffer(float r, float g, float b, float a)
    {
        this.fogColorBuffer.clear();
        this.fogColorBuffer.put(r).put(g).put(b).put(a);
        this.fogColorBuffer.flip();
        return this.fogColorBuffer;
    }

    /**
     * Sets up the fog to be rendered. If the arg passed in is -1 the fog starts at 0 and goes to 80% of far plane
     * distance and is used for sky rendering.
     */
    private void setupFog(int par1, float par2)
    {
        EntityLivingBase entity = this.dummyViewer;
        boolean flag = false;



        if (par1 == 999)
        {
            GL11.glFog(GL11.GL_FOG_COLOR, this.setFogColorBuffer(0.0F, 0.0F, 0.0F, 1.0F));
            GL11.glFogi(GL11.GL_FOG_MODE, GL11.GL_LINEAR);
            GL11.glFogf(GL11.GL_FOG_START, 0.0F);
            GL11.glFogf(GL11.GL_FOG_END, 8.0F);

            if (GLContext.getCapabilities().GL_NV_fog_distance)
            {
                GL11.glFogi(34138, 34139);
            }

            GL11.glFogf(GL11.GL_FOG_START, 0.0F);
        }
        else
        {
            GL11.glFog(GL11.GL_FOG_COLOR, this.setFogColorBuffer(this.fogColorRed, this.fogColorGreen, this.fogColorBlue, 1.0F));
            GL11.glNormal3f(0.0F, -1.0F, 0.0F);
            GL11.glColor4f(1.0F, 1.0F, 1.0F, 1.0F);
            //Block block = ActiveRenderInfo.getBlockAtEntityViewpoint(this.mc.theWorld, entity, par2);

            if (this.cloudFog)
            {
                GL11.glFogi(GL11.GL_FOG_MODE, GL11.GL_EXP);
                GL11.glFogf(GL11.GL_FOG_DENSITY, 0.1F);
            }
            else
            {
                float f1 = this.farPlaneDistance;
                if(this.mc.theWorld.provider.getWorldHasVoidParticles() && !flag)
                {
                    double d0 = (double)((entity.getBrightnessForRender(par2) & 15728640) >> 20) / 16.0D + (entity.lastTickPosY + 4.0D) / 32.0D;

                    if (d0 < 1.0D)
                    {
                        if (d0 < 0.0D)
                        {
                            d0 = 0.0D;
                        }

                        d0 *= d0;
                        float f2 = 100.0F * (float)d0;

                        if (f2 < 5.0F)
                        {
                            f2 = 5.0F;
                        }

                        if (f1 > f2)
                        {
                            f1 = f2;
                        }
                    }
                }

                GL11.glFogi(GL11.GL_FOG_MODE, GL11.GL_LINEAR);

                if (par1 < 0)
                {
                    GL11.glFogf(GL11.GL_FOG_START, 0.0F);
                    GL11.glFogf(GL11.GL_FOG_END, f1);
                }
                else
                {
                    GL11.glFogf(GL11.GL_FOG_START, f1 * 0.75F);
                    GL11.glFogf(GL11.GL_FOG_END, f1);
                }

                if (GLContext.getCapabilities().GL_NV_fog_distance)
                {
                    GL11.glFogi(34138, 34139);
                }

                if (this.mc.theWorld.provider.doesXZShowFog((int)entity.posX, (int)entity.posZ))
                {
                    GL11.glFogf(GL11.GL_FOG_START, f1 * 0.05F);
                    GL11.glFogf(GL11.GL_FOG_END, Math.min(f1, 192.0F) * 0.5F);
                }
            }

            GL11.glEnable(GL11.GL_COLOR_MATERIAL);
            GL11.glColorMaterial(GL11.GL_FRONT, GL11.GL_AMBIENT);


        }
    }

    /**calculates fog and calls glClearColor*/
    private void updateFogColor( float par2)
    {
        WorldClient world = this.mc.theWorld;
        EntityLivingBase entity = this.dummyViewer;
        float f1 = 0.25F + 0.75F * (float)this.mc.gameSettings.renderDistanceChunks / 16.0F;
        f1 = 1.0F - (float)Math.pow((double)f1, 0.25D);
        Vec3 vec3 = world.getSkyColor(entity, par2);
        float f2 = (float)vec3.xCoord;
        float f3 = (float)vec3.yCoord;
        float f4 = (float)vec3.zCoord;
        Vec3 vec31 = world.getFogColor(par2);
        this.fogColorRed = (float)vec31.xCoord;
        this.fogColorGreen = (float)vec31.yCoord;
        this.fogColorBlue = (float)vec31.zCoord;
        float f5;

        if(this.mc.gameSettings.renderDistanceChunks >= 4)
        {
            Vec3 vec32 = MathHelper.sin(world.getCelestialAngleRadians(par2)) > 0.0F ? Vec3.createVectorHelper(-1.0D, 0.0D, 0.0D) : Vec3.createVectorHelper(1.0D, 0.0D, 0.0D);
            f5 = (float)entity.getLook(par2).dotProduct(vec32);

            if(f5 < 0.0F)
            {
                f5 = 0.0F;
            }
            else if(f5 > 0.0F)
            {
                float[] afloat = world.provider.calcSunriseSunsetColors(world.getCelestialAngle(par2), par2);

                if (afloat != null)
                {
                    f5 *= afloat[3];
                    this.fogColorRed = this.fogColorRed * (1.0F - f5) + afloat[0] * f5;
                    this.fogColorGreen = this.fogColorGreen * (1.0F - f5) + afloat[1] * f5;
                    this.fogColorBlue = this.fogColorBlue * (1.0F - f5) + afloat[2] * f5;
                }
            }
        }

        this.fogColorRed += (f2 - this.fogColorRed) * f1;
        this.fogColorGreen += (f3 - this.fogColorGreen) * f1;
        this.fogColorBlue += (f4 - this.fogColorBlue) * f1;
        float f8 = world.getRainStrength(par2);

        if (f8 > 0.0F)
        {
            f5 = 1.0F - f8 * 0.5F;
            float f9 = 1.0F - f8 * 0.4F;
            this.fogColorRed *= f5;
            this.fogColorGreen *= f5;
            this.fogColorBlue *= f9;
        }

        f5 = world.getWeightedThunderStrength(par2);

        if (f5 > 0.0F)
        {
        	float f9 = 1.0F - f5 * 0.5F;
            this.fogColorRed *= f9;
            this.fogColorGreen *= f9;
            this.fogColorBlue *= f9;
        }


        /*float f10 = this.fogColor2 + (this.fogColor1 - this.fogColor2) * par2;
        this.fogColorRed *= f10;
        this.fogColorGreen *= f10;
        this.fogColorBlue *= f10;*/
        double d0 = entity.lastTickPosY * world.provider.getVoidFogYFactor();

        if(d0 < 1.0D)
        {
            if(d0 < 0.0D)
            {
                d0 = 0.0D;
            }

            d0 *= d0;
            this.fogColorRed = (float)((double)this.fogColorRed * d0);
            this.fogColorGreen = (float)((double)this.fogColorGreen * d0);
            this.fogColorBlue = (float)((double)this.fogColorBlue * d0);
        }

        if(this.bossColorModifier > 0.0F)
        {
        	float f11 = this.bossColorModifierPrev + (this.bossColorModifier - this.bossColorModifierPrev) * par2;
            this.fogColorRed = this.fogColorRed * (1.0F - f11) + this.fogColorRed * 0.7F * f11;
            this.fogColorGreen = this.fogColorGreen * (1.0F - f11) + this.fogColorGreen * 0.6F * f11;
            this.fogColorBlue = this.fogColorBlue * (1.0F - f11) + this.fogColorBlue * 0.6F * f11;
        }

        if(this.mc.gameSettings.anaglyph)
        {
        	float f11 = (this.fogColorRed * 30.0F + this.fogColorGreen * 59.0F + this.fogColorBlue * 11.0F) / 100.0F;
            float f6 = (this.fogColorRed * 30.0F + this.fogColorGreen * 70.0F) / 100.0F;
            float f7 = (this.fogColorRed * 30.0F + this.fogColorBlue * 70.0F) / 100.0F;
            this.fogColorRed = f11;
            this.fogColorGreen = f6;
            this.fogColorBlue = f7;
        }

        //背景色設定, a:0.0でテクスチャの背景が透明になる
        GL11.glClearColor(this.fogColorRed, this.fogColorGreen, this.fogColorBlue, 1.0F);
    }


    private void orientCamera(float par1)
    {
        EntityLivingBase viewer = this.dummyViewer;
        double d0 = viewer.posX;
        double d1 = viewer.posY;
        double d2 = viewer.posZ;

        GL11.glRotatef(viewer.rotationYaw + 180.0F, 0.0F, 1.0F, 0.0F);
        GL11.glRotatef(viewer.rotationPitch, 1.0F, 0.0F, 0.0F);

        this.cloudFog = this.mc.renderGlobal.hasCloudFog(d0, d1, d2, par1);
    }

    /**sets up projection, view effects, camera position/rotation*/
    private void setupCameraTransform(float par1, int par2)
    {

        this.farPlaneDistance = (float)(this.mc.gameSettings.renderDistanceChunks << 4);//*16

        /*射影************************************************************************/

        GL11.glMatrixMode(GL11.GL_PROJECTION);
        GL11.glLoadIdentity();

        if(this.mc.gameSettings.anaglyph)
        {
            GL11.glTranslatef((float)(-(par2 * 2 - 1)) * 0.07F, 0.0F, 0.0F);
        }

        //Project.gluPerspective(mirror.fov, mirror.aspect, mirror.depth, this.farPlaneDistance * 2.0F);
        GL11.glFrustum(this.left, this.right, this.bottom, this.top, this.depth, (double)this.farPlaneDistance * 2.0D);

        /*************************************************************************************/

        GL11.glMatrixMode(GL11.GL_MODELVIEW);
        GL11.glLoadIdentity();

        if(this.mc.gameSettings.anaglyph)
        {
            GL11.glTranslatef((float)(par2 * 2 - 1) * 0.1F, 0.0F, 0.0F);
        }

        this.orientCamera(par1);

    }

	public EntityLivingBase getViewer()
	{
		return this.dummyViewer;
	}

	public boolean skipRender()
	{
		return this.skipRender;
	}

	public void bindTexture()
	{
		this.buffer.bindFramebufferTexture();
	}

	public void unbindTexture()
	{
		this.buffer.unbindFramebufferTexture();
	}




	private void updateMirrorComponents(EntityLivingBase viewer)
	{
		boolean b = true;
		this.updateFace(viewer);
		b &= this.skipRender();
		this.skipRender |= b;
	}

	private void clear()
	{
		//this.width = 0.0F;
		//this.height = 0.0F;
		this.top = 0.0F;
		this.bottom = 0.0F;
		this.left = 0.0F;
		this.right = 0.0F;
	}

	public void updateFace(EntityLivingBase viewer)
	{
		EnumFace face = this.face;

		//視線ベクトル
		float vx = (float)( viewer.posX);
		float vy = (float)( viewer.posY - (double)this.getEyeHeight(viewer));
		float vz = (float)(viewer.posZ);
		this.lookVec.set(vx, vy, vz);

		this.skipRender2 = !(this.canLook(face) && this.calledFromRenderer);
		this.calledFromRenderer = false;

		//if(obj.type == MirrorType.Hexa_Cube)
		//{
		//	Block block = viewer.worldObj.getBlock(this.blockX + (int)face.normal[0], this.blockY + (int)face.normal[1], this.blockZ + (int)face.normal[2]);
		//	this.skipRender |= (block.isNormalCube() || block == RTMBlock.mirrorCube);
		//}

		if(this.skipRender){return;}

		//反転した視線ベクトル(相対座標)
		float fx = vx * face.flip[0];
		float fy = vy * face.flip[1];
		float fz = vz * face.flip[2];

		float xn = fx - 0.5F;
		float xp = fx + 0.5F;
		float yn = fy - 0.5F;
		float yp = fy + 0.5F;
		float zn = fz - 0.5F;
		float zp = fz + 0.5F;

		switch(face)
		{
		//case BOTTOM:this.setupUV(obj, -zp, -zn, xn, xp, fy);break;
		case BOTTOM:break;
		case TOP:	this.setupUV(zn, zp, xn, xp, fy);break;
		case BACK:	this.setupUV(-yp, -yn, -xp, -xn, fz);break;
		case FRONT:	this.setupUV(-yp, -yn, xn, xp, fz);break;
		case LEFT:	this.setupUV(-yp, -yn, zn, zp, fx);break;
		case RIGHT:	this.setupUV(-yp, -yn, -zp, -zn, fx);break;
		default:break;
		}
	}



	/**鏡面がプレーヤーから見えてるかどうか*/
	private boolean canLook(EnumFace face)
	{
		float f0 = this.lookVec.x * face.normal[0] + this.lookVec.y * face.normal[1] + this.lookVec.z * face.normal[2];
		return f0 <= 0.0F;
	}

	private void setupUV(float hNeg, float hPos, float wNeg, float wPos, float d)
	{

		this.setSize(-hNeg, -hPos, -wPos, -wNeg);
	}

	public void setSize(float t, float b, float l, float r)
	{
		if(t > this.top)
		{
			this.top = t;
		}

		if(b < this.bottom)
		{
			this.bottom = b;
		}

		if(l < this.left)
		{
			this.left = l;
		}

		if(r > this.right)
		{
			this.right = r;
		}
	}

	public static float getEyeHeight(EntityLivingBase viewer)
	{
		//return viewer.getEyeHeight();
		return viewer.yOffset - 1.62F;
	}








}

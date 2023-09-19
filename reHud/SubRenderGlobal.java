package mcheli.reHud;

import java.util.LinkedList;
import java.util.List;

import org.lwjgl.opengl.GL11;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.RenderGlobal;
import net.minecraft.client.renderer.WorldRenderer;
import net.minecraft.client.renderer.culling.ICamera;
import net.minecraft.entity.EntityLivingBase;

/**RenderGlobalの代替*/
@SideOnly(Side.CLIENT)
public final class SubRenderGlobal
{
	private List<WorldRenderer> watchableRenderers = new LinkedList<WorldRenderer>();
	/*private int posX;
	private int posY;
	private int posZ;*/


	public void renderBlocks(ICamera cam, int pass,DummyViewer viewer1)
	{
		Minecraft mc = Rend.getMinecraft();
		mc.entityRenderer.enableLightmap(pass);

        WorldRenderer[] array = getRenderers(mc.renderGlobal);
        for(int i = 0; i < array.length; ++i)
        {
        	WorldRenderer renderer = array[i];
        	this.callWorldRenderer(renderer, pass,viewer1);
        }

        mc.entityRenderer.disableLightmap(pass);

        //mc.renderGlobal.renderAllRenderLists(0, 0.0D);
	}

	private void callWorldRenderer(WorldRenderer renderer, int pass,DummyViewer viewer1)
	{
		/*int x = (renderer.posX >> 4) - (this.posX >> 4);
		int y = (renderer.posY >> 4) - (this.posY >> 4);
		int z = (renderer.posZ >> 4) - (this.posZ >> 4);
		float[] normal = this.mirror.face.normal;
		int i0 = x * (int)normal[0] + y * (int)normal[1] + z * (int)normal[2];
		if(i0 < 0){return;}*/

		int gl = renderer.getGLCallListForPass(pass);//視野内にあるかここで確認済み
		if(gl < 0){return;}

		EntityLivingBase viewer = viewer1;
    	this.callLists(gl, (float)(renderer.posXMinus - viewer.posX), (float)(renderer.posYMinus - viewer.posY), (float)(renderer.posZMinus - viewer.posZ));
	}

	private void callLists(int gl, float x, float y, float z)
	{
		GL11.glPushMatrix();
        GL11.glTranslatef(x, y, z);
        GL11.glCallList(gl);
        GL11.glPopMatrix();
	}

	public static WorldRenderer[] getRenderers(RenderGlobal renderGlobal)
	{
		return (WorldRenderer[])Rend.getField(RenderGlobal.class, renderGlobal, "worldRenderers", "field_72765_l");
	}
}

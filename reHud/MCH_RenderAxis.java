package mcheli.reHud;

import org.lwjgl.opengl.GL11;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import mcheli.wrapper.W_Render;
import mcheli.wrapper.modelloader.W_ModelCustom;
import net.minecraft.entity.Entity;
import net.minecraftforge.client.model.IModelCustom;

@SideOnly(Side.CLIENT)
public class MCH_RenderAxis extends W_Render{

	@Override
	public void doRender(Entity entity, double posX, double posY, double posZ, float par8, float tickTime) {

        if (entity != null && entity instanceof MCH_EntityAxis) {
        	if(((MCH_EntityAxis)entity).getInfo()!=null) {
            	GL11.glPushMatrix();
                GL11.glTranslated(posX, posY, posZ);
                GL11.glRotatef(90, 0.0F, -1.0F, 0.0F);
                GL11.glRotatef(0, 1.0F, 0.0F, 0.0F);
                GL11.glRotatef(0, 0.0F, 0.0F, 1.0F);
                this.renderBody(((MCH_EntityAxis)entity).getInfo().model);
                GL11.glPopMatrix();
        	}
        }

   }


    public static void renderBody(IModelCustom model) {
        if (model != null) {
            if (model instanceof W_ModelCustom) {
                if (((W_ModelCustom) model).containsPart("$body")) {
                    model.renderPart("$body");
                } else {
                    model.renderAll();
                }
            } else {
                model.renderAll();
            }
        }

    }




}

package mcheli.reHud;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.client.renderer.EntityRenderer;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityLiving;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class MCH_RealRadar {

    private World worldObj;

    List<Vec3> Entitys = new ArrayList<Vec3>();

    Vec3 trash1=Vec3.createVectorHelper(0, 0, 0);

    double cosHalf =0;

    double innerProduct=0;

    EntityRenderer test;



    public MCH_RealRadar(World world) {
        this.worldObj = world;
    }

    public void clear() {
    	this.Entitys.clear();

    }


    public  List<Vec3> updateXZ(Entity centerEntity, int range,Vec3 PlayerEyePos,Vec3 PlayerForward,float fov,Vec3 HudPos,Vec3 HudForward) {
        if (this.worldObj.isRemote) {

            this.clear();
            List list = centerEntity.worldObj.getEntitiesWithinAABBExcludingEntity(centerEntity, centerEntity.boundingBox.expand((double) range, (double) range, (double) range));

            for (int i = 0; i < list.size(); ++i) {
                Entity entity = (Entity) list.get(i);

                if (entity instanceof EntityLiving) {
                    double x = entity.posX - PlayerEyePos.xCoord;
                    double z = entity.posZ - PlayerEyePos.zCoord;
                    double y = entity.posY - PlayerEyePos.yCoord;

                    double hx = entity.posX - HudPos.xCoord;
                    double hz = entity.posZ - HudPos.zCoord;
                    double hy = entity.posY - HudPos.yCoord;

                    boolean dot=getEntityinFrontPlayer(PlayerForward,x,y,z,HudForward,hx,hy,hz,fov);
                    if ((x * x + z * z +y*y< (double) (range * range))&&dot) {//this.getEntityinFrontPlayer(PlayerEyePos, PlayerForward, x, y, z)
                    	this.Entitys.add(Vec3.createVectorHelper(0, 0, 0));
                    	(this.Entitys.get(this.Entitys.size()-1)).xCoord=entity.posX;
                    	(this.Entitys.get(this.Entitys.size()-1)).yCoord=entity.posY;
                    	(this.Entitys.get(this.Entitys.size()-1)).zCoord=entity.posZ;

                    }
                }
            }//For
            return  this.Entitys;

        }//Remote
        return null;

    }

    private boolean getEntityinFrontPlayer(Vec3 PlayerForward,double x,double y,double z,Vec3 HudForward,double hx,double hy,double hz ,float fov) {
    	cosHalf=Math.cos((fov/2)*(3.14159265358979323846F/180));
    	trash1.xCoord=x;
    	trash1.yCoord=y;
    	trash1.zCoord=z;
    	x*=x;
    	y*=y;
    	z*=z;
    	double dis=x+y+z;
    	dis=Math.sqrt(dis);
    	trash1.xCoord/=dis;
    	trash1.yCoord/=dis;
    	trash1.zCoord/=dis;

    	innerProduct =trash1.dotProduct(PlayerForward);

    	if(innerProduct<=cosHalf) {
    		return false;
    	}

    	trash1.xCoord=hx;
    	trash1.yCoord=hy;
    	trash1.zCoord=hz;
    	hx*=hx;
    	hy*=hy;
    	hz*=hz;
    	dis=hx+hy+hz;
    	dis=Math.sqrt(dis);
    	trash1.xCoord/=dis;
    	trash1.yCoord/=dis;
    	trash1.zCoord/=dis;

    	innerProduct =trash1.dotProduct(HudForward);

    	return innerProduct>0;
    }

}

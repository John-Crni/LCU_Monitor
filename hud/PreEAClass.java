package mcheli.hud;

import mcheli.MCH_Lib;
import mcheli.aircraft.MCH_AircraftInfo;
import mcheli.aircraft.MCH_EntityAircraft;
import mcheli.particles.MCH_HUDPI;
import mcheli.weapon.MCH_WeaponBase;
import mcheli.weapon.MCH_WeaponInfo;
import mcheli.weapon.MCH_WeaponParam;
import mcheli.weapon.MCH_WeaponSet;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityClientPlayerMP;
import net.minecraft.entity.Entity;
import net.minecraft.util.MathHelper;
import net.minecraft.util.MovingObjectPosition;
import net.minecraft.util.MovingObjectPosition.MovingObjectType;
import net.minecraft.util.Vec3;

public class PreEAClass{

    private double lastCalcLandInDistanceCount1;

    private double lastLandInDistance1;

    private Vector3 DispPos=Vector3.zero;


    public PreEAClass(){
    }

    public Vector3 GetDispPos() {
    	return this.DispPos;
    }



    public double getLandInDistance1(Entity user,int Alt,MCH_EntityAircraft AC,int Type)
    {//this.lastCalcLandInDistanceCount1 != (double) AC.getCountOnUpdate() &&
        if (AC.getCountOnUpdate() % 4 == 0)
        {
            this.lastCalcLandInDistanceCount1 = (double)AC.getCountOnUpdate();
            MCH_WeaponParam prm = new MCH_WeaponParam();
            prm.setPosition(AC.posX, AC.posY, AC.posZ);
            prm.entity = AC;
            prm.user = user;
            prm.isInfinity = AC.isInfinityAmmo(prm.user);

            if (prm.user != null)
            {
                MCH_WeaponSet currentWs = AC.getCurrentWeapon(prm.user);

                if (currentWs != null)
                {
                    int sid = AC.getSeatIdByEntity(prm.user);

                    if (AC.getAcInfo().getWeaponSetById(sid) != null)
                    {
                        prm.isTurret = ((MCH_AircraftInfo.Weapon)AC.getAcInfo().getWeaponSetById(sid).weapons.get(0)).turret;
                    }

                    this.lastLandInDistance1 =Secondly_getLandInDistance1(prm,currentWs,Alt,0);
                }
            }
        }

        return this.lastLandInDistance1;
    }

    public double getLandInDistance2(Entity user,int Alt,MCH_EntityAircraft AC)
    {//this.lastCalcLandInDistanceCount1 != (double) AC.getCountOnUpdate() &&
        //if (AC.getCountOnUpdate() % 1 == 0)
        //{
            this.lastCalcLandInDistanceCount1 = (double)AC.getCountOnUpdate();
            MCH_WeaponParam prm = new MCH_WeaponParam();
            prm.setPosition(AC.posX, AC.posY, AC.posZ);
            prm.entity = AC;
            prm.user = user;
            prm.isInfinity = AC.isInfinityAmmo(prm.user);

            if (prm.user != null)
            {
                MCH_WeaponSet currentWs = AC.getCurrentWeapon(prm.user);

                if (currentWs != null)
                {
                    int sid = AC.getSeatIdByEntity(prm.user);

                    if (AC.getAcInfo().getWeaponSetById(sid) != null)
                    {
                        prm.isTurret = ((MCH_AircraftInfo.Weapon)AC.getAcInfo().getWeaponSetById(sid).weapons.get(0)).turret;
                    }

                    this.lastLandInDistance1 =Secondly_getLandInDistance1(prm,currentWs,Alt,1);
                }
            }
        //}

        return this.lastLandInDistance1;
    }




    public double Secondly_getLandInDistance1(MCH_WeaponParam prm,MCH_WeaponSet ws,int Alt,int Type)
    {
        double ret = -1.0D;
        MCH_WeaponBase crtWpn1 = ws.getCurrentWeapon();

        if (crtWpn1 != null && crtWpn1.getInfo() != null)
        {
            MCH_WeaponInfo info = crtWpn1.getInfo();
            prm.rotYaw = prm.entity != null ? prm.entity.rotationYaw : 0.0F;
            prm.rotPitch = prm.entity != null ? prm.entity.rotationPitch : 0.0F;
            prm.rotYaw += ws.rotationYaw + crtWpn1.fixRotationYaw;
            prm.rotPitch += ws.rotationPitch + crtWpn1.fixRotationPitch;
            prm.rotYaw = MathHelper.wrapAngleTo180_float(prm.rotYaw);
            prm.rotPitch = MathHelper.wrapAngleTo180_float(prm.rotPitch);
            return (Type==0?this.Last_getLandInDistance1(prm,crtWpn1,Alt):this.getLandInDistanceTest(prm,crtWpn1));
        }
        else
        {
            return ret;
        }
    }

    public double Last_getLandInDistance1(MCH_WeaponParam prm,MCH_WeaponBase wb,int Alt)
    {

        float acceleration_re=0.0F,pitch=0;
        double acc=0,X=0;
        double speed=0.0D;
        double fac=0.0D;
        int i1;
        boolean flag=false;
        MCH_EntityAircraft air=wb.aircraft;
        X= MCH_HudItem.StickX/5;
        if (wb.weaponInfo == null)
        {
            return 0;
        }
        else if (wb.weaponInfo.gravity >= 0.0F)
        {
            return 0;
        }
        else
        {

            if(air.getRotPitch()<=0) {
                speed =Math.sqrt(air.motionY * air.motionY + air.motionZ * air.motionZ + air.motionX * air.motionX);
            }else {
                double p=air.getRotPitch();
                double m = (air.motionY * air.motionY);
                if(p>50&&p<=70){
                    m=0;
                }
                if(p>60&&p<=80){
                    p=p-9;
                }
                speed = speed + ((Math.sqrt(air.motionZ * air.motionZ + air.motionX * air.motionX + m)));
                if(p<40||p>80) {
                    speed = (speed * Math.cos(Math.toRadians(air.getRotPitch())));
                }else{
                    speed = (speed * Math.sin(Math.toRadians(p)));
                }
            }

            acceleration_re=wb.acceleration+(float)speed;
            pitch=-prm.rotPitch;

            if(pitch<0){
                pitch=0.01F;
            }

            Vec3 v = MCH_Lib.RotVec3(X, 0.0D, 1.0D, -prm.rotYaw,pitch, -prm.rotRoll);

            double s = Math.sqrt(v.xCoord * v.xCoord + v.yCoord * v.yCoord + v.zCoord * v.zCoord);
            acc = acceleration_re < 4.0F ? (double) acceleration_re : 4.0D;
            double accFac = (double)acceleration_re / acc;
            double my = v.yCoord * (double)acceleration_re / s;

            if (my <= 0.0D)
            {
                return 0;
            }else
            {

                MCH_HUDPI pi=new MCH_HUDPI();
                double mx = v.xCoord * (double)acceleration_re / s;
                double mz = v.zCoord * (double)acceleration_re / s;
                double ls = my / (double)wb.weaponInfo.gravity;
                double gravity = (double)wb.weaponInfo.gravity * accFac;
                double spx;

                EntityClientPlayerMP player = Minecraft.getMinecraft().thePlayer;

                if (ls < -12.0D)
                {
                    spx = ls / -12.0D;
                    mx *= spx;
                    my *= spx;
                    mz *= spx;
                    gravity *= spx * spx * 0.95D;
                }

                spx = prm.posX;
                double spy = prm.posY+3.0D;
                double spz = prm.posZ;
                Vec3 vs = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);
                Vec3 ve = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);


                for (int i = 0; i < Alt; ++i)
                {

                    vs.xCoord = spx;
                    vs.yCoord = spy;
                    vs.zCoord = spz;
                    ve.xCoord = spx + mx;
                    ve.yCoord = spy + my;
                    ve.zCoord = spz + mz;
                    MovingObjectPosition mop = wb.worldObj.rayTraceBlocks(vs, ve);

                    if ((mop != null &&(mop.typeOfHit == MovingObjectPosition.MovingObjectType.BLOCK)))
                    {
                        //pi.spawnHud(player, (double)mop.blockX+0.5D, (double)mop.blockY+1.0D, (double)mop.blockZ+0.5D);
                        this.DispPos.SetVec(pi.spawnHud(player, (double)mop.blockX+0.5D, (double)mop.blockY+1.0D, (double)mop.blockZ+0.5D));
                        return ve.xCoord;
                    }

                    my += gravity;
                    spx += mx;
                    spy += my;
                    spz += mz;

                }

                return 0.0D;
            }
        }
    }

    public double Last_getLandInDistance2VehicleBullet(MCH_WeaponParam prm,MCH_WeaponBase wb,int Alt)


    {

        float acceleration_re=0.0F,pitch=0;
        double acc=0,X=0;
        double speed=0.0D;
        double fac=0.0D;
        int i1;
        boolean flag=false;
        MCH_EntityAircraft air=wb.aircraft;
        X= MCH_HudItem.StickX/5;
        if (wb.weaponInfo == null)
        {
            return 0;
        }
        else if (wb.weaponInfo.gravity >= 0.0F)
        {
            return 0;
        }
        else
        {
/*
            if(air.getRotPitch()<=0) {
                speed =Math.sqrt(air.motionY * air.motionY + air.motionZ * air.motionZ + air.motionX * air.motionX);
            }else {
                double p=air.getRotPitch();
                double m = (air.motionY * air.motionY);
                if(p>50&&p<=70){
                    m=0;
                }
                if(p>60&&p<=80){
                    p=p-9;
                }
                speed = speed + ((Math.sqrt(air.motionZ * air.motionZ + air.motionX * air.motionX + m)));
                if(p<40||p>80) {
                    speed = (speed * Math.cos(Math.toRadians(air.getRotPitch())));
                }else{
                    speed = (speed * Math.sin(Math.toRadians(p)));
                }
            }
            */

            acceleration_re=wb.acceleration+(float)speed;
            pitch=-prm.rotPitch;

            if(pitch<0){
                pitch=0.01F;
            }

            Vec3 v = MCH_Lib.RotVec3(0.0D, 0.0D, 1.0D, -prm.rotYaw,-prm.rotPitch, -prm.rotRoll);

            double s = Math.sqrt(v.xCoord * v.xCoord + v.yCoord * v.yCoord + v.zCoord * v.zCoord);
            acc = acceleration_re < 4.0F ? (double) acceleration_re : 4.0D;
            double accFac = (double)acceleration_re / acc;
            double my = v.yCoord * (double)acceleration_re / s;

            if (my <= 0.0D)
            {
                return 0;
            }else
            {

                MCH_HUDPI pi=new MCH_HUDPI();
                double mx = v.xCoord * (double)acceleration_re / s;
                double mz = v.zCoord * (double)acceleration_re / s;
                double ls = my / (double)wb.weaponInfo.gravity;
                double gravity = (double)wb.weaponInfo.gravity * accFac;
                double spx;

                EntityClientPlayerMP player = Minecraft.getMinecraft().thePlayer;


                if (ls < -12.0D)
                {
                    spx = ls / -12.0D;
                    mx *= spx;
                    my *= spx;
                    mz *= spx;
                    gravity *= spx * spx * 0.95D;
                }


                spx = prm.posX;
                double spy = prm.posY+1;
                double spz = prm.posZ;
                Vec3 vs = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);
                Vec3 ve = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);


                for (int i = 0; i < 1000; ++i)
                {//mop.typeOfHit == MovingObjectPosition.MovingObjectType.ENTITY

                    vs.xCoord = spx;
                    vs.yCoord = spy;
                    vs.zCoord = spz;
                    ve.xCoord = spx + mx;
                    ve.yCoord = spy + my;
                    ve.zCoord = spz + mz;
                    MovingObjectPosition mop = wb.worldObj.rayTraceBlocks(vs, ve);

                    if ((mop != null &&((mop.typeOfHit == MovingObjectPosition.MovingObjectType.BLOCK))))
                    {
                        this.DispPos.SetVec(pi.spawnHud(player, (double)mop.blockX+0.5D, (double)mop.blockY+1.0D, (double)mop.blockZ+0.5D));

                        return ve.xCoord;
                    }

                    my += gravity;
                    spx += mx;
                    spy += my;
                    spz += mz;

                }

                return 0.0D;
            }
        }
    }

    double x=0;
    double y=0;
    double z=0;

    public double getLandInDistanceTest(MCH_WeaponParam prm,MCH_WeaponBase wb) {
        if (wb == null) {
            return -1.0D;
        } else if (wb.weaponInfo.gravity >= 0.0F) {
            return -1.0D;
        } else {
            //Vec3 v = MCH_Lib.RotVec3(0,0,1, -prm.rotYaw, -prm.rotPitch, -prm.rotRoll);//-prm.rotRoll
        	Vec3 v = MCH_Lib.RotVec3(0,0,1, -prm.rotYaw, -prm.rotPitch, -prm.rotRoll);//-prm.rotRoll

            double s = Math.sqrt(v.xCoord * v.xCoord + v.yCoord * v.yCoord + v.zCoord * v.zCoord);
            double acc = wb.acceleration < 4.0F ? (double) wb.acceleration : 4.0D;
            double accFac = (double) 8 / acc;
            double my = v.yCoord * (double)8/s;

           // if (my <= 0.0D) {
           //     return -1.0D;
           // } else {
            	MCH_HUDPI pi=new MCH_HUDPI();

                double mx = v.xCoord * (double) 8 /s;
                double mz = v.zCoord * (double) 8 / s;
                double ls = my / (double) wb.weaponInfo.gravity;//-0.00238
                //double gravity = (double) wb.weaponInfo.gravity;// * accFac
                double gravity =  (double) wb.weaponInfo.gravity * accFac;
                double spx;

                spx = prm.posX;
                double spy = prm.posY;
                double spz = prm.posZ;
                Vec3 vs = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);
                Vec3 ve = Vec3.createVectorHelper(0.0D, 0.0D, 0.0D);
                EntityClientPlayerMP player = Minecraft.getMinecraft().thePlayer;

                for (int i = 0; i < 1000; ++i) {
                    vs.xCoord = spx;
                    vs.yCoord = spy;
                    vs.zCoord = spz;
                    ve.xCoord = spx + mx;
                    ve.yCoord = spy + my;
                    ve.zCoord = spz + mz;
                    MovingObjectPosition mop = wb.worldObj.rayTraceBlocks(vs, ve);
                    double dx;
                    double dz;


                    if (mop != null && (mop.typeOfHit == MovingObjectType.BLOCK||mop.typeOfHit == MovingObjectType.ENTITY)) {
                        dx = (double) mop.blockX - prm.posX;
                        dz = (double) mop.blockZ - prm.posZ;

                        this.DispPos.SetVec(pi.spawnHud(player, (double)mop.blockX+0.5D, (double)mop.blockY, (double)mop.blockZ));
                        //this.DispPos.SetVec(pi.spawnHud(player, spx,spy,spz));

                        return dx;
                    }

                    my += gravity;
                    spx += mx;
                    spy += my;
                    spz += mz;

                    if (spy < prm.posY) {
                        dx = spx - prm.posX;
                        dz = spz - prm.posZ;
                        if (mop != null){
                        	this.DispPos.SetVec(pi.spawnHud(player, (double)mop.blockX+0.5D, (double)mop.blockY, (double)mop.blockZ));
                        }
                       // this.DispPos.SetVec(pi.spawnHud(player, spx,spy,spz));
                        return  dx;
                    }
                }

                return -1.0D;
            //}
        }
    }

}
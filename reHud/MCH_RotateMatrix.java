package mcheli.reHud;

import net.minecraft.util.Vec3;

public class MCH_RotateMatrix {

	private static double Pcos=0;

	private static double Psin=0;

	private static double Ycos=0;

	private static double Ysin=0;

	private static  double Rcos=0;

	private static double Rsin=0;

	public static Vec3 getRotationMat(float pitch,float yaw,float roll,byte xyz) {
		Pcos=Math.cos(Math.toRadians(pitch));
		Psin=Math.sin(Math.toRadians(pitch));

		Ycos=Math.cos(Math.toRadians(yaw));
		Ysin=Math.sin(Math.toRadians(yaw));

		Rcos=Math.cos(Math.toRadians(roll));
		Rsin=Math.sin(Math.toRadians(roll));

		Vec3 re=Vec3.createVectorHelper(0, 0, 0);

		switch(xyz) {
			case 0:re.xCoord=Rcos*Ycos-Rsin*Psin*Ysin;re.yCoord=-Pcos*Rsin;re.zCoord=Rcos*Ysin+Ycos*Rsin*Psin;break;
			case 1:re.xCoord=Ycos*Rsin+Rcos*Psin*Ysin;re.yCoord=Rcos*Pcos;re.zCoord=Rsin*Ysin-Rcos*Ycos*Psin;break;
			case 2:re.xCoord=-Pcos*Ysin;re.yCoord=Psin;re.zCoord=Pcos*Ycos;break;
		}

		return re;
	}


}

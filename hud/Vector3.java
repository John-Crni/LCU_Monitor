package mcheli.hud;

public class Vector3 {
	public float x=0f;
	public float y=0;
	public float z=0;

	public static Vector3 zero=new Vector3(0,0,0);

	public Vector3() {}

	public Vector3(float x,float y,float z) {
		this.x=x;
		this.y=y;
		this.z=z;
	}

	public void SetVec(float x,float y,float z) {
		this.x=x;
		this.y=y;
		this.z=z;
	}

	public void SetVec(Vector3 vec) {
		this.x=vec.x;
		this.y=vec.y;
		this.z=vec.z;
	}

	public static Vector3 Zero() {
		Vector3 re=new Vector3(0,0,0);
		return re;
	}

	public Vector3 Up() {
		Vector3 re=new Vector3(0,1,0);
		return re;
	}

	public Vector3 Right() {
		Vector3 re=new Vector3(1,0,0);
		return re;
	}

	public Vector3 Forward() {
		Vector3 re=new Vector3(0,0,1);
		return re;
	}
}

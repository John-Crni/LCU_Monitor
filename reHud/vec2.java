package mcheli.reHud;

public class vec2 {

	public float x;

	public float y;


	public vec2 getdiff2vec(vec2 tgt) {
		return new vec2(tgt.x-this.x,tgt.y-this.y);
	}


	public vec2 getMulVec(vec2 mul,float...rate) {
		if(rate.length>0) {
			return new vec2(this.x*rate[0],this.y*rate[0]);
		}
		return new vec2(this.x*mul.x,this.y*mul.y);
	}

	/**
	 * divで割る関数
	 * @param div 割る数 Getter
	 * @return
	 */
	public vec2 getDivvec(vec2 div) {
		return new vec2(this.x/div.x,this.y/div.y);

	}

	/**
	 * divで割る関数
	 * @param div 割る数 Setter
	 */
	public void setDivvec(vec2 div) {
		this.x=this.x/div.x;
		this.y=this.y/div.y;
	}

	/**
	 * mulでかける関数
	 * @param mul Setter
	 */
	public void setMulvec(vec2 mul,float... rate) {
		if(rate.length>0) {
			this.x=this.x*rate[0];
			this.y=this.y*rate[0];
		}else {
			this.x=this.x*mul.x;
			this.y=this.y*mul.y;
		}
	}

	public vec2 getSumvec(vec2 sum,float... rate) {
		if(rate.length>0) {
			return new vec2(this.x+rate[0],this.y+rate[0]);
		}
		return new vec2(this.x+sum.x,this.y+sum.y);
	}


	public void mulVec(vec2 mul) {
		this.x=this.x*mul.x;
		this.y=this.y*mul.y;
	}

	public void setSumVec(vec2 sum) {
		this.x+=sum.x;
		this.y+=sum.y;
	}


	public vec2[] getArray(int num) {
		vec2[] re=new vec2[num];
		for(int i=0;i<num;i++) {
			re[i]=new vec2();
		}
		return re;
	}

	public vec2() {
		this.x=0;
		this.y=0;
	}

	public vec2(float X,float Y) {
		this.x=X;
		this.y=Y;
	}

	public void setClone(vec2 v) {
		this.x=v.x;
		this.y=v.y;
	}

	public float RvCompareXmin(float X) {
		return this.x<=X?this.x:X;
	}

	public float RvCompareYmin(float Y) {
		return this.y<=Y?this.y:Y;
	}

	public float RvCompareXmax(float X) {
		return this.x>=X?this.x:X;
	}

	public float RvCompareYmax(float Y) {
		return this.y>=Y?this.y:Y;
	}

	public float RvCompareXminVec(vec2 vec) {
		return this.x<=vec.x?this.x:vec.x;
	}

	public float RvCompareYminVec(vec2 vec) {
		return this.y<=vec.y?this.y:vec.y;
	}

	public float RvCompareXmax(vec2 vec) {
		return this.x>=vec.x?this.x:vec.x;
	}

	public float RvCompareYmax(vec2 vec) {
		return this.y>=vec.y?this.y:vec.y;
	}

	public boolean isEqualVec(vec2 tgt) {
		return (this.x==tgt.x&&this.y==tgt.y);
	}

	public String RvText() {
		return ("X="+this.x+" Y="+this.y);
	}

	public vec2 getClone() {
		return new vec2(this.x,this.y);
	}

}

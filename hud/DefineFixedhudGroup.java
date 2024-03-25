package mcheli.hud;

import java.util.ArrayList;
import java.util.List;

import mcheli.MCH_Lib;
import mcheli.reHud.HudSquare;
import mcheli.reHud.groupedHudSquare;
import mcheli.reHud.vec2;
import net.minecraft.client.Minecraft;

public class DefineFixedhudGroup extends DefineHudEntitiy{

	List<DefineFixedhuds> DFH_LIST;

	public DefineFixedhudGroup(String name,List<DefineFixedhuds> DFH_LIST) {
		super(name);
		this.DFH_LIST=new ArrayList();
		for(int i=0;i<DFH_LIST.size();i++) {
			this.DFH_LIST.add(DFH_LIST.get(i));
		}
	}

	@Override
	public void final_init(Minecraft mc) {
		for(int i=0;i<this.DFH_LIST.size();i++) {
			if(!this.DFH_LIST.get(i).IsCompletalyInited) {
				//.Log("final_init="+this.DFH_LIST.get(i).na);
				this.IsCompletalyInitedok=false;
				return;
			}
		}
		List<HudSquare> huds=new ArrayList();
		for(int i=0;i<DFH_LIST.size();i++) {
			huds.add(DFH_LIST.get(i).ExecuteFunc);
		}
		this.ExecuteFunc=new groupedHudSquare(huds);
		MCH_Lib.Log("FINALY!");
		this.IsCompletalyInitedok=true;
	}

	@Override
	public void execute(vec2 size,vec2 pos,float rot, boolean isrotvec,vec2 rotvec1,Minecraft mc) {//ItemHUDからの呼び出し
		this.ExecuteFunc.isExecute=false;

		this.ExecuteFunc.Update(size, pos, rot, isrotvec, rotvec1,mc);

		this.ExecuteFunc.isExecute=true;
	}

}

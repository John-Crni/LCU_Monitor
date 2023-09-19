package mcheli.hud;

import java.util.List;

public class DefineFixedhudGroup extends DefineHudEntitiy{

	public List<DefineFixedhuds> Group;

	public DefineFixedhudGroup(String name,List<DefineFixedhuds> DFH_LIST) {
		super(name);
		this.Group=DFH_LIST;
	}

}

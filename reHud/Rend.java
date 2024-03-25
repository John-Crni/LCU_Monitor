package mcheli.reHud;

import java.lang.reflect.Field;

import cpw.mods.fml.client.FMLClientHandler;
import cpw.mods.fml.relauncher.ReflectionHelper;
import net.minecraft.client.Minecraft;

public class Rend {

	public static Object getField(Class<?> clazz, Object instance, String... names)
	{
		Field field = ReflectionHelper.findField(clazz, names);
		try
		{
			return field.get(instance);
		}
		catch (IllegalAccessException e)
		{
			e.printStackTrace();
		}
		return null;
	}

	public static Minecraft getMinecraft()
	{
		return FMLClientHandler.instance().getClient();
	}


}

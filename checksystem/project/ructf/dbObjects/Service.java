package ructf.dbObjects;

import java.sql.*;
import java.util.*;

public class Service
{
	private int id;
	private String name;
	private String checker;
	private boolean delayFlagGet;
	private boolean isNotTask;
	private int vulnboxSuffix;

	public static Vector<Service> LoadServices(Statement st) throws Exception
	{
		Vector<Service> services = new Vector<Service>();
		ResultSet rs = st.executeQuery(loadQuery);
		while (rs.next())
			services.add(new Service(rs));
		return services;
	}

	private Service(int id, String name, String checker, boolean delayFlagGet, boolean isNotTask, int vulnboxSuffix)
	{
		this.id = id;
		this.name = name;
		this.checker = checker;
		this.delayFlagGet = delayFlagGet;
		this.isNotTask = isNotTask;
		this.vulnboxSuffix = vulnboxSuffix;
	}

	private Service(ResultSet rs) throws SQLException
	{
		this(rs.getInt(1), rs.getString(2), rs.getString(3), rs.getBoolean(4), rs.getBoolean(5), rs.getInt(6));
	}

	public String toString()
	{
		return String.format("Service(%d, '%s', '%s', delay='%b', isNotTask='%b', vulnboxSuffix='%d')", id, name, checker, delayFlagGet, isNotTask, vulnboxSuffix);
	}

	public int getId()
	{
		return id;
	}

	public String getName()
	{
		return name;
	}

	public String getChecker()
	{
		return checker;
	}
	
	public boolean getDelayFlagGet()
	{
		return delayFlagGet;
	}
	
	public boolean getIsNotTask()
	{
		return isNotTask;
	}
	
	public int getVulnboxSuffix()
	{
		return vulnboxSuffix;
	}

	private static String loadQuery = "SELECT id, name, checker, delay_flag_get, is_not_task, vulnbox_suffix FROM services";
}

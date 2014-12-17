using System;

namespace heart.utils
{
	internal static class CommonUtils
	{
		public static void Try(Action action)
		{
			try
			{
				action();
			}
			catch(Exception e) {}
		}

		public static T TryOrDefault<T>(Func<T> func)
		{
			try
			{
				return func();
			}
			catch
			{
				return default(T);
			}
		}
	}
}
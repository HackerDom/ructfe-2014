using System;
using System.Linq;

namespace heart.db
{
	public static class StatMethods
	{
		public static double Avg(Stat stat)
		{
			return stat == null || stat.Points == null || stat.Points.Length == 0 ? 0 : (double)stat.Points.Sum(point => point.Value) / stat.Points.Length;
		}

		public static double Median(Stat stat)
		{
			if(stat == null || stat.Points == null || stat.Points.Length == 0)
				return 0;
			var isOdd = (stat.Points.Length & 1);
			var items = stat.Points.OrderBy(point => point.Value).Skip((stat.Points.Length >> 1) - (1 - isOdd)).Take(isOdd == 1 ? 1 : 2).ToArray();
			return (double)items.Sum(item => item.Value) / items.Length;
		}

		public static double StdDev(Stat stat)
		{
			if(stat == null || stat.Points == null || stat.Points.Length == 0)
				return 0;
			var avg = Avg(stat);
			return Math.Sqrt(stat.Points.Sum(point => (point.Value - avg) * (point.Value - avg)) / stat.Points.Length);
		}

		public static double Max(Stat stat)
		{
			return stat.Points.Length == 0 ? 0 : stat.Points.Max(point => point.Value);
		}

		public static double Min(Stat stat)
		{
			return stat.Points.Length == 0 ? 0 : stat.Points.Min(point => point.Value);
		}

		public static double Last(Stat stat)
		{
			return stat == null || stat.Points == null || stat.Points.Length == 0 ? 0 : stat.Points.Last().Value;
		}

		public static Stat WithEvents(Stat stat)
		{
			return Filter(stat, point => point.Event != null);
		}

		public static Stat LargerThan(Stat stat, int value)
		{
			return Filter(stat, point => point.Value > value);
		}

		public static Stat SmallerThan(Stat stat, int value)
		{
			return Filter(stat, point => point.Value < value);
		}

		private static Stat Filter(Stat stat, Func<DatePoint, bool> predicate)
		{
			return stat == null ? null : new Stat{Points = stat.Points == null ? null : stat.Points.Where(predicate).ToArray()};
		}
	}
}
using System;
using System.IO;
using System.Threading;
using heart.db;
using heart.handlers;
using log4net;
using log4net.Config;

namespace heart
{
	internal static class Program
	{
		private static void Main(string[] args)
		{
			XmlConfigurator.Configure();
			try
			{
				DB = new DbProvider(args[0]);

				var staticHandler = new StaticHandler(GetPrefix(null), Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "static"));
				staticHandler.Start();

				var addPointHandler = new AddPointHandler(GetPrefix("add"));
				addPointHandler.Start();

				var getSeriesHandler = new GetPointsHandler(GetPrefix("series"));
				getSeriesHandler.Start();

				var registerHandler = new RegisterHandler(GetPrefix("signup"));
				registerHandler.Start();

				var loginHandler = new LoginHandler(GetPrefix("signin"));
				loginHandler.Start();

				var setExpressionHandler = new SetExpressionHandler(GetPrefix("setexpr"));
				setExpressionHandler.Start();

				var getLastEventsHandler = new GetAlertsHandler(GetPrefix("alerts"));
				getLastEventsHandler.Start();

				Thread.Sleep(Timeout.Infinite);
			}
			catch(Exception e)
			{
				log.Fatal(e);
			}
		}

		private static string GetPrefix(string suffix)
		{
			return string.Format("http://+:{0}/{1}", Port, suffix == null ? null : suffix + '/');
		}

		private const int Port = 80;
		private static readonly ILog log = LogManager.GetLogger(typeof(Program));
		public static DbProvider DB;
	}
}
using System;
using System.Net;
using heart.db;

namespace heart.handlers
{
	internal class GetPointsHandler : AuthBaseHandler
	{
		public GetPointsHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessAuthorizedRequest(HttpListenerContext context, string login)
		{
			var utcNow = DateTime.UtcNow;
			var stat = Program.DB.TakeSafe(login, utcNow.AddMinutes(-60), utcNow);
			WriteData(context, stat.ToJson());
		}

		protected override void ProcessUnauthorizedRequest(HttpListenerContext context)
		{
			WriteData(context, GenerateRandom().ToJson());
		}

		private static Stat GenerateRandom()
		{
			const int count = 100;
			var utcNow = DateTime.UtcNow;
			var list = new DatePoint[count];
			var evtIdx = Random.Next(count - 4 * count / 5, count - count / 5);
			var mul = Random.Next(2) == 0 ? 1 : -1;
			for(int i = 0; i < count; i++)
			{
				string evt = null;
				var add = 30 - (evtIdx - i) * (evtIdx - i) / 10;
				if(add < 0) add = 0;
				add *= mul;
				if(i == evtIdx)
				{
					var eventsArray = add > 0 ? UpEvents : DownEvents;
					evt = eventsArray[Random.Next(UpEvents.Length)];
				}
				list[i] = new DatePoint {Date = utcNow.AddMinutes(i - count), Value = Random.Next(60, 80) + add, Event = evt};
			}
			return new Stat {Points = list};
		}

		private static Random Random { get { return random ?? (random = new Random()); } }

		[ThreadStatic] private static Random random;

		private static readonly string[] UpEvents = {"Running", "Fitness", "Skiing", "Swimming"};
		private static readonly string[] DownEvents = {"Sleeping", "Nirvana", "zZzZ", "Dinner"};
	}
}
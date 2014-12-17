using System;
using System.Net;
using System.Runtime.Serialization;
using heart.utils;

namespace heart.handlers
{
	internal class GetAlertsHandler : AuthBaseHandler
	{
		public GetAlertsHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessAuthorizedRequest(HttpListenerContext context, string login)
		{
			var utcNow = DateTime.UtcNow;

			var user = Program.DB.FindUser(login);
			if(user == null)
				throw new HttpException(HttpStatusCode.InternalServerError, "Can't find user");

			if(string.IsNullOrEmpty(user.Expression))
			{
				WriteData(context, null);
				return;
			}

			var series = Program.DB.TakeSafe(login, utcNow.AddMinutes(-60), utcNow);
			var result = ExpressionHelper.CalcExpression(user.Expression, series);
			WriteData(context, result != null ? new Alert {Message = result, Date = DateTime.UtcNow}.ToJson() : null);//TODO: Date?
		}

		[DataContract]
		internal class Alert : Data<Alert>
		{
			[DataMember(Name = "msg", Order = 1, EmitDefaultValue = false)] public string Message;
			[DataMember(Name = "dt", Order = 2, EmitDefaultValue = false)] private long date;

			[IgnoreDataMember] public DateTime Date { get { return DateTimeUtils.ParseUnixTime(date); } set { date = value.ToUnixTime(); } }
		}
	}
}
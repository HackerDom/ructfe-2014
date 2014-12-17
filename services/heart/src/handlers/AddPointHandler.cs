using System;
using System.Net;
using heart.db;

namespace heart.handlers
{
	internal class AddPointHandler : AuthBaseHandler
	{
		public AddPointHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessAuthorizedRequest(HttpListenerContext context, string login)
		{
			context.Request.AssertMethod(WebRequestMethods.Http.Post);
			var form = context.Request.GetPostData();

			string value;
			int intValue;
			if(!form.TryGetValue("val", out value) || !int.TryParse(value, out intValue))
				throw new HttpException(HttpStatusCode.BadRequest, "Empty val");

			if(intValue < 0)
				throw new HttpException(HttpStatusCode.BadRequest, "Val must be >= 0");

			string evt;
			form.TryGetValue("evt", out evt);

			var point = new DatePoint {Date = DateTime.UtcNow, Value = intValue, Event = evt};
			Program.DB.Insert(login, point);
			WriteString(context, "OK");
		}
	}
}
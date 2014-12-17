using System;
using System.Net;
using heart.utils;

namespace heart.handlers
{
	internal class SetExpressionHandler : AuthBaseHandler
	{
		public SetExpressionHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessAuthorizedRequest(HttpListenerContext context, string login)
		{
			context.Request.AssertMethod(WebRequestMethods.Http.Post);
			var form = context.Request.GetPostData();

			string expression;
			form.TryGetValue("expr", out expression);

			if(!string.IsNullOrEmpty(expression))
			{
				if(expression.Length > 512)
					throw new HttpException(HttpStatusCode.BadRequest, "Expression too large");

				var utcNow = DateTime.UtcNow;
				ExpressionHelper.CalcExpression(expression, Program.DB.TakeSafe(login, utcNow.AddMinutes(-60), utcNow));
			}

			string readable;
			form.TryGetValue("parts", out readable);

			if(readable != null && readable.Length > 512)
				throw new HttpException(HttpStatusCode.BadRequest, "Expression too large");

			Program.DB.SetExpression(login, expression, readable);
			context.Response.SetCookie("expr", readable);

			WriteString(context, "OK");
		}
	}
}
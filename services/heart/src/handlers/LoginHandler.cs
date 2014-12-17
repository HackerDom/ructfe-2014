using System;
using System.Net;
using heart.db;
using heart.utils;

namespace heart.handlers
{
	internal class LoginHandler : BaseHandler
	{
		public LoginHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessRequest(HttpListenerContext context)
		{
			context.Request.AssertMethod(WebRequestMethods.Http.Post);
			var form = context.Request.GetPostData();

			User user;
			string login, pass;
			if(!form.TryGetValue("login", out login) || !form.TryGetValue("pass", out pass) || string.IsNullOrEmpty(login) || string.IsNullOrEmpty(pass) || (user = Program.DB.FindUser(login)) == null || PassHash.GetHash(pass) != user.PassHash)
				throw new HttpException(HttpStatusCode.Forbidden, "Invalid credentials");

			context.Response.SetCookie("login", login);
			context.Response.SetCookie("token", TokenCrypt.Encrypt(new Token {Login = login, DateTime = DateTime.UtcNow}.ToJsonString()), true);
			context.Response.SetCookie("expr", user.Readable);

			WriteString(context, "OK");
		}
	}
}
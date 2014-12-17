using System;
using System.Net;
using System.Text.RegularExpressions;
using heart.db;
using heart.utils;

namespace heart.handlers
{
	internal class RegisterHandler : BaseHandler
	{
		public RegisterHandler(string prefix)
			: base(prefix)
		{
		}

		protected override void ProcessRequest(HttpListenerContext context)
		{
			context.Request.AssertMethod(WebRequestMethods.Http.Post);
			var form = context.Request.GetPostData();

			string login, pass;
			if(!form.TryGetValue("login", out login) || string.IsNullOrEmpty(login))
				throw new HttpException(HttpStatusCode.BadRequest, "Empty 'login' value");

			if(!form.TryGetValue("pass", out pass) || string.IsNullOrEmpty(pass))
				throw new HttpException(HttpStatusCode.BadRequest, "Empty 'pass' value");

			if(login.Length > MaxLength || pass.Length > MaxLength)
				throw new HttpException(HttpStatusCode.BadRequest, "Too large login/pass (max len 64)");

			if(!Regex.IsMatch(login, @"^\w+$"))
				throw new HttpException(HttpStatusCode.BadRequest, @"Only \w chars allowed in login");

			var user = new User {Login = login, PassHash = PassHash.GetHash(pass)};
			if(!Program.DB.AddUser(user))
				throw new HttpException(HttpStatusCode.Conflict, string.Format("User '{0}' already exists", login));

			context.Response.SetCookie("login", login);
			context.Response.SetCookie("token", TokenCrypt.Encrypt(new Token {Login = login, DateTime = DateTime.UtcNow}.ToJsonString()), true);
			context.Response.SetCookie("expr", null);

			WriteString(context, "OK");
		}

		private const int MaxLength = 64;
	}
}
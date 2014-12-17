using System;
using System.Globalization;
using System.Net;
using Ciloci.Flee;
using heart.db;

namespace heart.handlers
{
	internal static class ExpressionHelper
	{
		public static string CalcExpression(string expression, Stat stat)
		{
			var context = new ExpressionContext();
			context.Imports.AddType(typeof(Math));
			context.Imports.AddType(typeof(StatMethods));
			context.Variables.Add("stat", stat);
			context.Options.ParseCulture = CultureInfo.InvariantCulture;
			try
			{
				var e = context.CompileGeneric<string>(expression);
				return e.Evaluate();
			}
			catch(Exception e)
			{
				var ex = e as ExpressionCompileException;
				throw new HttpException(HttpStatusCode.InternalServerError, ex != null ? ex.Message : "Failed to build expression");
			}
		}
	}
}
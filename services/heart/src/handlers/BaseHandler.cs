﻿using System;
using System.Net;
using System.Text;
using heart.utils;
using log4net;

namespace heart.handlers
{
	internal abstract class BaseHandler
	{
		protected BaseHandler(string prefix)
		{
			listener = new HttpListener();
			listener.Prefixes.Add(prefix);
		}

		public void Start()
		{
			//log.InfoFormat("listen '{0}'", listener.Prefixes.FirstOrDefault());
			listener.Start();
			listener.BeginGetContext(Callback, null);
		}

		private void Callback(IAsyncResult result)
		{
			listener.BeginGetContext(Callback, null);
			var context = listener.EndGetContext(result);
			try
			{
				context.Response.KeepAlive = true;
				ProcessRequest(context);
				//log.InfoFormat("{0} {1}", context.Request.HttpMethod, context.Request.RawUrl);
			}
			catch(HttpException exception)
			{
				//log.Error(exception);
				Error(context, exception.Status, exception.Message);
			}
			catch(Exception exception)
			{
				log.Error(exception);
				Error(context, HttpStatusCode.InternalServerError, "Internal server error");
			}
			CommonUtils.Try(() => context.Response.Close());
		}

		protected static void WriteString(HttpListenerContext context, string msg)
		{
			context.Response.ContentType = "text/plain; charset=utf-8";
			Write(context, msg == null ? null : Encoding.UTF8.GetBytes(msg));
		}

		protected static void WriteData(HttpListenerContext context, byte[] data)
		{
			context.Response.ContentType = "application/json";
			Write(context, data ?? EmptyJson);
		}

		private static void Write(HttpListenerContext context, byte[] data)
		{
			var response = context.Response;
			if(data == null)
			{
				response.ContentLength64 = 0;
				return;
			}
			response.ContentLength64 = data.Length;
			response.OutputStream.Write(data, 0, data.Length);
		}

		protected abstract void ProcessRequest(HttpListenerContext context);

		private static void Error(HttpListenerContext context, HttpStatusCode status, string msg)
		{
			CommonUtils.Try(() =>
			{
				//log.InfoFormat("{0} - {1}: {2}", status, status, msg);
				var response = context.Response;
				response.Headers.Clear();
				response.StatusCode = (int)status;
				response.ContentType = "text/plain; charset=utf-8";
				if(string.IsNullOrEmpty(msg))
				{
					response.ContentLength64 = 0;
					return;
				}
				var bytes = Encoding.UTF8.GetBytes(msg);
				response.ContentLength64 = bytes.Length;
				response.OutputStream.Write(bytes, 0, bytes.Length);
			});
		}

		private static readonly byte[] EmptyJson = Encoding.UTF8.GetBytes("{}");
		private static readonly ILog log = LogManager.GetLogger(typeof(BaseHandler));
		private readonly HttpListener listener;
	}
}
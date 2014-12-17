﻿using System;
using System.Collections;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net;
using heart.utils;

namespace heart.handlers
{
	internal class StaticHandler : BaseHandler
	{
		public StaticHandler(string prefix, string root)
			: base(prefix)
		{
			this.root = Path.GetFullPath(root);
			localPath = new Uri(prefix.Replace("+", "localhost").Replace("*", "localhost")).LocalPath;
		}

		protected override void ProcessRequest(HttpListenerContext context)
		{
			var fileInfo = GetFileInfo(context.Request.Url);
			if(fileInfo == null)
				throw new HttpException(HttpStatusCode.NotFound, "File not found");

			var lastModified = fileInfo.LastWriteTimeUtc.TruncSeconds();
			context.Response.AddHeader("Date", DateTime.UtcNow.ToString("r"));
			if(IsNotModifiedSince(context, lastModified))
			{
				context.Response.StatusCode = (int)HttpStatusCode.NotModified;
				return;
			}

			var contentType = GetContentType(Path.GetExtension(fileInfo.FullName));

			//context.Response.SendChunked = true;
			context.Response.AddHeader("Cache-Control", "max-age=" + MaxAge);
			context.Response.AddHeader("Last-Modified", lastModified.ToString("r"));
			context.Response.AddHeader("Accept-Ranges", "none");
			context.Response.AddHeader("Content-Type", contentType);
			context.Response.ContentType = contentType;

			var outputStream = context.Response.OutputStream;

			var acceptEncoding = context.Request.Headers["Accept-Encoding"].TrimToLower();
			if(acceptEncoding != null && !contentType.StartsWith("image") && !contentType.StartsWith("sound") && !contentType.StartsWith("video"))
			{
				/*if(acceptEncoding.IndexOf("gzip", StringComparison.Ordinal) >= 0)
				{
					outputStream = new GZipStream(outputStream, CompressionMode.Compress, false);
					context.Response.AddHeader("Content-Encoding", "gzip");
				}
				else if(acceptEncoding.IndexOf("deflate", StringComparison.Ordinal) >= 0)
				{
					outputStream = new DeflateStream(outputStream, CompressionMode.Compress, false);
					context.Response.AddHeader("Content-Encoding", "deflate");
				}*/
			}

			using(outputStream)
			using(var stream = fileInfo.OpenRead())
			{
				context.Response.ContentLength64 = fileInfo.Length;
				stream.CopyTo(outputStream);
				outputStream.Flush();
			}
		}

		private FileInfo GetFileInfo(Uri requestUrl)
		{
			var requestPath = requestUrl.LocalPath;

			if(!requestPath.StartsWith(localPath))
				return null;

			var path = requestPath.Substring(localPath.Length);
			var fullpath = Path.GetFullPath(Path.Combine(root, path));

			if(!fullpath.StartsWith(root))
				return null;

			if(fullpath == root)
			{
				var filepath = DefaultFiles.Select(filename => Path.Combine(fullpath, filename)).FirstOrDefault(File.Exists);
				if(filepath != null)
					fullpath = filepath;
			}

			var fileInfo = new FileInfo(fullpath);
			return !fileInfo.Exists ? null : fileInfo;
		}

		private static bool IsNotModifiedSince(HttpListenerContext context, DateTime lastModified)
		{
			DateTime ifModifiedSince;
			if(!DateTime.TryParseExact(context.Request.Headers["If-Modified-Since"], "r", CultureInfo.InvariantCulture, DateTimeStyles.AdjustToUniversal | DateTimeStyles.AssumeUniversal, out ifModifiedSince))
				ifModifiedSince = DateTime.MinValue;
			return ifModifiedSince >= lastModified;
		}

		private static string GetContentType(string fileExt)
		{
			return ContentTypes[fileExt] as string ?? "application/octet-stream";
		}

		private static readonly Hashtable ContentTypes = new Hashtable
		{
			{".txt", "text/plain"},
			{".htm", "text/html"},
			{".html", "text/html"},
			{".css", "text/css"},
			{".js", "application/javascript"},
			{".ico", "image/x-icon"},
			{".gif", "image/gif"},
			{".png", "image/png"},
			{".jpg", "image/jpeg"},
			{".jpeg", "image/jpeg"}
		};

		private static readonly string[] DefaultFiles =
		{
			"index.html",
			"default.html"
		};

		private const int MaxAge = 300;

		private readonly string root;
		private readonly string localPath;
	}
}
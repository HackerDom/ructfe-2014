using System;
using System.Security.Cryptography;
using System.Text;

namespace heart.db
{
	internal static class PassHash
	{
		public static string GetHash(string pass)
		{
			using(var sha = new HMACMD5(Key))
			{
				var bytes = Encoding.UTF8.GetBytes(pass);
				return Convert.ToBase64String(sha.ComputeHash(bytes));
			}
		}

		//NOTE: Hiii
		private static readonly byte[] Key = Convert.FromBase64String("L9r7XYZVjZ5UuAvfUPOf8DWWabM7SlyQDtv1H3PXxho=");
	}
}
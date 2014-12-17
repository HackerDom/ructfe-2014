﻿using System;
using System.IO;
using System.Runtime.Serialization;
using System.Security.Cryptography;
using System.Text;
using heart.utils;

namespace heart.handlers
{
	public static class TokenCrypt
	{
		static TokenCrypt()
		{
			try
			{
				CryptKey = AesKey.ParseJson(File.ReadAllText(KeyFile).Trim());
			}
			catch(FileNotFoundException)
			{
				using(var aes = new AesManaged())
				{
					aes.GenerateKey();
					aes.GenerateIV();
					CryptKey = new AesKey {Key = aes.Key, IV = aes.IV};
					File.WriteAllText(KeyFile, CryptKey.ToJsonString());
				}
			}
		}

		public static string Decrypt(string tokenString)
		{
			var tokenBytes = Convert.FromBase64String(tokenString);
			if(tokenBytes == null)
				throw new Exception(string.Format("Invalid token string '{0}'", tokenString));
			using(var crypt = new AesManaged())
			using(var decryptor = crypt.CreateDecryptor(CryptKey.Key, CryptKey.IV))
			{
				var bytes = decryptor.TransformFinalBlock(tokenBytes, 0, tokenBytes.Length);
				return Encoding.UTF8.GetString(bytes);
			}
		}

		public static string Encrypt(string tokenString)
		{
			var tokenBytes = Encoding.UTF8.GetBytes(tokenString);
			using(var crypt = new AesManaged())
			using(var encryptor = crypt.CreateEncryptor(CryptKey.Key, CryptKey.IV))
			{
				var bytes = encryptor.TransformFinalBlock(tokenBytes, 0, tokenBytes.Length);
				return Convert.ToBase64String(bytes);
			}
		}

		[DataContract]
		private class AesKey : Data<AesKey>
		{
			[DataMember(Name = "k", Order = 1)] private string key;
			[DataMember(Name = "iv", Order = 2)] private string iv;

			//NOTE: [OnSerializing] and [OnDeserialized] not used in mono
			[IgnoreDataMember] public byte[] Key { get { return Convert.FromBase64String(key); } set { key = Convert.ToBase64String(value); } }
			[IgnoreDataMember] public byte[] IV { get { return Convert.FromBase64String(iv); } set { iv = Convert.ToBase64String(value); } }

			/*[OnSerializing]
			private void OnSerializing(StreamingContext context)
			{
				key = Convert.ToBase64String(Key);
				iv = Convert.ToBase64String(IV);
			}

			[OnDeserialized]
			private void OnDeserialized(StreamingContext context)
			{
				Key = Convert.FromBase64String(key);
				IV = Convert.FromBase64String(iv);
			}*/
		}

		private static readonly string KeyFile = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "key");
		private static readonly AesKey CryptKey;
	}
}
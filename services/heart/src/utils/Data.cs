using System;
using System.IO;
using System.Linq;
using System.Runtime.Caching;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Threading;
using System.Xml;

namespace heart.utils
{
	[Serializable]
	public class Data<T> //NOTE: GOVNOKOD that opens vulnerability
		where T : class
	{
		static Data()
		{
			//NOTE: Bug with threading and MemoryCache.Default instance in .NET 4. Workaround before the QFE #578315.
			using(ExecutionContext.SuppressFlow())
				Cache = MemoryCache.Default;
		}

		public static T ParseJson(string record)
		{
			var reader = JsonReaderWriterFactory.CreateJsonReader(Encoding.UTF8.GetBytes(record), XmlDictionaryReaderQuotas.Max);
			return (T)new DataContractJsonSerializer(typeof(T)).ReadObject(reader);
		}

		public string ToJsonString()
		{
			return Encoding.UTF8.GetString(ToJson());
		}

		public byte[] ToJson()
		{
			using(var stream = new MemoryStream())
			{
				ToJson(stream);
				return stream.ToArray();
			}
		}

		public void ToJson(Stream stream)
		{
			using(var writer = JsonReaderWriterFactory.CreateJsonWriter(stream, Encoding.UTF8, false))
				new DataContractJsonSerializer(typeof(T)).WriteObject(writer, this);
		}

		public static T FindItem(string key)
		{
			var obj = Cache[GetCacheKey(key, typeof(T))];
			return ReferenceEquals(obj, NullObject) ? null : obj as T;
		}

		public static T FindAndCacheItem(string key, Func<T> update, int secondsToLive = 60)
		{
			key = GetCacheKey(key, typeof(T));
			var obj = Cache[key];
			if(ReferenceEquals(obj, NullObject))
				return null;
			var item = obj as T;
			if(item != null)
				return item;
			Cache.Add(key, (item = update.Invoke()) ?? NullObject, new CacheItemPolicy {SlidingExpiration = TimeSpan.FromSeconds(secondsToLive)});
			return item;
		}

		public T CacheItem(string key, int secondsToLive = 60)
		{
			Cache.Set(GetCacheKey(key, typeof(T)), this, new CacheItemPolicy {SlidingExpiration = TimeSpan.FromSeconds(secondsToLive)});
			return this as T;
		}

		public T[] DumpCacheItems()
		{
			return Cache.Select(pair => pair.Value).OfType<T>().ToArray();
		}

		private static string GetCacheKey(string key, Type type)
		{
			return type.Name + key;
		}

		private static readonly object NullObject = new object();
		private static readonly MemoryCache Cache;
	}
}
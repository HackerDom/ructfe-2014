using System;
using System.Linq;
using heart.utils;
using ServiceStack.Redis;

namespace heart.db
{
	internal class DbProvider
	{
		public DbProvider(string redisHostPort)
		{
			manager = new PooledRedisClientManager(redisHostPort);
		}

		public void Insert(string login, DatePoint point)
		{
			//NOTE: GOVNOKOD - thanks to Mono ServiceStack lib implementation
			using(var redis = manager.GetClient())
			{
				redis.AddItemToSortedSet(StatsSetIdPrefix + login, point.ToJsonString(), RedisClient.GetLexicalScore(point.Date.ToShortUnixTime().ToString()));
			}
		}

		public void SetExpression(string login, string expression, string readable)
		{
			using(var redis = manager.GetClient())
			{
				var user = User.ParseJson(redis.GetValueFromHash(UsersHashId, login));
				user.Expression = expression;
				user.Readable = readable;
				redis.SetEntryInHash(UsersHashId, login, user.CacheItem(login).ToJsonString());
			}
		}

		public bool AddUser(User user)
		{
			using(var redis = manager.GetClient())
			{
				return redis.SetEntryInHashIfNotExists(UsersHashId, user.Login, user.CacheItem(user.Login).ToJsonString());
			}
		}

		public User FindUser(string login)
		{
			return User.FindAndCacheItem(login, () =>
			{
				using(var redis = manager.GetClient())
				{
					var value = redis.GetValueFromHash(UsersHashId, login);
					return value != null ? User.ParseJson(value).CacheItem(login) : null;
				}
			});
		}

		public Stat TakeSafe(string login, DateTime from, DateTime to)
		{
			return Stat.FindAndCacheItem(login, () =>
			{
				using(var redis = manager.GetClient())
				{
					var list = redis.GetRangeFromSortedSetByLowestScore(StatsSetIdPrefix + login, @from.ToShortUnixTime().ToString(), to.ToShortUnixTime().ToString());
					return new Stat {Points = list.Select(DatePoint.ParseJson).ToArray()}.CacheItem(StatsSetIdPrefix + login);
				}
			});
		}

		private const string UsersHashId = "u";
		private const string StatsSetIdPrefix = "s:";

		private readonly PooledRedisClientManager manager;
	}
}
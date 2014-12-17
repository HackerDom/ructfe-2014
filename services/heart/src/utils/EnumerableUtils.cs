﻿using System;
using System.Collections.Generic;

namespace heart.utils
{
	internal static class EnumerableUtils
	{
		public static Dictionary<TKey, TValue> ToDict<T, TKey, TValue>(this IEnumerable<T> enumerable, Func<T, TKey> keyFunc, Func<T, TValue> valFunc)
		{
			var dict = new Dictionary<TKey, TValue>();
			enumerable.ForEach(item => dict[keyFunc(item)] = valFunc(item));
			return dict;
		}

		public static void ForEach<T>(this IEnumerable<T> enumerable, Action<T> action)
		{
			if(enumerable == null)
				return;
			foreach(var item in enumerable)
				action(item);
		}
	}
}
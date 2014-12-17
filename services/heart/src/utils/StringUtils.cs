namespace heart.utils
{
	internal static class StringUtils
	{
		public static string TrimToLower(this string value)
		{
			return string.IsNullOrWhiteSpace(value) ? null : value.Trim().ToLowerInvariant();
		}
	}
}
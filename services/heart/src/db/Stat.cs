using System.Runtime.Serialization;
using heart.utils;

namespace heart.db
{
	[DataContract]
	public class Stat : Data<Stat>
	{
		[DataMember(Name = "points", Order = 1, EmitDefaultValue = false)] public DatePoint[] Points;
	}
}
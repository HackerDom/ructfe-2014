using System;
using System.Runtime.Serialization;
using heart.utils;

namespace heart.db
{
	[DataContract]
	public class DatePoint : Data<DatePoint>
	{
		[DataMember(Name = "dt", Order = 1, EmitDefaultValue = false)] private long date;
		[DataMember(Name = "val", Order = 2, EmitDefaultValue = false)] public int Value;
		[DataMember(Name = "evt", Order = 3, EmitDefaultValue = false)] public string Event;

		[IgnoreDataMember] public DateTime Date { get { return DateTimeUtils.ParseUnixTime(date); } set { date = DateTimeUtils.ToUnixTime(value); } }
	}
}
using System;
using System.Runtime.Serialization;
using heart.utils;

namespace heart.handlers
{
	[DataContract]
	internal class Token : Data<Token>
	{
		[DataMember(Name = "login", Order = 1)] public string Login;
		[DataMember(Name = "dt", Order = 2)] public DateTime DateTime;
	}
}